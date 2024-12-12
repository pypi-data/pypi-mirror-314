import collections.abc
import functools
import inspect
import signal
import sys
import types
import typing

from .connector import Connector

T = typing.TypeVar("T")


Generator = typing.Union[
    collections.abc.Generator[T, None, None],
    collections.abc.AsyncGenerator[T, None],
]


AppFactory = collections.abc.Callable[
    ...,
    typing.Union[
        Connector,
        collections.abc.Awaitable[Connector],
        Generator,
    ],
]


async def compose_app(create_app: AppFactory) -> Connector:
    """
    Creates and configures a ready to use Connector.

    Args:
      create_app: The factory method used to create the Connector instance.

    Returns:
      The newly created Connector.

    Raises:
      ValueError: If create_app does not follow the required interface.
    """

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    app = await init_app(app_factory=create_app)

    return app


# pylint: disable-next=unused-argument
def signal_handler(signum: int, frame: typing.Optional[types.FrameType]) -> None:
    """
    Gracefully handle received signals.

    Args:
      signum: The signal number.
      frame: The current stack frame.
    """

    sys.exit(signum)


async def init_app(app_factory: AppFactory) -> Connector:
    """
    Uses the provided factory method to init a new Connector.

    Args:
      app_factory: The factory method to call.

    Returns:
      The initialized Connector.

    Raises:
      ValueError: If app_factory does not follow the required interface.
    """

    if inspect.isasyncgenfunction(app_factory) or inspect.isgeneratorfunction(app_factory):
        generator: Generator[Connector] = app_factory()
        generator = _sync_to_async_gen(generator)

        try:
            app = await generator.__anext__()
        except (StopAsyncIteration, StopIteration):
            raise ValueError("Unable to create app: `create_app` did not yield a value.") from None

        shutdown_handler = functools.partial(_shutdown_yield, generator)
        app.on_shutdown(handler=shutdown_handler)

        return app

    if inspect.iscoroutinefunction(app_factory):
        return await app_factory()

    if inspect.isfunction(app_factory):
        return app_factory()

    raise ValueError(f"Invalid `create_app`: '{app_factory}'. Provide a callable function that returns a Connector.")


async def _shutdown_yield(generator: collections.abc.AsyncGenerator[T, None]) -> None:
    """
    Execute the shutdown of a factory function by advancing the iterator
    after the yield and ensure the iteration ends (if not it means there is
    more than one yield in the function).

    Args:
      generator: The factory function to create the app.
    """

    try:
        await generator.__anext__()
    except (StopAsyncIteration, StopIteration):
        pass
    else:
        await _shutdown_yield(generator)


async def _sync_to_async_gen(generator: Generator[T]) -> collections.abc.AsyncGenerator[T, None]:
    """
    Wraps any generator into an async generator.

    Args:
      generator: The generator to wrap as async.

    Returns:
      The async generator.
    """

    if inspect.isasyncgen(generator):
        async for item in generator:
            yield item

        return

    if inspect.isgenerator(generator):
        while True:
            try:
                yield next(generator)
            except StopIteration:
                return

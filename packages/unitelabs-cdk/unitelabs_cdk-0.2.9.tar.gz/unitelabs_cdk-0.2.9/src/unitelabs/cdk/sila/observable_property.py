import collections.abc
import dataclasses
import functools
import inspect
import typing

import sila.server as sila

from . import utils
from .data_types import parser
from .defined_execution_error import define_error

T = typing.TypeVar("T")
Stream = collections.abc.AsyncIterator[T]


@dataclasses.dataclass
class ObservableProperty:
    identifier: str = ""
    display_name: str = ""
    description: str = ""
    errors: list[type[Exception]] = dataclasses.field(default_factory=list)

    def __call__(self, function: typing.Callable):
        setattr(function, "__handler", self)
        return function

    def attach(self, feature: sila.Feature, function: typing.Callable):
        name = function.__name__.lower().removeprefix("subscribe_")
        display_name = self.display_name or utils.humanize(name)
        identifier = self.identifier or display_name.replace(" ", "")
        description = self.description or inspect.getdoc(function) or ""

        type_hint = inspect.signature(function).return_annotation
        type_hint = typing.get_args(type_hint)[0]

        observable_property = sila.ObservableProperty(
            identifier=identifier,
            display_name=display_name,
            description=description,
            function=functools.partial(self.execute, function),
            errors=[define_error(error) for error in self.errors],
            data_type=parser.parse(type_hint, feature),
        )
        feature.add_handler(observable_property)

        return observable_property

    async def execute(self, function: collections.abc.Callable, **kwargs):
        """
        Executes a given function with the provided keyword arguments.

        Args:
          function: The function to be executed.
          **kwargs: Additional keyword arguments to be passed to the function.

        Returns:
          The result of the function execution.

        Raises:
          DefinedExecutionError: If the error type is in the list of defined errors.
          Exception: If an unexpected error occurs during execution.
        """

        try:
            responses = function(**kwargs)

            if inspect.isawaitable(responses):
                responses = await responses

            if inspect.isasyncgen(responses):
                async for response in responses:
                    yield response

            if inspect.isgenerator(responses):
                for response in responses:
                    yield response

        except Exception as error:
            if type(error) in self.errors:
                raise define_error(error) from None

            raise error

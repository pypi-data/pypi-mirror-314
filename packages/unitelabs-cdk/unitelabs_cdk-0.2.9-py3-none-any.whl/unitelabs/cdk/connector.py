import asyncio
import contextlib
import logging
import typing

from sila import cloud_connector, discovery, server
from unitelabs.cdk.features.core.sila_service import SiLAService

from .config import Config

Handler = typing.Callable[..., typing.Union[typing.Any, typing.Awaitable[typing.Any]]]


class Connector:
    """Main app"""

    def __init__(self, config: typing.Optional[dict] = None):
        self.__config = Config.model_validate(config or {}, strict=False)

        self._shutdown_handlers: list[Handler] = []

        self._sila_server = server.Server(config=self.config.sila_server)
        self.logger.debug(self._sila_server)
        self._broadcaster = discovery.Broadcaster(self._sila_server)

        self.config.cloud_server_endpoint["options"] = {
            # The period (in milliseconds) after which a keepalive ping is sent on the transport.
            "grpc.keepalive_time_ms": 60 * 1000,
            # The amount of time (in milliseconds) the sender of the keepalive ping waits for an
            # acknowledgement. If it does not receive an acknowledgment within this time, it will
            # close the connection.
            "grpc.keepalive_timeout_ms": 3 * 60 * 1000,
            # If set to 1 (0 : false; 1 : true), allows keepalive pings to be sent even if there
            # are no calls in flight.
            "grpc.keepalive_permit_without_calls": 0,
            # How many pings can the client send before needing to send a data/header frame.
            "grpc.http2.max_pings_without_data": 0,
        } | self.config.cloud_server_endpoint.get("options", {})

        self._cloud_server_endpoint = cloud_connector.CloudServerEndpoint(
            self._sila_server, self.config.cloud_server_endpoint
        )

        self.register(SiLAService())

    def register(self, feature: server.Feature):
        """Register a new feature to this driver"""
        self.logger.debug("Added feature: %s", feature)
        self._sila_server.add_feature(feature)

    async def start(self):
        """
        Start the connector and all related services.
        """

        try:
            await asyncio.gather(
                asyncio.create_task(self._sila_server.start()),
                asyncio.create_task(self._broadcaster.start()),
                asyncio.create_task(self._cloud_server_endpoint.start()),
            )
        except asyncio.CancelledError:
            pass
        finally:
            await self.close()

    async def close(self):
        """
        Close the connector and all related services.
        """

        for shutdown_handler in self._shutdown_handlers:
            with contextlib.suppress(Exception):
                if asyncio.iscoroutinefunction(shutdown_handler):
                    await shutdown_handler()
                else:
                    shutdown_handler()

    @property
    def config(self) -> Config:
        return self.__config

    @property
    def sila_server(self) -> server.Server:
        return self._sila_server

    @property
    def logger(self) -> logging.Logger:
        """A standard Python :class:`~logging.Logger` for the app."""
        return logging.getLogger(__package__)

    @property
    def debug(self) -> bool:
        """Whether debug mode is enabled."""
        return True

    def on_shutdown(self, handler: Handler) -> None:
        """
        Add a shutdown hook to be called in the terminating phase (in response
        to an explicit call to `app.close()` or upon receipt of system signals
        such as SIGINT or SIGTERM).

        Args:
          handler: The method to be called on shutdown.

        Raises:
          TypeError: If the `handler` argument is not callable.
        """

        if not callable(handler):
            raise TypeError("The `handler` argument must be callable.")

        self._shutdown_handlers.append(handler)

    def off_shutdown(self, handler: Handler) -> None:
        """
        Remove a previously added shutdown hook.

        Args:
          handler: The handler to be removed from the shutdown hooks.
        """

        try:
            self._shutdown_handlers.remove(handler)
        except ValueError:
            pass

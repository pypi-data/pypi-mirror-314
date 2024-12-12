from __future__ import annotations

import asyncio
import dataclasses
import typing

from unitelabs.cdk import sila

from .lock_controller_base import InvalidLockIdentifier, LockControllerBase, ServerAlreadyLocked, ServerNotLocked


@dataclasses.dataclass
class Lock:
    identifier: str
    timeout: sila.datetime.timedelta
    last_usage: sila.datetime.datetime = dataclasses.field(default_factory=sila.datetime.datetime.now)

    @property
    def expired(self) -> bool:
        return (sila.datetime.datetime.now() - self.timeout) > self.last_usage


class LockController(LockControllerBase):
    def __init__(self, affects: list[sila.identifiers.FullyQualifiedIdentifier] | None = None):
        super().__init__()

        self.affects = affects
        self._lock: typing.Optional[Lock] = None
        self._event = asyncio.Event()

    @property
    def lock(self) -> typing.Optional[Lock]:
        if self._lock and self._lock.expired:
            self._event.set()
            self._lock = None

        return self._lock

    @lock.setter
    def lock(self, value: typing.Optional[Lock]):
        self._event.set()
        self._lock = value

    async def subscribe_is_locked(self):
        try:
            while True:
                yield self.lock is not None
                await self._event.wait()
                self._event.clear()
        finally:
            pass

    def lock_server(self, lock_identifier, timeout):
        if self.lock:
            raise ServerAlreadyLocked()

        self.lock = Lock(identifier=lock_identifier, timeout=sila.datetime.timedelta(seconds=timeout))

    def unlock_server(self, lock_identifier):
        lock = self.lock
        if lock is None:
            raise ServerNotLocked()

        if lock.identifier != lock_identifier:
            raise InvalidLockIdentifier()

        self.lock = None

    def add_to_server(self, server):
        self.add_metadata(LockIdentifier(self))
        super().add_to_server(server=server)


class LockIdentifier(sila.Metadata):
    """
    The lock identifier has to be sent with every (lock protected) call in order to use the functionality
    of a locked SiLA Server.
    """

    def __init__(self, lock_controller: LockController):
        super().__init__(data_type=sila.data_types.String(), errors=[InvalidLockIdentifier()])
        self.lock_controller = lock_controller

    def affects(self) -> list[sila.identifiers.FullyQualifiedIdentifier]:
        if not self.lock_controller.server:
            return self.lock_controller.affects or []

        return self.lock_controller.affects or [
            feature.fully_qualified_identifier
            for feature in self.lock_controller.server.features.values()
            if feature.identifier not in ("SiLAService", "LockController")
        ]

    def intercept(self, handler: sila.Handler, metadata_: dict):
        if any(str(handler.fully_qualified_identifier).startswith(str(affected)) for affected in self.affects()):
            data: bytes | None = metadata_.get(
                "sila-org.silastandard-core-lockcontroller-v2-metadata-lockidentifier-bin", None
            )

            if data is None:
                raise sila.errors.FrameworkError(
                    error_type=sila.errors.FrameworkError.Type.INVALID_METADATA,
                    message="The required SiLA Client Metadata has not been sent along or is invalid.",
                )

            identifier: str = self.message.decode(data).get("LockIdentifier", "")

            if not self.lock_controller.lock or self.lock_controller.lock.identifier != identifier:
                raise InvalidLockIdentifier()

            self.lock_controller.lock.last_usage = sila.datetime.datetime.now()

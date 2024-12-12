import abc
import typing
from collections.abc import AsyncIterator

from unitelabs.cdk import sila


class ServerAlreadyLocked(sila.DefinedExecutionError):
    """The SiLA Server can not be locked because it is already locked."""


class ServerNotLocked(sila.DefinedExecutionError):
    """The SiLA Server can not be unlocked because it is not locked."""


class InvalidLockIdentifier(sila.DefinedExecutionError):
    """The sent lock identifier is not valid."""


class LockControllerBase(sila.Feature, metaclass=abc.ABCMeta):
    """
    This Feature allows a SiLA Client to lock a SiLA Server for exclusive use, preventing other SiLA Clients
    from using the SiLA Server while it is locked. To lock a SiLA Server a Lock Identifier has to be set, using the
    'LockServer' command. This Lock Identifier has to be sent along with every (lock protected)
    request to the SiLA Server in order to use its functionality.

    To send the lock identifier the SiLA Client Meta Data 'LockIdentifier' has to be used.

    When locking a SiLA Server a timeout can be specified that defines the time after which the SiLA Server will
    be automatically unlocked if no request with a valid lock identifier has been received meanwhile.
    After the timeout has expired or after explicit unlock no lock identifier has to be sent any more.
    """

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="core",
            version="2.0",
            maturity_level="Draft",
        )

    @abc.abstractmethod
    @sila.ObservableProperty()
    async def subscribe_is_locked(self) -> AsyncIterator[bool]:
        """
        Returns true if the SiLA Server is currently locked or false else.

        This property MUST NOT be lock protected, so that any SiLA Client can query the current lock state
        of a SiLA Server.
        """

    @abc.abstractmethod
    @sila.UnobservableCommand(errors=[ServerAlreadyLocked])
    def lock_server(
        self,
        lock_identifier: str,
        timeout: typing.Annotated[
            int,
            sila.constraints.Unit(
                label="s", components=[sila.constraints.Unit.Component(unit=sila.constraints.SIUnit.SECOND)]
            ),
        ],
    ) -> None:
        """
        Locks a SiLA Server for exclusive use by setting a lock identifier that has to be sent along with
        any following (lock protected) request as long as the SiLA Server is locked.
        The lock can be reset by issuing the 'Unlock Server' command.

        .. parameter:: The lock identifier that has to be sent along with every (lock protected) request to use the
                       server's functionality.
        .. parameter:: The time (in seconds) after a SiLA Server is automatically unlocked when no request with a valid
                       lock identifier has been received meanwhile. A timeout of zero seconds specifies an infinite time (no timeout).
        """

    @abc.abstractmethod
    @sila.UnobservableCommand(errors=[ServerNotLocked, InvalidLockIdentifier])
    def unlock_server(self, lock_identifier: str) -> None:
        """
        Unlocks a locked SiLA Server. No lock identifier has to be sent for any following calls until
        the server is locked again via the 'Lock Server' command.

        .. parameter:: The lock identifier that has been used to lock the SiLA Server.
        """

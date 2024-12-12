import abc

from unitelabs.cdk import sila


class GripControllerBase(sila.Feature, metaclass=abc.ABCMeta):
    """
    Controls a robotic gripper for e.g. labware transfer operations.
    """

    def __init__(self):
        super().__init__(
            originator="io.unitelabs",
            category="robot",
            version="1.0",
            maturity_level="Draft",
        )

    @abc.abstractmethod
    @sila.UnobservableCommand()
    async def grip(self) -> None:
        """Closes the gripper."""

    @abc.abstractmethod
    @sila.UnobservableCommand()
    async def release(self) -> None:
        """Releases the gripper."""

import abc
import typing

from unitelabs.cdk import sila


class CountdownTooLong(sila.DefinedExecutionError):
    """
    The provided countdown duration was too large
    """


class TimerProviderBase(sila.Feature, metaclass=abc.ABCMeta):
    """
    Provides a timer command and the current time
    """

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="examples",
            version="1.0",
            maturity_level="Draft",
        )

    @abc.abstractmethod
    @sila.ObservableCommand(errors=[CountdownTooLong])
    @sila.Response(name="Message")
    @sila.Response(name="Timestamp")
    @sila.IntermediateResponse(name="CurrentNumber")
    async def countdown(
        self,
        n: typing.Annotated[
            int,
            sila.constraints.Unit(
                label="Second",
                components=[sila.constraints.UnitComponent(unit=sila.constraints.SIUnit.SECOND)],
            ),
            sila.constraints.MinimalInclusive(0),
        ],
        message: str,
        *,
        status: sila.Status,
        intermediate: sila.Intermediate[typing.Annotated[int, sila.constraints.MinimalExclusive(0)]],
    ) -> tuple[str, sila.datetime.datetime]:
        """
        Count down from N to 0, then return the given message and the current time
        .. parameter:: The number from which to count down
            :name: N
        .. parameter:: The message to return on completion
        .. yield:: The current number
        .. return:: The message provided as parameter
        .. return:: The timestamp when the countdown finished
        """

    @abc.abstractmethod
    @sila.ObservableProperty()
    async def subscribe_current_time(self) -> sila.Stream[sila.datetime.time]:
        """The current time"""

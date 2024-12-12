import asyncio

from unitelabs.cdk import sila


class ObservableCommandTest(sila.Feature):
    """
    This is a test feature to test observable commands.
    It specifies various observable commands and returns defined answers to validate against.
    """

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="test",
            version="1.0",
        )

    @sila.ObservableCommand()
    @sila.IntermediateResponse(name="Current Iteration")
    @sila.Response(name="Iteration Response")
    async def observable_iteration(
        self, number_iterations: int, *, status: sila.Status, intermediate: sila.Intermediate[int]
    ) -> int:
        """
        Observable iteration, running NumberIterations times and returning the current count as intermediate result.

        .. parameter:: Number of Iterations to perform
        .. yield:: Return the current iteration in progress, starting from 0 to NumberIterations (excluded).
        .. return:: If the command ended successfully the response should be NumberIterations - 1
        """
        for i in range(number_iterations):
            status.update(
                progress=i / (number_iterations - 1),
                remaining_time=sila.datetime.timedelta(seconds=number_iterations - i - 1),
            )
            intermediate.send(i)
            await asyncio.sleep(1)

        return number_iterations - 1

    @sila.ObservableCommand()
    @sila.Response(name="Received Value")
    async def echo_value_async(self, value: int, delay_in_ms: int, *, status: sila.Status) -> int:
        """
        Echo the given value asynchronously after the specified delay.

        .. parameter:: The value to echo
        .. parameter:: The delay in milliseconds
        .. return:: The Received Value
        """
        seconds, rest = divmod(delay_in_ms, 1000)
        for i in range(int(seconds)):
            status.update(
                progress=i / (delay_in_ms / 1000),
                remaining_time=sila.datetime.timedelta(microseconds=(delay_in_ms - i * 1000) * 1000),
            )
            await asyncio.sleep(1)

        status.update(
            progress=int(seconds) / (delay_in_ms / 1000),
            remaining_time=sila.datetime.timedelta(microseconds=rest * 1000),
        )
        await asyncio.sleep(rest / 1000)

        return value

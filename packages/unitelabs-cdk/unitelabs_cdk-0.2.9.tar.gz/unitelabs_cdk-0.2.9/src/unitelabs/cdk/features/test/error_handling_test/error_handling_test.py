from unitelabs.cdk import sila


class TestError(Exception):
    """An error exclusively used for testing purposes"""


class ErrorHandlingTest(sila.Feature):
    """
    Tests that errors are propagated correctly
    """

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="test",
            version="1.0",
        )

    @sila.UnobservableCommand(errors=[TestError])
    async def raise_defined_execution_error(self) -> None:
        """
        Raises the "Test Error" with the error message 'SiLA2_test_error_message'
        """

        raise TestError("SiLA2_test_error_message")

    @sila.ObservableCommand(errors=[TestError])
    async def raise_defined_execution_error_observably(self, *, status: sila.Status) -> None:
        """
        Raises the "Test Error" with the error message 'SiLA2_test_error_message'
        """

        raise TestError("SiLA2_test_error_message")

    @sila.UnobservableCommand()
    async def raise_undefined_execution_error(self) -> None:
        """
        Raises an Undefined Execution Error with the error message 'SiLA2_test_error_message'
        """

        raise RuntimeError("SiLA2_test_error_message")

    @sila.ObservableCommand()
    async def raise_undefined_execution_error_observably(self, *, status: sila.Status) -> None:
        """
        Raises the "Test Error" with the error message 'SiLA2_test_error_message'
        """

        raise RuntimeError("SiLA2_test_error_message")

    @sila.UnobservableProperty(errors=[TestError])
    async def raise_defined_execution_error_on_get(self) -> int:
        """
        A property that raises a "Test Error" on get with the error message 'SiLA2_test_error_message'
        """

        raise TestError("SiLA2_test_error_message")

    @sila.ObservableProperty(errors=[TestError])
    async def raise_defined_execution_error_on_subscribe(self) -> sila.Stream[int]:
        """
        A property that raises a "Test Error" on subscribe with the error message 'SiLA2_test_error_message'
        """

        raise TestError("SiLA2_test_error_message")

    @sila.UnobservableProperty()
    async def raise_undefined_execution_error_on_get(self) -> int:
        """
        A property that raises an Undefined Execution Error on get with the error message 'SiLA2_test_error_message'
        """

        raise RuntimeError("SiLA2_test_error_message")

    @sila.ObservableProperty()
    async def raise_undefined_execution_error_on_subscribe(self) -> sila.Stream[int]:
        """
        A property that raises an Undefined Execution Error on subscribe with the error message 'SiLA2_test_error_message'
        """

        raise RuntimeError("SiLA2_test_error_message")

    @sila.ObservableProperty(errors=[TestError])
    async def raise_defined_execution_error_after_value_was_sent(self) -> sila.Stream[int]:
        """
        A property that first sends the integer value 1 and then raises a Defined Execution Error with the error message 'SiLA2_test_error_message'
        """

        yield 1

        raise TestError("SiLA2_test_error_message")

    @sila.ObservableProperty()
    async def raise_undefined_execution_error_after_value_was_sent(self) -> sila.Stream[int]:
        """
        A property that first sends the integer value 1 and then raises a Undefined Execution Error with the error message 'SiLA2_test_error_message'
        """

        yield 1

        raise RuntimeError("SiLA2_test_error_message")

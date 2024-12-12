import collections.abc
import dataclasses
import functools
import inspect
import typing

import sila.server as sila

from . import utils
from .commands import Parameters, Responses
from .defined_execution_error import define_error


@dataclasses.dataclass
class UnobservableCommand:
    identifier: str = ""
    display_name: str = ""
    description: str = ""
    errors: list[type[Exception]] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.parameter_by_identifier = {}
        self.responses = sila.data_types.Structure()

    def __call__(self, function: typing.Callable):
        setattr(function, "__handler", self)
        return function

    def attach(self, feature: sila.Feature, function: typing.Callable):
        docs = utils.parse_docs(inspect.getdoc(function))

        display_name = self.display_name or utils.humanize(function.__name__)
        identifier = self.identifier or str(display_name).replace(" ", "")
        description = self.description or docs.get("default", "")

        parameters = Parameters.from_signature(feature, function)
        self.responses = Responses.from_signature(feature, function)
        self.parameter_by_identifier = parameters.get_mapping(function)

        unobservable_command = sila.UnobservableCommand(
            identifier=identifier,
            display_name=display_name,
            description=description,
            function=functools.partial(self.execute, function),
            errors=[define_error(error) for error in self.errors],
            parameters=parameters,
            responses=self.responses,
        )
        feature.add_handler(unobservable_command)

        return unobservable_command

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
            parameters = self.parse_parameters(kwargs)
            responses = function(**parameters)
            if inspect.isawaitable(responses):
                responses = await responses

            return self.parse_responses(responses)
        except Exception as error:
            if type(error) in self.errors:
                raise define_error(error) from None

            raise error

    def parse_parameters(self, parameters: dict) -> dict:
        result = {}
        for key, parameter in parameters.items():
            key = self.parameter_by_identifier.get(key, key)
            result[key] = parameter

        return result

    def parse_responses(self, responses) -> dict:
        if responses is None:
            return {}

        result = {}
        responses = [responses] if not isinstance(responses, tuple) else responses
        for index, response in enumerate(responses):
            key = self.responses.elements[index].identifier if index < len(self.responses.elements) else index
            result[key] = response

        return result

import collections.abc
import dataclasses
import functools
import inspect
import typing

import sila.server as sila

from . import utils
from .data_types import parser
from .defined_execution_error import define_error


@dataclasses.dataclass
class UnobservableProperty:
    identifier: str = ""
    display_name: str = ""
    description: str = ""
    errors: list[type[Exception]] = dataclasses.field(default_factory=list)

    def __call__(self, function: collections.abc.Callable):
        setattr(function, "__handler", self)
        return function

    def attach(self, feature: sila.Feature, function: typing.Callable):
        name = function.__name__.lower().removeprefix("get_")
        display_name = self.display_name or utils.humanize(name)
        identifier = self.identifier or display_name.replace(" ", "")
        description = self.description or inspect.getdoc(function) or ""

        type_hint = inspect.signature(function).return_annotation

        unobservable_property = sila.UnobservableProperty(
            identifier=identifier,
            display_name=display_name,
            description=description,
            function=functools.partial(self.execute, function),
            errors=[define_error(error) for error in self.errors],
            data_type=parser.parse(type_hint, feature),
        )
        feature.add_handler(unobservable_property)

        return unobservable_property

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

            return responses
        except Exception as error:
            if type(error) in self.errors:
                raise define_error(error) from None

            raise error

import dataclasses
import inspect
import typing

import sila.server as sila

from . import utils


def define_error(exception: typing.Union[Exception, type[Exception]]) -> sila.errors.DefinedExecutionError:
    """
    Convert an exception into a defined execution error.

    Args:
      exception: The exception class or instance to convert.

    Returns:
      A DefinedExecutionError object with the parsed information from the exception.
    """

    if inspect.isclass(exception):
        exception = exception()

    display_name = utils.to_display_name(exception.__class__.__name__)
    identifier = display_name.replace(" ", "")
    description = str(exception) or inspect.getdoc(exception) or ""

    return sila.errors.DefinedExecutionError(identifier=identifier, display_name=display_name, description=description)


@dataclasses.dataclass
class DefinedExecutionError(sila.errors.DefinedExecutionError):
    def __init__(self, *args, identifier: str = "", display_name: str = "", description: str = "", **kwargs):
        display_name = display_name or utils.to_display_name(self.__class__.__name__)
        identifier = identifier or display_name.replace(" ", "")
        description = description or inspect.getdoc(self) or ""

        super().__init__(*args, identifier=identifier, display_name=display_name, description=description, **kwargs)

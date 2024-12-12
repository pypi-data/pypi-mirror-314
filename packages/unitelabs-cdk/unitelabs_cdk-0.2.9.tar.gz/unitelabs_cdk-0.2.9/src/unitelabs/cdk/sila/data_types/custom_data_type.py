import abc
import dataclasses
import inspect
import typing

from .. import utils


@dataclasses.dataclass
class CustomDataType(abc.ABC):
    identifier: typing.ClassVar[str] = ""
    display_name: typing.ClassVar[str] = ""
    description: typing.ClassVar[str] = ""

    def __init_subclass__(cls, *args, identifier="", display_name="", description="", **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)

        docs = utils.parse_docs(inspect.getdoc(cls))

        cls.display_name = display_name or utils.to_display_name(cls.__name__)
        cls.identifier = identifier or cls.display_name.replace(" ", "")
        cls.description = description or docs.get("default", "")

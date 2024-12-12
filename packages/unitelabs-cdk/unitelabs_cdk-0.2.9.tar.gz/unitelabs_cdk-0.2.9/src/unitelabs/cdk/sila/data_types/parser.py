from __future__ import annotations

import dataclasses
import inspect
import typing

import sila.server as sila
from sila import identifiers

from .. import utils
from .custom_data_type import CustomDataType
from .data_type_definition import DataTypeDefinition


def parse(type_hint: typing.Type, feature: sila.Feature) -> sila.data_types.DataType:
    origin = typing.get_origin(type_hint) or type_hint

    if origin is None or issubclass(origin, type(None)):
        return sila.data_types.Void()
    if issubclass(origin, CustomDataType):
        feature_identifier = feature.fully_qualified_identifier
        identifier = identifiers.FullyQualifiedCustomDataTypeIdentifier(
            **dataclasses.asdict(feature_identifier), custom_data_type=origin.identifier
        )

        if identifier in feature.data_type_definitions:
            return feature.data_type_definitions[identifier]

        docs = utils.parse_docs(inspect.getdoc(origin))
        fields = dataclasses.fields(origin)

        if len(fields) == 1 and utils.humanize(fields[0].name).replace(" ", "") == origin.identifier:
            data_type_definition = DataTypeDefinition(
                identifier=origin.identifier,
                display_name=origin.display_name,
                description=origin.description,
                fields_by_identifier={origin.identifier: fields[0].name},
                factory=type_hint,
                data_type=parse(fields[0].type, feature),
            )

            feature.add_data_type_definition(data_type_definition)
            return data_type_definition

        elements: list[sila.data_types.Structure.Element] = []
        fields_by_identifier: dict[str, str] = {}
        for index, field in enumerate(fields):
            field_display_name = utils.humanize(field.name)
            field_identifier = field_display_name.replace(" ", "")
            fields_by_identifier[field_identifier] = field.name
            elements.append(
                sila.data_types.Structure.Element(
                    identifier=field_identifier,
                    display_name=field_display_name,
                    description=docs.get("parameter", [])[index].get("default", ""),
                    data_type=parse(field.type, feature),
                )
            )

        data_type_definition = DataTypeDefinition(
            identifier=origin.identifier,
            display_name=origin.display_name,
            description=origin.description,
            fields_by_identifier=fields_by_identifier,
            factory=type_hint,
            data_type=sila.data_types.Structure(elements=elements),
        )
        feature.add_data_type_definition(data_type_definition)
        return data_type_definition
    if issubclass(origin, sila.data_types.DataType):
        return origin()
    if issubclass(origin, bool):
        return sila.data_types.Boolean()
    if issubclass(origin, int):
        return sila.data_types.Integer()
    if issubclass(origin, float):
        return sila.data_types.Real()
    if issubclass(origin, str):
        return sila.data_types.String()
    if issubclass(origin, bytes):
        return sila.data_types.Binary()
    if issubclass(origin, sila.datetime.date):
        return sila.data_types.Date()
    if issubclass(origin, sila.datetime.time):
        return sila.data_types.Time()
    if issubclass(origin, sila.datetime.datetime):
        return sila.data_types.Timestamp()
    if issubclass(origin, list):
        arg = typing.get_args(type_hint)
        if not arg:
            raise TypeError(f"Unable to identify SiLA type from annotation '{type_hint}'")

        return sila.data_types.List(data_type=parse(arg[0], feature))
    if issubclass(origin, typing.Annotated):
        args = typing.get_args(type_hint)
        return sila.data_types.Constrained(data_type=parse(args[0], feature), constraints=list(args[1:]))

    raise TypeError(f"Unable to identify SiLA type from annotation '{type_hint}'")

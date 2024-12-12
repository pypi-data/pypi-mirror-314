from __future__ import annotations

import dataclasses
import functools
import inspect

import sila.server as sila

from . import utils


@dataclasses.dataclass
class Feature(sila.Feature):
    def __init__(self, *args, identifier: str = "", display_name: str = "", description: str = "", **kwargs):
        display_name = display_name or utils.to_display_name(self.__class__.__name__)
        identifier = identifier or display_name.replace(" ", "")
        description = description or next((inspect.getdoc(cls) for cls in inspect.getmro(type(self))), "") or ""

        super().__init__(*args, identifier=identifier, display_name=display_name, description=description, **kwargs)

    def add_to_server(self, server: sila.Server) -> None:
        for cls in inspect.getmro(type(self)):
            for name, function in inspect.getmembers(cls, predicate=inspect.isfunction):
                if handler := getattr(function, "__handler", None):
                    implementation = getattr(self, name).__func__

                    implementation = functools.partial(implementation, self)
                    result = functools.wraps(function)(implementation)

                    handler.attach(self, result)

        super().add_to_server(server)

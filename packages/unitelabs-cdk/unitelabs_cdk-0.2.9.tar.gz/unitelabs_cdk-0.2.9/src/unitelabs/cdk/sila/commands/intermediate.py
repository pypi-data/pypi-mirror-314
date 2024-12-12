from __future__ import annotations

import typing
import weakref

from sila.commands import CommandExecution

T = typing.TypeVar("T")


class Intermediate(typing.Generic[T]):
    def __init__(self, command_execution: CommandExecution):
        self.command_execution: CommandExecution = weakref.proxy(command_execution)

    def send(self, value: T) -> None:
        self.command_execution.send_intermediate_responses(value)

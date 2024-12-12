from __future__ import annotations

import weakref

from sila import datetime
from sila.commands import CommandExecution


class Status:
    def __init__(self, command_execution: CommandExecution):
        self.command_execution: CommandExecution = weakref.proxy(command_execution)

    def update(
        self,
        progress: float | None = None,
        remaining_time: datetime.timedelta | None = None,
        updated_lifetime: datetime.timedelta | None = None,
    ) -> None:
        """Updates the execution status of an observable command execution"""
        self.command_execution.update_execution_info(
            progress_info=progress,
            estimated_remaining_time=remaining_time,
            updated_lifetime_of_execution=updated_lifetime,
        )

from __future__ import annotations

import asyncio
import dataclasses
import typing
import uuid

from sila import data_types, datetime, errors, identifiers

from .command_confirmation import CommandConfirmation
from .command_execution_info import CommandExecutionInfo, CommandExecutionStatus
from .command_execution_uuid import CommandExecutionUUID


@dataclasses.dataclass
class CommandExecution:
    identifier: identifiers.FullyQualifiedCommandIdentifier
    """The command's fully qualified identifier."""

    executable: typing.Callable
    """The function to call when the execution should run."""

    task: typing.Optional[asyncio.Task] = None

    command_execution_uuid: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    """A Command Execution UUID is the UUID of a Command execution."""

    command_execution_status: CommandExecutionStatus = CommandExecutionStatus.WAITING
    """The Command Execution Status provides details about the execution status of a Command."""

    _progress_info: float | None = None
    """Progress Info is the estimated progress of a Command execution, in percent (0...100%)."""

    _estimated_remaining_time: datetime.timedelta | None = None
    """Estimated Remaining Time is the estimated remaining execution time of a Command."""

    _lifetime_of_execution: datetime.timedelta | None = None
    """The Lifetime of Execution is the duration during which a Command Execution UUID is valid."""

    responses: bytes | None = dataclasses.field(init=False, default=None)
    """The tasks return value."""

    exception: errors.SiLAException | None = dataclasses.field(init=False, default=None)
    """The tasks return value."""

    def __post_init__(self):
        self.execution_info = asyncio.Event()
        self.intermediate_responses = asyncio.Queue()

    @property
    def command_confirmation(self) -> CommandConfirmation:
        """A command confirmation message is returned to identify the command execution."""
        return CommandConfirmation(
            command_execution_uuid=CommandExecutionUUID(value=self.command_execution_uuid),
            lifetime_of_execution=data_types.Duration.from_native(self._lifetime_of_execution)
            if self._lifetime_of_execution
            else None,
        )

    @property
    def command_execution_info(self) -> CommandExecutionInfo:
        """The Command Execution Info provides information about the current status of a Command being executed."""
        return CommandExecutionInfo(
            command_execution_status=self.command_execution_status,
            progress_info=data_types.Real.from_native(self._progress_info) if self._progress_info is not None else None,
            estimated_remaining_time=data_types.Duration.from_native(self._estimated_remaining_time)
            if self._estimated_remaining_time is not None
            else None,
            updated_lifetime_of_execution=data_types.Duration.from_native(self._lifetime_of_execution)
            if self._lifetime_of_execution is not None
            else None,
        )

    def run(self):
        self.task = asyncio.create_task(self.executable(command_execution=self))
        self.command_execution_status = CommandExecutionStatus.RUNNING

    def update_execution_info(
        self,
        progress_info: float | None = None,
        estimated_remaining_time: datetime.timedelta | None = None,
        updated_lifetime_of_execution: datetime.timedelta | None = None,
    ):
        self._progress_info = progress_info if progress_info is not None else self._progress_info
        self._estimated_remaining_time = (
            estimated_remaining_time if estimated_remaining_time is not None else self._estimated_remaining_time
        )
        self._lifetime_of_execution = (
            updated_lifetime_of_execution if updated_lifetime_of_execution is not None else self._lifetime_of_execution
        )
        self.execution_info.set()

    def send_intermediate_responses(self, intermediate_responses):
        self.intermediate_responses.put_nowait(intermediate_responses)

    def send_responses(self, responses: bytes):
        self.responses = responses
        self.command_execution_status = CommandExecutionStatus.FINISHED_SUCCESSFULLY
        self._progress_info = 1.0
        self._estimated_remaining_time = datetime.timedelta()
        self.execution_info.set()

    def raise_exception(self, exception: errors.SiLAException):
        self.exception = exception
        self.command_execution_status = CommandExecutionStatus.FINISHED_WITH_ERROR
        self._progress_info = 1.0
        self._estimated_remaining_time = datetime.timedelta()
        self.execution_info.set()

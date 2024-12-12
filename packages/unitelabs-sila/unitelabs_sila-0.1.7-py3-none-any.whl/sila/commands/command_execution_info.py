from __future__ import annotations

import dataclasses
import enum
import typing

from sila import data_types, protobuf


class CommandExecutionStatus(enum.IntEnum):
    """
    The Command Execution Status provides details about the execution status of a Command. It is either, and in this
    sequence, first "Command Waiting”, second "Command Running” and third "Command Finished Successfully” or "Command
    Finished With Error”. The Command Execution Status cannot be reverted back to a previous state that has already been
    left. That is, once the Command is running, the state cannot go back to waiting etc.
    """

    WAITING = 0
    RUNNING = 1
    FINISHED_SUCCESSFULLY = 2
    FINISHED_WITH_ERROR = 3


@dataclasses.dataclass
class CommandExecutionInfo(protobuf.BaseMessage):
    """
    The Command Execution Info provides information about the current status of a Command being executed. It consists of
    the Command Execution Status, and optionally the Progress Info and an Estimated Remaining Time. In addition, an
    updated Lifetime of Execution must be provided, if a Lifetime of Execution has been provided at Command initiation.
    """

    command_execution_status: typing.Annotated[CommandExecutionStatus, protobuf.Field(1)] = (
        CommandExecutionStatus.WAITING
    )
    """
    The Command Execution Status provides details about the execution status of a Command. It is either, and in this
    sequence, first "Command Waiting”, second "Command Running” and third "Command Finished Successfully” or "Command
    Finished With Error”. The Command Execution Status cannot be reverted back to a previous state that has already been
    left. That is, once the Command is running, the state cannot go back to waiting etc.
    """

    progress_info: typing.Annotated[typing.Optional[data_types.Real.Message], protobuf.Field(2)] = None
    """Progress Info is the estimated progress of a Command execution, in percent (0...100%)."""

    estimated_remaining_time: typing.Annotated[typing.Optional[data_types.Duration.Message], protobuf.Field(3)] = None
    """
    Estimated Remaining Time is the estimated remaining execution time of a Command.
    If the SiLA Server provides an updated Lifetime of Execution as part of the Command Execution Info, the updated
    lifetime must always result in an absolute lifetime that is equal to or greater than prior lifetimes reported. The
    absolute lifetime of a Command Execution UUID must never be reduced, but may be extended by any time.
    """

    updated_lifetime_of_execution: typing.Annotated[typing.Optional[data_types.Duration.Message], protobuf.Field(4)] = (
        None
    )
    """
    The Lifetime of Execution is the duration during which a Command Execution UUID is valid. The Lifetime of Execution
    is always a relative duration with respect to the point in time the SiLA Server initiated the response to the SiLA
    Client (the point in time when the SiLA Server returns the Command Execution UUID to the SiLA Client).
    """

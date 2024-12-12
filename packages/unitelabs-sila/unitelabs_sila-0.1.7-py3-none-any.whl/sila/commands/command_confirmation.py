from __future__ import annotations

import dataclasses
import typing

from sila import data_types, protobuf

from .command_execution_uuid import CommandExecutionUUID


@dataclasses.dataclass
class CommandConfirmation(protobuf.BaseMessage):
    """A command confirmation message is returned to identify the command execution."""

    command_execution_uuid: typing.Annotated[CommandExecutionUUID, protobuf.Field(1)] = dataclasses.field(
        default_factory=CommandExecutionUUID
    )
    """
    A Command Execution UUID is the UUID of a Command execution. It is unique within one instance of a SiLA Server and
    its lifetime (Lifetime of a SiLA Server).
    """

    lifetime_of_execution: typing.Annotated[typing.Optional[data_types.Duration.Message], protobuf.Field(2)] = None
    """
    The Lifetime of Execution is the duration during which a Command Execution UUID is valid. The Lifetime of Execution
    is always a relative duration with respect to the point in time the SiLA Server initiated the response to the SiLA
    Client (the point in time when the SiLA Server returns the Command Execution UUID to the SiLA Client).
    """

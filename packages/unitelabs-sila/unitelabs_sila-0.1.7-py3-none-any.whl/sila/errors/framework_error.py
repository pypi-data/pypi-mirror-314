from __future__ import annotations

import dataclasses
import enum
import typing

from sila import protobuf

from .sila_exception import SiLAException


class ErrorType(enum.IntEnum):
    """The following Framework Errors can occur:"""

    COMMAND_EXECUTION_NOT_ACCEPTED = 0
    """
    Is issued in case the SiLA server does not allow the command execution because it is occupied handling other command
    executions.
    """

    INVALID_COMMAND_EXECUTION_UUID = 1
    """
    Is issued when a SiLA client is trying to get or subscribe to command execution info, intermediate responses or
    responses of an observable command with an invalid command execution uuid.
    """

    COMMAND_EXECUTION_NOT_FINISHED = 2
    """
    Is issued when a SiLA client is trying to get the command response of an observable command when the command has not
    been finished yet.
    """

    INVALID_METADATA = 3
    """
    Is issued if a required SiLA client metadata has not been sent to the SiLA server or if the sent metadata has the
    wrong SiLA data type.
    """

    NO_METADATA_ALLOWED = 4
    """
    Is issued when the SiLA server receives a call of the SiLA service feature that contains SiLA client metadata.
    """


@dataclasses.dataclass
class FrameworkError(SiLAException, protobuf.BaseMessage):
    """
    A Framework Error is an error which occurs when a SiLA Client accesses a SiLA Server in a way that violates the SiLA
    2 specification. The Framework Error MUST include human readable information in the American English language (see
    Internationalization) about the error and SHOULD provide proposals for how to resolve the error.
    """

    Type: typing.ClassVar = ErrorType

    error_type: typing.Annotated[ErrorType, protobuf.Field(1)]
    """The Framework Error type."""

    message: typing.Annotated[str, protobuf.Field(2)]
    """
    Human readable information in the American English language about the error and proposals for how to resolve the
    error.
    """

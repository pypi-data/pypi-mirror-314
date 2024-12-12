from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .defined_execution_error import DefinedExecutionError
from .framework_error import FrameworkError
from .undefined_execution_error import UndefinedExecutionError
from .validation_error import ValidationError


@dataclasses.dataclass
class SiLAError(protobuf.BaseMessage):
    union: typing.ClassVar[protobuf.OneOf] = protobuf.OneOf()
    which_one = union.which_one_of_getter()

    validation_error: typing.Annotated[typing.Optional[ValidationError], protobuf.Field(1)] = None
    defined_execution_error: typing.Annotated[typing.Optional[DefinedExecutionError.Message], protobuf.Field(2)] = None
    undefined_execution_error: typing.Annotated[typing.Optional[UndefinedExecutionError], protobuf.Field(3)] = None
    framework_error: typing.Annotated[typing.Optional[FrameworkError], protobuf.Field(4)] = None

    @classmethod
    def from_exception(cls, exception: Exception) -> SiLAError:
        """Parses any exception into a SiLA Error"""
        if isinstance(exception, ValidationError):
            return SiLAError(validation_error=exception)
        if isinstance(exception, FrameworkError):
            return SiLAError(framework_error=exception)
        if isinstance(exception, DefinedExecutionError):
            return SiLAError(
                defined_execution_error=DefinedExecutionError.Message(
                    error_identifier=str(exception.fully_qualified_identifier),
                    message=exception.description,
                )
            )
        if isinstance(exception, UndefinedExecutionError):
            return SiLAError(undefined_execution_error=exception)

        return SiLAError(undefined_execution_error=UndefinedExecutionError(message=str(exception)))

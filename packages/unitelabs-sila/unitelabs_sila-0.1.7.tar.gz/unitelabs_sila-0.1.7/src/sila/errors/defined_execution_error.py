from __future__ import annotations

import dataclasses
import typing

from sila import identifiers, protobuf, validators

from .sila_exception import SiLAException

if typing.TYPE_CHECKING:
    from sila import core


@dataclasses.dataclass
class DefinedExecutionError(SiLAException):
    """
    A Defined Execution Error is an Execution Error that has been defined by the Feature Designer as part of the
    Feature. Defined Execution Errors enable the SiLA Client to react more specifically to an Execution Error, as the
    nature of the error as well as possible recovery procedures are known in better detail.

    Defined Execution Errors enable the Feature Designer to design error situations and allow the SiLA Client to
    implement situation specific and more explicit error handling routines.

    The Defined Execution Error MUST include its Fully Qualified Defined Execution Error Identifier, human readable
    information in the American English language (see Internationalization) about the error and SHOULD provide proposals
    for how to resolve the error.
    """

    identifier: validators.Identifier = validators.Identifier()

    display_name: validators.DisplayName = validators.DisplayName()

    description: str = dataclasses.field(default="")

    feature: core.Feature | None = dataclasses.field(repr=False, default=None)
    """The SiLA feature this error was registered with."""

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the Defined Execution Error."""

        error_identifier: typing.Annotated[str, protobuf.Field(1)]
        """
        The Fully Qualified Defined Execution Error Identifier of this SiLA Defined Execution Type.
        """

        message: typing.Annotated[str, protobuf.Field(2)]
        """
        Human readable information in the American English language about the error and proposals for how to resolve the
        error.
        """

    @property
    def fully_qualified_identifier(self) -> identifiers.FullyQualifiedDefinedExecutionErrorIdentifier:
        """
        The Fully Qualified Defined Execution Error Identifier of this SiLA Defined Execution Type.
        """
        if self.feature is None:
            raise UnboundLocalError()

        feature_identifier = self.feature.fully_qualified_identifier
        return identifiers.FullyQualifiedDefinedExecutionErrorIdentifier(
            **dataclasses.asdict(feature_identifier), defined_execution_error=self.identifier
        )

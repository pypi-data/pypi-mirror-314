from __future__ import annotations

import dataclasses
import typing

from sila import data_types, errors, identifiers, protobuf

if typing.TYPE_CHECKING:
    from sila import core


@dataclasses.dataclass
class Metadata:
    """
    SiLA Client Metadata is information that a SiLA Server expects to receive from a SiLA Client when executing a
    Command or reading or subscribing to a Property. If expected SiLA Client Metadata is not received, a Invalid
    Metadata Framework Error must be issued. This must be checked before parameter validation. Each SiLA Client Metadata
    has a specific Metadata Identifier and a SiLA Data Type. Metadata is intended for small pieces of data, and
    transmission might fail for values larger than 1 KB.
    """

    @dataclasses.dataclass
    class AffectedByResponse(protobuf.BaseMessage):
        affected_calls: typing.Annotated[list[data_types.String.Message], protobuf.Field(1)] = dataclasses.field(
            default_factory=list
        )

    identifier: str = dataclasses.field(default="")
    """
    A Metadata Identifier is the Identifier of a SiLA Client Metadata. A Metadata Identifier must be unique within the
    scope of a Feature. Uniqueness must be checked without taking lower and upper case into account.
    """

    display_name: str = dataclasses.field(default="")
    """A Metadata Display Name is the Display Name of a SiLA Client Metadata."""

    description: str = dataclasses.field(default="")
    """The Metadata Description is the Description of a SiLA Client Metadata."""

    data_type: dataclasses.InitVar[data_types.DataType] = data_types.Void()
    """A Metadata Data Type is the SiLA Data Type of a SiLA Client Metadata."""

    errors: list[errors.DefinedExecutionError] = dataclasses.field(repr=False, default_factory=list)

    feature: core.Feature | None = dataclasses.field(repr=False, default=None)
    """The SiLA feature this error was registered with."""

    def __post_init__(self, data_type: data_types.DataType):
        self.message = data_types.Structure(
            elements=[
                data_types.Structure.Element(
                    identifier=self.identifier,
                    display_name=self.display_name,
                    description=self.description,
                    data_type=data_type,
                )
            ]
        )

    @property
    def fully_qualified_identifier(self) -> identifiers.FullyQualifiedMetadataIdentifier:
        """
        The Fully Qualified Metadata Identifier of this SiLA Metadata.
        """
        if self.feature is None:
            raise UnboundLocalError()

        feature_identifier = self.feature.fully_qualified_identifier
        return identifiers.FullyQualifiedMetadataIdentifier(
            **dataclasses.asdict(feature_identifier), metadata=self.identifier
        )

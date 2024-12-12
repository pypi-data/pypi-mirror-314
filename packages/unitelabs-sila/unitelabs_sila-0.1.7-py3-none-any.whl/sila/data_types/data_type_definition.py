from __future__ import annotations

import dataclasses
import typing
import weakref

from sila import core, identifiers

from .data_type import DataType
from .structure import Structure
from .void import Void

if typing.TYPE_CHECKING:
    from sila.core.feature import Feature


@dataclasses.dataclass
class DataTypeDefinition(DataType[dict]):
    """Abstract base class for custom data types."""

    identifier: str = ""
    """Uniquely identifies the custom data type within the scope of the same feature."""

    display_name: str = dataclasses.field(repr=False, default="")
    """Human readable name of the custom data type."""

    description: str = dataclasses.field(repr=False, default="")
    """Describes the use and purpose of the custom data type."""

    data_type: dataclasses.InitVar[DataType] = Void()

    feature: core.Feature | None = dataclasses.field(repr=False, default=None)

    def __post_init__(self, data_type: DataType):
        self.message = Structure(
            elements=[
                Structure.Element(
                    identifier=self.identifier,
                    display_name=self.display_name,
                    description=self.description,
                    data_type=data_type,
                )
            ]
        )

    def encode(self, value: dict, field_number: int | None = None) -> bytes:
        if isinstance(self.message.elements[0].data_type, Structure):
            return self.message.elements[0].data_type.encode(value.get(self.identifier, None), field_number=1)

        return self.message.encode(value, field_number=None)

    def decode(self, data: bytes) -> dict:
        return self.message.decode(data)

    @property
    def fully_qualified_identifier(self) -> identifiers.FullyQualifiedCustomDataTypeIdentifier:
        """
        The Fully Qualified Custom Data Type Identifier of this SiLA Custom Data Type.
        """
        if self.feature is None:
            raise UnboundLocalError()

        feature_identifier = self.feature.fully_qualified_identifier
        return identifiers.FullyQualifiedCustomDataTypeIdentifier(
            **dataclasses.asdict(feature_identifier), custom_data_type=self.identifier
        )

    def add_to_feature(self, feature: Feature):
        """
        Registers this data type definition with a SiLA feature.

        Args:
            feature: The SiLA feature to add this data type definition to.
        """
        self.feature = weakref.proxy(feature)
        feature.data_type_definitions[self.fully_qualified_identifier] = self

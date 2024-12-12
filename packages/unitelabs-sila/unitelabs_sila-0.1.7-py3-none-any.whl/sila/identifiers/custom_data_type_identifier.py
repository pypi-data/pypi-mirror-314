from __future__ import annotations

import dataclasses

from sila import validators

from .feature_identifier import FullyQualifiedFeatureIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedCustomDataTypeIdentifier(FullyQualifiedFeatureIdentifier):
    """
    Uniquely identifies a custom data type among all potentially existing custom data types, e.g.
    `"org.silastandard/core/ErrorRecoveryService/v1/DataType/ContinuationOption"`
    """

    custom_data_type: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedCustomDataTypeIdentifier:
        feature_identifier, custom_data_type_identifier = identifier.split("/DataType/")
        feature = super().parse(identifier=feature_identifier)

        return FullyQualifiedCustomDataTypeIdentifier(
            **dataclasses.asdict(feature), custom_data_type=custom_data_type_identifier
        )

    def __repr__(self) -> str:
        return f"{super().__repr__()}/DataType/{self.custom_data_type}"

from __future__ import annotations

import dataclasses

from sila import validators

from .feature_identifier import FullyQualifiedFeatureIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedPropertyIdentifier(FullyQualifiedFeatureIdentifier):
    """
    Uniquely identifies a property among all potentially existing properties, e.g.
    `"org.silastandard/core/SiLAService/v1/Property/ServerUUID"`
    """

    property: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedPropertyIdentifier:
        feature_identifier, property_identifier = identifier.split("/Property/")
        feature = super().parse(identifier=feature_identifier)

        return FullyQualifiedPropertyIdentifier(**dataclasses.asdict(feature), property=property_identifier)

    def __repr__(self) -> str:
        return f"{super().__repr__()}/Property/{self.property}"

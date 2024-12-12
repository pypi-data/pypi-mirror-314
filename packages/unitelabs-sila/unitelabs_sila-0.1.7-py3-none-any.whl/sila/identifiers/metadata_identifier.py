from __future__ import annotations

import dataclasses

from sila import validators

from .feature_identifier import FullyQualifiedFeatureIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedMetadataIdentifier(FullyQualifiedFeatureIdentifier):
    """
    Uniquely identifies a metadata among all potentially existing metadata, e.g.
    `"org.silastandard/core/SiLAService/v1/Metadata/ServerUUID"`
    """

    metadata: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedMetadataIdentifier:
        feature_identifier, metadata_identifier = identifier.split("/Metadata/")
        feature = super().parse(identifier=feature_identifier)

        return FullyQualifiedMetadataIdentifier(**dataclasses.asdict(feature), metadata=metadata_identifier)

    def __repr__(self) -> str:
        return f"{super().__repr__()}/Metadata/{self.metadata}"

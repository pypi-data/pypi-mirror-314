from __future__ import annotations

import dataclasses

from sila import validators

from .feature_identifier import FullyQualifiedFeatureIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedCommandIdentifier(FullyQualifiedFeatureIdentifier):
    """
    Uniquely identifies a command among all potentially existing commands, e.g.
    `"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition"`
    """

    command: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedCommandIdentifier:
        feature_identifier, command_identifier = identifier.split("/Command/")
        feature = super().parse(identifier=feature_identifier)

        return FullyQualifiedCommandIdentifier(**dataclasses.asdict(feature), command=command_identifier)

    def __repr__(self) -> str:
        return f"{super().__repr__()}/Command/{self.command}"

from __future__ import annotations

import dataclasses

from sila import validators

from .command_identifier import FullyQualifiedCommandIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedCommandResponseIdentifier(FullyQualifiedCommandIdentifier):
    """
    Uniquely identifies a command response among all potentially existing command responses, e.g.
    `"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Response/FeatureDefinition"`
    """

    response: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedCommandResponseIdentifier:
        command_identifier, response_identifier = identifier.split("/Response/")
        command = super().parse(identifier=command_identifier)

        return FullyQualifiedCommandResponseIdentifier(**dataclasses.asdict(command), response=response_identifier)

    def __repr__(self) -> str:
        return f"{super().__repr__()}/Response/{self.response}"

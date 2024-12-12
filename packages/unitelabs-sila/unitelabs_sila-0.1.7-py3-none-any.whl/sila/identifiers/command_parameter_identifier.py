from __future__ import annotations

import dataclasses

from sila import validators

from .command_identifier import FullyQualifiedCommandIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedCommandParameterIdentifier(FullyQualifiedCommandIdentifier):
    """
    Uniquely identifies a command parameter among all potentially existing command parameters, e.g.
    `"org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"`
    """

    parameter: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedCommandParameterIdentifier:
        command_identifier, parameter_identifier = identifier.split("/Parameter/")
        command = super().parse(identifier=command_identifier)

        return FullyQualifiedCommandParameterIdentifier(**dataclasses.asdict(command), parameter=parameter_identifier)

    def __repr__(self) -> str:
        return f"{super().__repr__()}/Parameter/{self.parameter}"

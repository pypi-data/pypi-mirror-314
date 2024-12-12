from __future__ import annotations

import dataclasses

from sila import validators

from .command_identifier import FullyQualifiedCommandIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedIntermediateCommandResponseIdentifier(FullyQualifiedCommandIdentifier):
    """
    Uniquely identifies an intermediate command response among all potentially existing intermediate command responses,
    e.g. `"org.silastandard/test/ObservableCommandTest/v1/Command/Count/IntermediateResponse/CurrentIteration"`
    """

    intermediate_response: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedIntermediateCommandResponseIdentifier:
        command_identifier, intermediate_response_identifier = identifier.split("/IntermediateResponse/")
        command = super().parse(identifier=command_identifier)

        return FullyQualifiedIntermediateCommandResponseIdentifier(
            **dataclasses.asdict(command), intermediate_response=intermediate_response_identifier
        )

    def __repr__(self) -> str:
        return f"{super().__repr__()}/IntermediateResponse/{self.intermediate_response}"

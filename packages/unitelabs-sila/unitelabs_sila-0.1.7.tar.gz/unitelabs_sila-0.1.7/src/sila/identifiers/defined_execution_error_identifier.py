from __future__ import annotations

import dataclasses

from sila import validators

from .feature_identifier import FullyQualifiedFeatureIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedDefinedExecutionErrorIdentifier(FullyQualifiedFeatureIdentifier):
    """
    Uniquely identifies a defined execution error among all potentially existing defined execution errors, e.g.
    `"org.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature"`
    """

    defined_execution_error: validators.Identifier = validators.Identifier()

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedDefinedExecutionErrorIdentifier:
        feature_identifier, defined_execution_error_identifier = identifier.split("/DefinedExecutionError/")
        feature = super().parse(identifier=feature_identifier)

        return FullyQualifiedDefinedExecutionErrorIdentifier(
            **dataclasses.asdict(feature), defined_execution_error=defined_execution_error_identifier
        )

    def __repr__(self) -> str:
        return f"{super().__repr__()}/DefinedExecutionError/{self.defined_execution_error}"

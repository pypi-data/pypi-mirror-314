from __future__ import annotations

import dataclasses

from sila import validators

from .identifier import FullyQualifiedIdentifier


@dataclasses.dataclass(eq=False)
class FullyQualifiedFeatureIdentifier(FullyQualifiedIdentifier):
    """
    Uniquely identifies a feature among all potentially existing features, e.g. `"org.silastandard/core/SiLAService/v1"`
    """

    originator: validators.Domain = validators.Domain()
    category: validators.Domain = validators.Domain()
    feature: validators.Identifier = validators.Identifier()
    version: validators.Version = validators.Version(required=validators.Version.Level.MAJOR)

    def __post_init__(self):
        if len(str(self)) > 2048:
            raise ValueError("A fully qualified identifier must not exceed 2048 characters in length.")

    @classmethod
    def parse(cls, identifier: str) -> FullyQualifiedFeatureIdentifier:
        try:
            originator, category, feature, version, *_ = identifier.split("/")
        except AttributeError as error:
            raise ValueError("Received malformed identifier") from error

        if not version.startswith("v"):
            raise ValueError("Major version in fully qualified identifiers must be prefixed with 'v', e.g. 'v1'.")
        version = version[1:]

        return FullyQualifiedFeatureIdentifier(
            originator=originator, category=category, feature=feature, version=version
        )

    @property
    def feature_identifier(self) -> str:
        """The fully qualified feature identifier."""
        return f"{self.originator}/{self.category}/{self.feature}/v{self.version}"

    def __repr__(self) -> str:
        return self.feature_identifier

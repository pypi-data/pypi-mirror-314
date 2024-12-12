from __future__ import annotations

import abc
import dataclasses
import typing
import weakref

from sila import identifiers, validators

if typing.TYPE_CHECKING:
    from sila import errors

    from .feature import Feature


@dataclasses.dataclass
class Handler(abc.ABC):
    """Abstract base class for RPC handlers."""

    identifier: validators.Identifier = validators.Identifier()
    """Uniquely identifies the handler within the scope of the same feature."""

    display_name: validators.DisplayName = validators.DisplayName()
    """Human readable name of the handler."""

    description: str = dataclasses.field(repr=False, default="")
    """Describes the use and purpose of the handler."""

    observable: bool = dataclasses.field(repr=False, default=False)
    """Whether the handler returns an observable stream or just a single value."""

    errors: list[errors.DefinedExecutionError] = dataclasses.field(repr=False, default_factory=list)
    """
    A list of defined execution error identifiers referring to all the defined execution errors that can happen when
    accessing this handler.
    """

    feature: Feature | None = dataclasses.field(repr=False, default=None)
    """The SiLA feature this handler was registered with."""

    @property
    @abc.abstractmethod
    def fully_qualified_identifier(self) -> identifiers.FullyQualifiedIdentifier:
        """Universally uniquely identifies the handler."""

    def add_to_feature(self, feature: Feature) -> None:
        """
        Registers this property as handler with a SiLA feature.

        Parameters:
            feature: The SiLA feature to add this handler to.
        """
        self.feature = weakref.proxy(feature)

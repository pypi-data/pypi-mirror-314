from __future__ import annotations

import abc
import dataclasses
import typing
import weakref

from sila import core

if typing.TYPE_CHECKING:
    from .feature import Feature


@dataclasses.dataclass
class Handler(core.Handler, metaclass=abc.ABCMeta):
    """Abstract base class for RPC handlers."""

    feature: Feature | None = dataclasses.field(repr=False, default=None)
    """The SiLA feature this handler was registered with."""

    function: typing.Callable = dataclasses.field(repr=False, default=lambda: ...)
    """The implementation which is executed by the RPC handler."""

    def add_to_feature(self, feature: Feature) -> None:
        """
        Registers this property as RPC handler with a SiLA feature.

        Args:
            feature: The SiLA feature to add this property to.
        """
        self.feature = weakref.proxy(feature)

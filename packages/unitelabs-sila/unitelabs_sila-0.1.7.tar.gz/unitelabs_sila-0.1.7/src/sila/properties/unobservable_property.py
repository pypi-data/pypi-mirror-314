from __future__ import annotations

import dataclasses

from .property import Property


@dataclasses.dataclass
class UnobservableProperty(Property):
    """
    An unobservable property is a property that can be read at any time but no subscription mechanism is provided to
    observe its changes.
    """

    observable: bool = dataclasses.field(init=False, repr=False, default=False)

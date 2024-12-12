from __future__ import annotations

import dataclasses

from .property import Property


@dataclasses.dataclass
class ObservableProperty(Property):
    """
    An observable property is a property that can be read at any time and that offers a subscription mechanism to
    observe any change of its value.
    """

    observable: bool = dataclasses.field(init=False, repr=False, default=True)

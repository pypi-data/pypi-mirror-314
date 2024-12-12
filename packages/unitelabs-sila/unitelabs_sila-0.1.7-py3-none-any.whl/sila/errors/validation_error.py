from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .sila_exception import SiLAException


@dataclasses.dataclass
class ValidationError(SiLAException, protobuf.BaseMessage):
    """
    A Validation Error is an error that occurs during the validation of Parameters before executing a Command.

    Before executing a Command, a SiLA Server MUST validate all Parameters and MUST issue a Validation Error in case of
    invalid or missing Parameters. The Validation Error MUST include the Fully Qualified Command Parameter Identifier,
    human readable information in the American English language (see Internationalization) why the Parameter was invalid
    and SHOULD provide proposals for how to resolve the error (e.g. present a valid Parameter range to the user).
    """

    parameter: typing.Annotated[str, protobuf.Field(1)]
    """
    The Fully Qualified Command Parameter Identifier of the SiLA Parameter this Validation Error was associated with.
    """

    message: typing.Annotated[str, protobuf.Field(2)]
    """
    Human readable information in the American English language why the Parameter was invalid and proposals for how to 
    resolve the error (e.g. present a valid Parameter range to the user).
    """

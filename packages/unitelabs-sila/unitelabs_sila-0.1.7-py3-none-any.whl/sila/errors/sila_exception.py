from __future__ import annotations

import abc


class SiLAException(Exception, metaclass=abc.ABCMeta):
    """
    There are four types of errors that can happen when a SiLA client communicates with a SiLA server over a connection:
     - Validation Error
     - Execution Error
     - Framework Error
     - Connection Error

    All types of errors, except for the connection error are always issued by the SiLA server, but never by the SiLA
    client. The connection error is different, as it is not actively issued by the SiLA server nor the SiLA client, but
    by the underlying infrastructure (such as the communication network).
    """

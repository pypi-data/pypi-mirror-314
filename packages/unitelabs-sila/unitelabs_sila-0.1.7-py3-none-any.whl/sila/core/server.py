import dataclasses

from sila.validators import UUID, DisplayName, Identifier, Version


@dataclasses.dataclass
class Server:
    """
    A SiLA server is a system (a software system, a laboratory instrument, or device) that offers features to a SiLA
    client. Every SiLA server must implement the SiLA service feature.

    A SiLA server can either be a physical laboratory instrument (i.e. a spectrophotometer, a balance, a pH meter, ...)
    or a software system (i.e. a software system such as a Laboratory Information Management System - LIMS, a Laboratory
    Notebook - ELN, a Laboratory Execution System - LES, an Enterprise Resource Planning System - ERP, ...) that offers
    functionalities to a SiLA client. A SiLA server can offer a set of functionalities. All functionalities are
    specified and described by features.
    """

    uuid: UUID = UUID()
    """
    The SiLA server UUID is a UUID of a SiLA server. Each SiLA server must generate a UUID once, to uniquely identify
    itself. It needs to remain the same even after the lifetime of a SiLA server has ended.
    """

    type: Identifier = Identifier()
    """
    The SiLA server type is a human readable identifier of the SiLA server used to describe the entity that the SiLA
    server represents. For example, the make and model for a hardware device. A SiLA server type must comply with the
    rules for any identifier and start with an upper-case letter (A-Z) and may be continued by lower and upper-case
    letters (A-Z and a-z) and digits (0-9) up to a maximum of 255 characters in length.
    """

    name: DisplayName = DisplayName()
    """
    The SiLA server name is a human readable name of the SiLA server. By default this name should be equal to the SiLA
    server type. This property must be configurable via the SiLA service feature's “Set Server Name” command. This
    property has no uniqueness guarantee. A SiLA server name is the display name of a SiLA server (i.e. must comply with
    the rules for any display name, hence be a string of unicode characters of maximum 255 characters in length).
    """

    version: Version = Version(required=Version.Level.MINOR, optional=Version.Level.LABEL)
    """
    The SiLA server version is the version of the SiLA server. A "Major" and a "Minor" version number (e.g. 1.0) must be
    provided, a "Patch" version number may be provided. Optionally, an arbitrary text, separated by an underscore may be
    appended, e.g. “3.19.373_mighty_lab_devices”.
    """

    description: str = ""
    """
    The SiLA server description is the description of the SiLA server. It should include the use and purpose of this
    SiLA server.
    """

    vendor_url: str = ""
    """
    The SiLA server vendor URL is the URL to the website of the vendor or the website of the product of this SiLA
    server. This URL should be accessible at all times. The URL is a Uniform Resource Locator as defined in RFC 1738.
    """

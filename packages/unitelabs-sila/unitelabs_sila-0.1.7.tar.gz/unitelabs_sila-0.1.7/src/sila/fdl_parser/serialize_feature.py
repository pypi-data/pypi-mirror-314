import textwrap

from sila import core

from .serialize_command import serialize_command
from .serialize_data_type_definition import serialize_data_type_definition
from .serialize_defined_execution_error import serialize_defined_execution_error
from .serialize_description import serialize_description
from .serialize_metadata import serialize_metadata
from .serialize_property import serialize_property


def serialize_feature(feature: core.Feature) -> str:
    defined_execution_errors = {
        error.identifier: error
        for handler in list(feature.commands.values()) + list(feature.properties.values())
        for error in handler.errors
    }

    return (
        '<?xml version="1.0" encoding="utf-8" ?>\n'
        + f'<Feature Locale="{ feature.locale }" SiLA2Version="{feature.sila2_version}" FeatureVersion="{feature.version}" MaturityLevel="{feature.maturity_level}" Originator="{feature.originator}" Category="{feature.category}"\n'
        + '         xmlns="http://www.sila-standard.org"\n'
        + '         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
        + '         xsi:schemaLocation="http://www.sila-standard.org https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd">'
        + textwrap.indent(
            textwrap.dedent(
                f"""
                <Identifier>{ feature.identifier }</Identifier>
                <DisplayName>{ feature.display_name }</DisplayName>
                """
            )
            + serialize_description(feature.description)
            + "\n"
            + "\n".join(serialize_command(command) for command in feature.commands.values())
            + ("\n" if feature.commands else "")
            + "\n".join(serialize_property(property_) for property_ in feature.properties.values())
            + ("\n" if feature.properties else "")
            + "\n".join(serialize_metadata(metadata) for metadata in feature.metadata.values())
            + ("\n" if feature.metadata else "")
            + "\n".join(
                serialize_defined_execution_error(defined_execution_error)
                for defined_execution_error in defined_execution_errors.values()
            )
            + ("\n" if defined_execution_errors else "")
            + "\n".join(
                serialize_data_type_definition(data_type_definition)
                for data_type_definition in feature.data_type_definitions.values()
            ),
            "  ",
        )
        + "</Feature>"
    )

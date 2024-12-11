"""
Docstring parser.
"""

# Declare published functions and variables.
__all__ = ["parse_docstr", "DocStrInfo"]

# Import standard libraries.
import enum
import re

# For type hinting.
from collections.abc import Generator

# Import custom modules.
from .argopt import parse_arg, parse_opt
from .dtypes import DocStrInfo
from .usage  import parse_usg
from .utils  import match_and_get


class SectionType(enum.Enum):
    """
    Type of section in docstring.
    """
    UNKNOWN   = 0
    USAGES    = 1
    ARGUMENTS = 2
    OPTIONS   = 3


def split_section(docstr: str) -> Generator[tuple[str, str]]:
    """
    Parse docstring and split it to sections.

    Args:
        docstr (str): Input docstring.

    Returns:
        (tuple): A tuple of (section type, line).

    Examples:
        >>> list(split_section("Usage:\\n usage\\nArgs:\\n arg"))
        [(<SectionType.USAGES: 1>, ' usage'), (<SectionType.ARGUMENTS: 2>, ' arg')]
        >>> list(split_section("Usage:\\n usage\\nOpts:\\n --opt"))
        [(<SectionType.USAGES: 1>, ' usage'), (<SectionType.OPTIONS: 3>, ' --opt')]
    """
    section_patterns_and_indices = [
        # regular expression, (section_name_index, None)
        # ----------------------------------------------
        (r"^([\w ]+):\s*$",       (1,), None),  # SectionName:
        (r"^\[([\w ]+)\]\s*$",    (1,), None),  # [SectionName]
    ]

    section_name_patterns = {
        SectionType.USAGES   : ["usage"],
        SectionType.ARGUMENTS: ["args", "arguments"],
        SectionType.OPTIONS  : ["opts", "options"],
    }

    # Initialize the section type.
    current_sec_type = SectionType.UNKNOWN

    for line in docstr.split("\n"):

        # Try to match the section name patterns.
        sec_name, *_ = match_and_get(line.rstrip(), section_patterns_and_indices)

        # Case 1: New section found.
        if sec_name is not None:

            # Update the current section if matched to the section patterns.
            for sec_type, keywords in section_name_patterns.items():
                if any(sec_name.lower().endswith(keyword) for keyword in keywords):
                    current_sec_type = sec_type

        # Case 2: If not the beginning of section, try to match as section contents.
        elif re.match(r'^\s', line):
            yield (current_sec_type, line.rstrip())


def parse_docstr(docstr: str) -> DocStrInfo:
    """
    Parse the given docstring and create a data class.

    Args:
        docstr (str) : The target docstring.

    Returns:
        (tuple): A pair of DocStrInfo and usage descriptions.
    """
    # Initialize output variable.
    dsinfo = DocStrInfo(usgs=[], args=[], opts=[], utxt="Usage:")

    # Create a dictionary of parser function and list to be append.
    parsers_and_append_targets = {
        SectionType.USAGES   : (parse_usg, dsinfo.usgs),
        SectionType.ARGUMENTS: (parse_arg, dsinfo.args),
        SectionType.OPTIONS  : (parse_opt, dsinfo.opts),
    }

    # Parse each section.
    for sec_type, line in split_section(docstr):

        # Get corresponding parser function and target list.
        parser, target = parsers_and_append_targets[sec_type]

        # Parse the line and append to the target list.
        target.append(parser(line))

        # Append usage text.
        if sec_type == SectionType.USAGES:
            dsinfo.utxt += "\n" + line

    return dsinfo


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

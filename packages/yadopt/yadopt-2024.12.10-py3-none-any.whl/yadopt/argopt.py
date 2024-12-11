"""
Docstring parser.
"""

# Declare published functions and variables.
__all__ = ["parse_arg", "parse_opt"]

# Import standard libraries.
import re

# Import custom modules.
from .dtypes import ArgEntry, OptEntry
from .utils  import get_default, match_and_get
from .hints  import DTYPE_HINTS


def parse_arg(line: str) -> ArgEntry | OptEntry | None:
    """
    Parse an entry of argument section.
    Now `parse_opt` can manage both arguments and options.

    Examples:
        >>> parse_arg("  arg1 msg")
        ArgEntry(name='arg1', dtype_str=None, description='msg', default=None)
        >>> parse_arg("  arg1  (INT) msg  [default: 10]")
        ArgEntry(name='arg1', dtype_str='int', description='msg', default='10')
    """
    return parse_opt(line)


def parse_opt(line: str) -> ArgEntry | OptEntry | None:
    """
    Parse an entry of argument and option sections.

    Args:
        line (str): Input line.

    Returns:
        (ArgEntry | OptEntry | None): Parsed result.

    Examples:
        >>> parse_opt("  -o   msg")
        OptEntry(name='o', name_alt=None, has_value=False, dtype_str='bool', \
description='msg', default='False')
        >>> parse_opt("  --opt   msg")
        OptEntry(name='opt', name_alt=None, has_value=False, dtype_str='bool', \
description='msg', default='False')
        >>> parse_opt("  -o, --opt   msg")
        OptEntry(name='opt', name_alt='o', has_value=False, dtype_str='bool', \
description='msg', default='False')
        >>> parse_opt("  -o, --opt INT   msg")
        OptEntry(name='opt', name_alt='o', has_value=True, dtype_str='int', \
description='msg', default=None)
    """
    arg_patterns_and_indices = [
        # regular expression, (name,), None
        # ---------------------------------
        (r"\s+(\w+)", (1, ), None),
    ]
    opt_patterns_and_indices = [
        # regular expression,        (name, alt, value), has_value   # | type  | value  | delim |
        # ---------------------------------------------------------  # --------------------------
        (r"\s+-(\w+)=(\w+), --(\w+)=(\w+)", (3, 1,    2   ), True),  # | both  | double | equal |
        (r"\s+-(\w+) (\w+), --(\w+) (\w+)", (3, 1,    2   ), True),  # | both  | double | space |
        (r"\s+-(\w+), --(\w+)=(\w+)",       (2, 1,    3   ), True),  # | both  | single | equal |
        (r"\s+-(\w+), --(\w+) (\w+)",       (2, 1,    3   ), True),  # | both  | single | space |
        (r"\s+-(\w+), --(\w+)",             (2, 1,    None), False), # | both  | none   | -     |
        (r"\s+--(\w+)=(\w+)",               (1, None, 2   ), True),  # | long  | single | equal |
        (r"\s+--(\w+) (\w+)",               (1, None, 2   ), True),  # | long  | single | space |
        (r"\s+--(\w+)",                     (1, None, None), False), # | long  | none   | -     |
        (r"\s+-(\w+)=(\w+)",                (1, None, 2   ), True),  # | short | single | equal |
        (r"\s+-(\w+) (\w+)",                (1, None, 2   ), True),  # | short | single | space |
        (r"\s+-(\w+)",                      (1, None, None), False), # | short | none   | -     |
    ]

    # Try to parse as argument line.
    name, description, _ = match_and_get(line, arg_patterns_and_indices)

    if name is not None:

        # Get data type.
        dtype_str, description = get_dtype_str(name, description)

        # Get default value.
        description, default = get_default(description)

        return ArgEntry(name, dtype_str, description, default)

    # Try to parse as option line.
    name, name_alt, value, description, has_value = match_and_get(line, opt_patterns_and_indices)

    if name is not None:

        # Get data type.
        dtype_str, description = get_dtype_str(value, description)

        # Get default value.
        description, default = get_default(description)

        # If the option has no value (i.e. has_value is False),
        # then the data type and defualt value should be bool and False, respectively.
        if has_value is False:
            dtype_str, default = "bool", "False"

        return OptEntry(name, name_alt, has_value, dtype_str, description, default)

    return None


def get_dtype_str(var_name: str, description: str) -> tuple[type, str]:
    """
    Returns appropriate data type.

    Args:
        var_name (str): Variable name.

    Returns:
        (type): An appropriate Python data type.

    Examples:
        >>> get_dtype_str("x_int", "Integer value.")
        ('int', 'Integer value.')
        >>> get_dtype_str("x", "(INT) Integer value.")
        ('int', 'Integer value.')
    """
    # Try to get type from the description.
    if (m := re.match(r"^\s*\((\w+)\)\s*", description)) is not None:

        # Get matched data type name and description.
        dtype_str = m.group(1).strip().lower()
        description = description[len(m.group(0)):]

        # If the matched data type name is valid, then return them.
        if dtype_str in DTYPE_HINTS:
            return (dtype_str, description)

    # Returns None if variable name is None.
    if var_name is None:
        return (None, description)

    # Try to get type from the variable name.
    for key in DTYPE_HINTS:
        if var_name.lower().endswith(key):
            return (key, description)

    return (None, description)


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

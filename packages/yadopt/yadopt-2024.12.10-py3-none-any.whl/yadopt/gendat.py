"""
Generate YadoptArgument data class.
"""

# Declare published functions and variables.
__all__ = ["generate_data", "YadOptArgs"]

# Import standard libraries.
import copy

# Import custom modules.
from .dtypes import UserInput, YadOptArgs
from .docstr import DocStrInfo


def generate_data(user_input: UserInput, dsinfo: DocStrInfo, argv: list[str]) -> YadOptArgs:
    """
    Create YadOptArgs instance, fill the values, and return it.

    Args:
        user_input (UserInput) : Parsed user input.
        dsinfo     (DocStrInfo): Parsed docstring info.
        argv       (list[str]) : Argument vector.
    """
    # Create data instance.
    data = YadOptArgs()

    # Fill user input preceding values.
    for name, value in user_input.pres.items():
        setattr(data, name, bool(value))

    # Fill user input arguments and options.
    for name, value in (user_input.args | user_input.opts).items():
        setattr(data, name, value)

    # Append extra data.
    setattr(data, "_info_", copy.deepcopy(dsinfo))
    setattr(data, "_user_", copy.deepcopy(user_input))
    setattr(data, "_argv_", copy.deepcopy(argv))

    return data


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

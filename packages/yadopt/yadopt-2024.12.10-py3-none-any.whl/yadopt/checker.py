"""
Check argument vector based on the parsed arguments and options.
"""

# Declare published functions and variables.
__all__ = ["check_user_input"]

# Import custom modules.
from .docstr import DocStrInfo
from .argvec import UserInput
from .errors import YadOptError


def check_user_input(user_input: UserInput, docinfo: DocStrInfo) -> bool:
    """
    Check all user input variables are defined in arguments/options section.

    Args:
        user_input (UserInput) : User input info.
        docinfo    (DocStrInfo): Parse result of arguments/options section.

    Returns:
        (bool): Returns True if all checks are passed.
    """
    # Generate a set of all available argument names.
    available_args = {item.name for item in docinfo.args}

    # Generate a set of all available option names.
    available_opts  = {item.name     for item in docinfo.opts}
    available_opts |= {item.name_alt for item in docinfo.opts if item.name_alt is not None}

    # Check all user input is defined in argument sections.
    for name, value in user_input.args.items():
        if name not in available_args:
            raise YadOptError["usage_arg_mismatch"](name, value)

    # Check all user input is defined in option sections.
    for name, value in user_input.opts.items():
        if name not in available_opts:
            raise YadOptError["usage_arg_mismatch"](name, value)

    return True


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

"""
Assign types based on type hinting string.
"""

# Import standard libraries.
import ast
import pathlib

# For type hinting.
from collections.abc import Callable

# Import custom modules.
from .dtypes  import ArgEntry, OptEntry, DocStrInfo, UserInput
from .utils   import strtobool


DTYPE_HINTS = {"bool": strtobool, "boolean": strtobool,
               "int": int, "integer": int,
               "flt": float, "float": float,
               "str": str, "string": str,
               "path": pathlib.Path}


def fill_default_values(user_input: UserInput, dsinfo: DocStrInfo):
    """
    Fill default values.

    Args:
        user_input (UserInput) : Parsed user input.
        dsinfo     (DocStrInfo): Parsed docstring info.
    """
    for opt_entry in dsinfo.opts:
        if opt_entry.name not in user_input.opts:
            user_input.opts[opt_entry.name] = opt_entry.default

    return user_input


def type_hint(user_input: UserInput, dsinfo: DocStrInfo, type_func: Callable, fill_default: bool):
    """
    Apply type hints.

    Args:
        user_input (UserInput) : Parsed user input.
        dsinfo     (DocStrInfo): Parsed docstring info.
        type_func  (Callable)  : A function that assign types to values.
    """
    def autotype(value):
        """
        Automatically determine the data type.
        """
        try:
            return ast.literal_eval(value)
        except ValueError:
            return str(value)

    def set_typed_value(value_dict, list_entries: list[ArgEntry|OptEntry], type_func: Callable):
        """
        Get typed value.
        """
        for entry in list_entries:
            if entry.name in value_dict:

                # If the value is None, not necessary to assign type.
                if value_dict[entry.name] is None:
                    continue

                # Get type function.
                f = DTYPE_HINTS.get(entry.dtype_str, autotype) if type_func is None else type_func

                # If the target value is list of string, then apply the type function
                # to the list contents.
                if isinstance(value_dict[entry.name], list):
                    value_dict[entry.name] = [f(v) for v in value_dict[entry.name]]

                # Else, normaly apply type function to the value.
                else:
                    value_dict[entry.name] = f(value_dict[entry.name])

    # Fill deafult values to the user input.
    if fill_default:
        fill_default_values(user_input, dsinfo)

    # Assign type to the values.
    set_typed_value(user_input.args, dsinfo.args, type_func)
    set_typed_value(user_input.opts, dsinfo.opts, type_func)


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

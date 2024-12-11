"""
Collections of data types and classes.
"""

# Declare published functions and variables.
__all__ = ["ArgEntry", "OptEntry", "UsgEntry", "UserInput", "DocStrInfo"]

# Import standard libraries.
import dataclasses


############################################################
# Data types for parsing docstring
############################################################

@dataclasses.dataclass
class ArgEntry:
    """
    Parsed result of argument definition in docstring.
    """
    name       : str         # Option name.
    dtype_str  : str         # Data type string.
    description: str         # Description of this option.
    default    : str | None  # Default value (string).

@dataclasses.dataclass
class OptEntry:
    """
    Parsed result of option definition in docstring.
    """
    name       : str         # Option name.
    name_alt   : str         # Alternative option name.
    has_value  : bool        # Number of arguments.
    dtype_str  : str         # Data type string.
    description: str         # Description of this option.
    default    : str | None  # Default value (string).

@dataclasses.dataclass
class UsgEntry:
    """
    Parsed result of usage definition in docstring.
    """
    pres: list[str]                     # Preceding tokens.
    args: list[str]                     # Argument tokens.
    opts: dict[str, tuple[bool, bool]]  # Option tokens: name -> (has_value, is_mandatory).

@dataclasses.dataclass
class DocStrInfo:
    """
    Parse result of docstring.
    """
    usgs: list[UsgEntry]  # Information of usages.
    args: list[ArgEntry]  # Information of argument.
    opts: list[OptEntry]  # Information of option.
    utxt: str             # Usage raw text.


############################################################
# Data types for parsing user inputs
############################################################

@dataclasses.dataclass
class UserInput:
    """
    Information of user input.
    """
    pres: dict  # Preceding tokens.
    args: dict  # Argument tokens.
    opts: dict  # Option tokens.


############################################################
# A class to store parsed results
############################################################

class YadOptArgs:
    """
    Command line arguments parsed by YadOpt.
    """
    def __init__(self, args_dict=None):
        """
        Constructor.
        """
        if args_dict is not None:
            for key, value in args_dict.items():
                setattr(self, key, value)

    @property
    def __normal_dict__(self):
        """
        Returns "normal" dictionary that contains keys not starting with the underscore.
        """
        return {key:value for key, value in self.__dict__.items() if not key.startswith("_")}

    def __repr__(self):
        """
        Representation of this class.
        """
        contents = ", ".join(f"{key}={val}" for key, val in self.__normal_dict__.items())
        return f"{self.__class__.__name__}({contents})"

    def __str__(self):
        """
        String expression of this class.
        """
        return self.__repr__()

    def __eq__(self, other):
        """
        Returns True if equivarent.
        """
        return self.__normal_dict__ == other.__normal_dict__


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

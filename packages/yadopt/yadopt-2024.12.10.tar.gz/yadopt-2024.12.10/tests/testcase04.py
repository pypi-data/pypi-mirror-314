"""
Testcase 4: error check - usage and arguments not match
"""

# Import standard libraries.
import os
import pathlib
import sys
import traceback


docstring = """
Usage:
    sample.py <arg_mistake> [-a NAME]

Arguments:
    arg       Input argument.

Options:
    -a name   Option with value.
"""

commands = [
    "sample.py arg -a val",
]


def check(index, args, command):
    """
    Checker function for testcases.

    Args:
        index   (int)       : Index of testcases.
        args    (YadOptArgs): Parsed command line arguments.
        command (str)       : Command string (source of `args`).
    """
    raise NotImplementedError("This function cannot be called")


def check_error(index, error):
    """
    Checker function for error object caused in testcases.

    Args:
        index (int)      : Index of testcases.
        error (Exception): Cathed error object.
    """
    print("  ->", type(error))
    assert error.__class__.__name__ == "YadOptErrorUsageArgMismatch"
    assert str(error).strip().startswith("Error summary:\n  ")


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

"""
Testcase 13: error check - usage parse
"""

# Import standard libraries.
import os
import pathlib
import sys
import traceback


docstring = """
Usage:
    sample.py --opt VALUE
    sample.py --help

Options:
    --opt VALUE    Option with value.
    -h, --help     Show this help message and exit.
"""

commands = [
    "sample.py --opt value",
    "sample.py --help",
]


def check(index, args, command):
    """
    Checker function for testcases.

    Args:
        index   (int)       : Index of testcases.
        args    (YadOptArgs): Parsed command line arguments.
        command (str)       : Command string (source of `args`).
    """
    print("  ->", args)

    if index == 0:
        assert args.opt == "value"

    elif index == 1:
        assert args is None

    else:
        raise ValueError(f"Check function for index={index} not found")


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

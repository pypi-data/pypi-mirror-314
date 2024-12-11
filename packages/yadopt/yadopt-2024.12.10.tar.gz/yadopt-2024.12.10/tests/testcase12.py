"""
Testcase 12: error check - usage parse
"""

# Import standard libraries.
import os
import pathlib
import sys
import traceback


docstring = """
Usage:
    cmd <config_path>
    cmd --help

Arguments:
    config_path    Path to config

Other options:
    -h, --help     Show this help message and exit.
"""

commands = [
    "sample.py",
    "sample.py file.txt",
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
        assert args is None

    elif index == 1:
        assert args.config_path == pathlib.Path("file.txt")

    elif index == 2:
        assert args is None

    else:
        raise ValueError(f"Check function for index={index} not found")


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

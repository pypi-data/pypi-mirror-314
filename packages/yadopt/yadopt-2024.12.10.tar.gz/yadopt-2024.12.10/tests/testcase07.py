"""
Testcase 7: error check - user input not match
"""

# Import standard libraries.
import os
import pathlib
import sys
import traceback


docstring = """
Usage:
    sample.py subcmd <arg>

Arguments:
    arg    Input argument.
"""

commands = [
    "sample.py cmdsub argument",
]


def check(index, args, command):
    """
    Checker function for testcases.

    Args:
        index   (int)       : Index of testcases.
        args    (YadOptArgs): Parsed command line arguments.
        command (str)       : Command string (source of `args`).
    """
    if index == 0:
        assert args is None


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

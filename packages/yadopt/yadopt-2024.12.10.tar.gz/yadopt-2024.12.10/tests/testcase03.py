"""
Testcase 3: data type hints
"""

# Import standard libraries.
import os
import pathlib


docstring = """
Testcase 03: test data types.

Usage:
    sample.py <arg> [-a NAME]
    sample.py <arg_bool> <arg_boolean> [-b NAME_BOOL] [-c NAME_BOOLEAN]
    sample.py <arg_int> <arg_integer> <arg_path> [-d NAME_INT] [-e NAME_INTEGER] [-f NAME_PATH]
    sample.py <arg_flt> <arg_float> <arg_str> <arg_string> [-g NAME_FLT] [-h NAME_FLOAT] [-i NAME_STR] [-j NAME_STRING]

Arguments:
    arg           No type specification means string.
    arg_bool      Boolean option value.
    arg_boolean   Boolean option value.
    arg_int       Integer option value.
    arg_integer   Integer option value.
    arg_path      Path option value.
    arg_flt       Float option value.
    arg_float     Float option value.
    arg_str       String option value.
    arg_string    String option value.

Options:
    -a name           No type specification means string.
    -b name_bool      Boolean option value.
    -c name_boolean   Boolean option value.
    -d name_int       Integer option value.
    -e name_integer   Integer option value.
    -f name_path      Path option value.
    -g name_flt       Float option value.
    -h name_float     Float option value.
    -i name_str       String option value.
    -j name_string    String option value.
"""

commands = [
    "sample.py arg -a val",
    "sample.py True False -b true -c false",
    "sample.py 12 345 /tmp -d 67 -e 890 -f /home",
    "sample.py 3.1415 2.7183 hoge fuga -g 0.1 -h 1.0 -i foo -j bar",
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
        assert isinstance(args.arg, str)
        assert isinstance(args.a, str)

    elif index == 1:
        assert isinstance(args.arg_bool, bool)
        assert isinstance(args.arg_boolean, bool)
        assert isinstance(args.b, bool)
        assert isinstance(args.c, bool)

    elif index == 2:
        assert isinstance(args.arg_int, int)
        assert isinstance(args.arg_integer, int)
        assert isinstance(args.arg_path, pathlib.Path)
        assert isinstance(args.d, int)
        assert isinstance(args.e, int)
        assert isinstance(args.f, pathlib.Path)

    elif index == 3:
        assert isinstance(args.arg_flt, float)
        assert isinstance(args.arg_float, float)
        assert isinstance(args.arg_str, str)
        assert isinstance(args.arg_string, str)
        assert isinstance(args.g, float)
        assert isinstance(args.h, float)
        assert isinstance(args.i, str)
        assert isinstance(args.j, str)

    else:
        print(f"No assertion defined for the {index}-th test")
        print(f"  -> {command}")
        exit(os.EX_DATAERR)


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

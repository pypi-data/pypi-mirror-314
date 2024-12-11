"""
Run all test at once.
"""

# Import standard libraries.
import importlib
import pathlib
import shlex
import sys

# Import Yadopt.
sys.path.append(".")
import yadopt


# Define color code.
COLOR_GREEN  = "\x1b[32m"
COLOR_YELLOW = "\x1b[33m"
COLOR_NONE   = "\x1b[0m"


def main():
    """
    Main function of test.
    """
    print(f"{COLOR_YELLOW}Starts the tests...{COLOR_NONE}")
    print()

    # Run unittests.
    print(f"----- Test: run_all_unittests -----")
    unit_test = importlib.import_module("unit_test")
    unit_test.run_all_unittests()
    print(f"{COLOR_GREEN}Passed{COLOR_NONE}")
    print(f"-----------------------------------")
    print()

    # Run all test cases.
    for path_py in sorted(pathlib.Path(__file__).parent.glob("testcase??.py")):

        # Get the module name.
        module_name = path_py.with_suffix("").name

        # Import testcase module.
        testcase = importlib.import_module(module_name)

        for idx, command in enumerate(testcase.commands):

            print(f"----- Test: {module_name}.{idx} -----")

            # Run the testcase.
            try:
                args = yadopt.parse(testcase.docstring, shlex.split(command), force_continue=True)
            except Exception as error:
                testcase.check_error(idx, error)
            else:
                testcase.check(idx, args, command)

            print(f"{COLOR_GREEN}Passed{COLOR_NONE}")
            print(f"------------------------------")
            print()

    # Test wrap function.
    print(f"----- Test: testcase_wrap -----")
    testcase = importlib.import_module("testcase_wrap")
    testcase.test()
    print(f"{COLOR_GREEN}Passed{COLOR_NONE}")
    print(f"-------------------------------")
    print()


if __name__ == "__main__":
    main()


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

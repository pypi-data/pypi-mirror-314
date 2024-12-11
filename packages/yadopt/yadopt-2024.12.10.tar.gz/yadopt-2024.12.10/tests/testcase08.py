"""
Testcase 7: data type on the description head
"""

# Import standard libraries.
import os
import pathlib
import sys
import traceback


docstring = """
Usage:
    train.py <config> [--epochs EPOCHS] [--model MODEL] [--lr LR] [--output OUTPUT] [--verbose]
    train.py --help

Train a neural network model.

Arguments:
    config           (path)   Path to config file.

Training options:
    --epochs EPOCHS  (int)    The number of training epochs.   [default: 100]
    --model MODEL    (str)    Neural network model name.       [default: mlp]
    --lr LR          (float)  Learning rate.                   [default: 1.0E-3]

Output options:
    --output OUTPUT  (path)   Path to output directory.        [default: runs]

Other options:
    -v, --verbose    (bool)   Enables verbose output.
    -h, --help       (bool)   Show this help message and exit.
"""

commands = [
    "train.py config.toml --epochs 10 --model=cnn",
    "train.py config.toml -v",
    "train.py --help",
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
        assert args.config == pathlib.Path("config.toml")
        assert args.epochs == 10
        assert args.model == "cnn"
        assert abs(args.lr - 1.0E-3) < 1.0E-8
        assert args.output == pathlib.Path("runs")
        assert args.help == False
        assert args.verbose == False

    elif index == 1:
        assert args.config == pathlib.Path("config.toml")
        assert args.epochs == 100
        assert args.model == "mlp"
        assert abs(args.lr - 1.0E-3) < 1.0E-8
        assert args.output == pathlib.Path("runs")
        assert args.help == False
        assert args.verbose == True

    elif index == 2:
        assert args is None

    else:
        raise ValueError(f"Check function for index={index} not found")


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

"""
Usage line parser.
"""

# Declare published functins and variables.
__all__ = ["parse_usg"]

# Import standard libraries.
import copy
import re

# For type hinting.
from collections.abc import Generator

# Import custom modules.
from .dtypes import UsgEntry, UserInput
from .errors import YadOptError


def parse_usg(line: str) -> UsgEntry:
    """
    Parse usage line.

    Args:
        line (str): Input usage string.

    Examples:
        >>> parse_usg("sample.py <arg1> <arg2> [--opt1]")
        UsgEntry(pres=['sample.py'], args=['arg1', 'arg2'], opts={'opt1': (False, False)})
        >>> parse_usg("sample.py subcmd <arg1> [--opt1 INT]")
        UsgEntry(pres=['sample.py', 'subcmd'], args=['arg1'], opts={'opt1': (True, False)})
        >>> parse_usg("sample.py subcmd <arg1> --opt1")
        UsgEntry(pres=['sample.py', 'subcmd'], args=['arg1'], opts={'opt1': (False, True)})
    """
    def is_arg(token):
        return token.startswith("<") and token.endswith(">")

    def is_opt(token):
        return token.strip("[]").startswith("-") or (token == "[OPTIONS]")

    # Initialize output variable.
    usage = UsgEntry(pres=[], args=[], opts={})

    # Tokenize usage string.
    tokens = list(tokenize(line))

    # Extract preceding tokens until arguments or options appears.
    while tokens and (not is_arg(tokens[0])) and (not is_opt(tokens[0])):
        usage.pres.append(tokens.pop(0))

    # Process arguments and options.
    while tokens:

        # Get the first token.
        token = tokens.pop(0)

        # Case 1: Argument token.
        if token.startswith("<") and token.endswith(">"):
            usage.args.append(token.strip("<>"))

        # Case 2: Mandatory option token.
        elif token.startswith("-"):

            # Get the option name.
            opt_key = token.lstrip("-")

            # Case 2.1: Option with value.
            if tokens and all(not tokens[0].startswith(s) for s in ["<", "[", "-"]):

                # Get the option value (but not used now).
                _ = tokens.pop(0)

                # Add option entry.
                usage.opts[opt_key] = (True, True)

            # Case 2.2: Option without value.
            else:
                usage.opts[opt_key] = (False, True)

        # Case 3: Non-mandatory option token.
        elif (token.startswith("[-") and token.endswith("]")) or (token == "[OPTIONS]"):

            # Split option name and value (i.e. split by " " or "=").
            subtokens = re.split("[ =]", token.strip("[]").lstrip("-"), maxsplit=1)

            # Add option entry.
            usage.opts[subtokens[0]] = (len(subtokens) > 1, False)

        else:
            raise YadOptError["invalid_constant"](token, line)

    return usage


def tokenize(usage_line: str) -> Generator[str]:
    """
    Tokenize usage line. This function is focusing on the tokenization of usage pattern.
    If you prefer simple tokenization, use `shlex.split` function.

    Args:
        usage_line (str) : Usage string.
        strip      (bool): Strip whitespace from returned tokens if true.

    Examples:
        >>> list(tokenize("sample.py <arg1> [--opt1]"))
        ['sample.py', '<arg1>', '[--opt1]']
        >>> list(tokenize("sample.py --opt1 --opt2 val2"))
        ['sample.py', '--opt1', '--opt2', 'val2']
        >>> list(tokenize("sample.py subcmd <arg1> <arg2> [--opt1] [--opt2 val2]"))
        ['sample.py', 'subcmd', '<arg1>', '<arg2>', '[--opt1]', '[--opt2 val2]']
    """
    token_patterns = [
        r"\s+",                     # Whitespace
        r"[\w\.-]+",                # Preceding token
        r"<\w+>",                   # Argument token
        r"<\w+\.\.\.>",             # Argument token
        r"\[[\w\.-]+\]",            # Optional token
        r"\[[\w\.-]+ [\w\.-]+\]",   # Optional token with value (space)
        r"\[[\w\.-]+=[\w\.-]+\]",   # Optional token with value (equal)
    ]

    # Copy the input usage string for safety.
    usage_line = copy.deepcopy(usage_line)

    while usage_line:

        # Find matched patterns.
        for pattern in token_patterns:
            if (m := re.match(pattern, usage_line)) is not None:
                break

        # Raise an error if no pattern matched.
        if m is None:
            raise YadOptError["usage_parse"](usage_line)

        # Get matched substring.
        token = m.group(0)

        # Returns token as generator.
        if token.strip():
            yield token.strip()

        # Remove the returned token.
        usage_line = usage_line[len(token):]


def match_argvec_and_usage(argv: list[str], usage: UsgEntry) -> UserInput:
    """
    Try to match the given argument vector and usage pattern.
    If matched, returns UserInput instance, and otherwise, returns None.

    Args:
        argv  (list[str]): Argument vector.
        usage (UsgEntry) : Usage pattern.

    Returns:
        (UserInput): UserInput instance if matched, and None otherwise.
    """
    # Copy the input argment vector for safety.
    argv = copy.deepcopy(argv)

    # Initialize the output dictionary.
    user_input = UserInput(pres={}, args={}, opts={})

    # Check preceding strings. It's convenient for users to ignore the first
    # preceding argument, which is often the name of the called Python script.
    for idx, token in enumerate(usage.pres[1:], start=1):

        # Return None if preceding token does not match.
        if (len(argv) <= idx) or (argv[idx] != token):
            return None

        user_input.pres[token] = True

    # Drop the preceding tokens from the argument vector.
    argv = argv[len(usage.pres):]

    # Make a copy of available argument names.
    available_args = copy.deepcopy(usage.args)

    while argv:

        # Get next token.
        token = argv.pop(0)

        # Case 1: Option token.
        if token.startswith("-"):
            is_matched = proc_opt_token(token, argv, user_input, usage)

        # Case 2: Argument token.
        else:
            is_matched = proc_arg_token(token, user_input, available_args)

        # Return None if not matched.
        if not is_matched:
            return None

    # If unused arguments remaining, that means the usage does not match.
    if any(not arg.endswith("...") for arg in available_args):
        return None

    # If any of the required options are missing, that means the usage does not match.
    if not all(name in user_input.opts for name, (_, is_mand) in usage.opts.items() if is_mand):
        return None

    return user_input


def proc_arg_token(token: str, user_input: UserInput, available_args: list[str]) -> bool:
    """
    Process argument token.

    Args:
        token          (str)      : Input token.
        user_input     (UserInput): User input instance.
        available_args (list[str]): Rest of available arguments.
    """
    # NOT MATRCHED!: too many arguments.
    if not available_args:
        return False

    # Case 2.1: multiple arguments.
    if available_args[0].endswith("..."):

        # Get argument name.
        target_arg = available_args[0].rstrip(".")

        # Create a list.
        if target_arg not in user_input.args:
            user_input.args[target_arg] = []

        # Append the token to the list.
        user_input.args[target_arg].append(token)

    # Case 2.2: single arguments.
    else:
        user_input.args[available_args.pop(0)] = token

    return True


def proc_opt_token(token: str, argv: list[str], user_input: UserInput, usage: UsgEntry) -> bool:
    """
    Process option token.

    Args:
        token      (str)       : Input token.
        argv       (list[str]) : Argument vector.
        user_input (UserInput) : User input instance.
        usage      (UsageEntry): Usage pattern.
    """
    # Remove hyphens.
    token = token.lstrip("-")

    # NOT MATRCHED!: unknown option.
    if token not in usage.opts:
        return False

    # Get the properties of the target option.
    has_value, _ = usage.opts[token]

    # Case 1.1: Option with value.
    if has_value:

        # NOT MATRCHED!: option value not found: there is no remaining token.
        if not argv:
            return False

        # Get option value.
        token_value = argv.pop(0)

        # NOT MATRCHED!: option value not found: seems like option token.
        if token_value.startswith("-"):
            return False

        # Add {option_name: token_value} to the option dictionary of the user input.
        user_input.opts |= {token: token_value}

    # Case 1.2: Option without value.
    else:

        # Add {option_name: "True"} to the option dictionary of the user input.
        user_input.opts |= {token: "True"}

    return True


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

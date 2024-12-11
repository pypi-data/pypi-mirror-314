"""
Collection of utility functions.
"""

# Import standard libraries.
import re

# For type hinting.
from collections.abc import Generator


def get_default(description: str) -> tuple:
    """
    Get default value.

    Args:
        description (str): Description message contains default value.

    Returns:
        (tuple): A tuple of (rest of description, default value string).

    Examples:
        >>> get_default("sample description [default: value]")
        ('sample description', 'value')
    """
    default_pattern = r"^(.*)\s+\[default:\s*([^\]]+)\]\s*$"

    # Search default string.
    m = re.fullmatch(default_pattern, description)

    # Returns entire description and None if no default string found.
    if m is None:
        return (description.strip(), None)

    # Otherwise, returns rest of descriptions and default string.
    return (m.group(1).strip(), m.group(2).strip())


def get_error_marker(line: str, token: str) -> str:
    """
    Args:
        line  (str): Entire line.
        token (str): Target token.

    Returns:
        (str): Error marker string like.

    Examples:
        >>> get_error_marker("this is a pen", "pen")
        '          ^^^'
        >>> get_error_marker("this is a pen", "pencil")
        '             '
    """
    pos = line.find(token)

    # Returns whitespace if the token not found in the line.
    if pos < 0:
        return " " * len(line)

    return " " * pos + "^" * len(token) + " " * (len(line) - len(token) - pos)


def match_and_get(line: str, patterns_and_indices: list) -> tuple[str]:
    """
    Parse the given string and returns specified matched strings.

    Args:
        line                 (str) : The target line.
        patterns_and_indices (list): A list of patterns and indices.

    Returns:
        (tuple[str]): A tuple of matched strings corresponding to the indices,
                      and the rest of matched strings.

    Examples:
        >>> match_and_get("-h, --help", [(r"-(\\w+), --(\\w+)", (2, 1), None)])
        ('help', 'h', '', None)
    """
    # Get the number of indices for each pattern.
    n_indices = len(patterns_and_indices[0][1])

    for pattern, indices, optional_value in patterns_and_indices:

        # Compute regular expression match, and continue the loop if not matched.
        if (m := re.match(pattern, line, re.ASCII)) is None:
            continue

        # Get the required matched strings.
        output = [None if idx is None else m[idx] for idx in indices]

        # Get the rest of the matched strings.
        output.append(line[len(m.group(0)):])

        # Append the optional value.
        output.append(optional_value)

        return tuple(output)

    return tuple([None] * (n_indices + 2))


def remove_indent(text: str) -> str:
    """
    Remove common indent from the given text.

    Args:
        text (str): Input text.

    Returns:
        (str): Text after removing the common indent.

    Examples:
        >>> remove_indent("  A\\n  B\\n  C")
        'A\\nB\\nC'
    """
    # Get non-empty lines.
    lines = [line for line in text.split("\n") if line.strip()]

    # Compute minimum indent of the non-empty lines.
    min_indent = min(len(line) - len(line.lstrip()) for line in lines)

    return "\n".join(line[min_indent:] for line in text.split("\n"))


def strtobool(s: str) -> bool:
    """
    Convert the given string to bool instance. The function `bool(...)` is not suitable
    for this purpose, because `bool("False")` returns `True`.

    Args:
        s (str): Input string.

    Returns:
        (bool): Corresponding boolean value.
    """
    if s.lower() in {"t", "true", "y", "yes", "on", "1"}:
        return True
    if s.lower() in {"f", "false", "n", "no", "off", "0"}:
        return False
    return None


def retokenize(argv: list[str]) -> Generator[str]:
    """
    Tokenize the argument vector.

    Args:
        target (str): Target string to be tokenized.

    Returns:
        (Generator[str]): Re-tokenized tokens.

    Examples:
        >>> list(retokenize(["A=a", "B=b"]))
        ['A', 'a', 'B', 'b']
    """
    for token in argv:
        yield from token.split("=", maxsplit=1)


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

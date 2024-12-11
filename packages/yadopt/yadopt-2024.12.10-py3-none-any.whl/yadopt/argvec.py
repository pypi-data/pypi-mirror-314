"""
Argment vector parsers.
"""

# Declare published functins and variables.
__all__ = ["parse_argvec"]

# Import custom modules.
from .dtypes import DocStrInfo, UserInput
from .usage  import match_argvec_and_usage


def parse_argvec(argv: list[str], dsinfo: DocStrInfo) -> UserInput:
    """
    Try to match with the given arguemtn vector and usage patterns.
    If matched usage found, this function returns a dictionary that represents name-value
    correspondance. Otherwise, returns None.

    Args:
        argv   (list[str]) : Argument vector.
        dsinfo (DocStrInfo): Parsed result of docstring.

    Returns:
        (UserInput): Correspondance of argument/option names and values.
    """
    def standerdize_option_names_in_argument_vector(argv, alt_names):
        """
        Standardize option names of argument vector.
        For example, "-h" -> "--help".
        """
        # Standardize option names of argument vector.
        for idx, (prefix, key) in enumerate((token[0], token[1:]) for token in argv):
            yield f"--{alt_names[key]}" if (prefix == "-") and (key in alt_names) else argv[idx]

    # Get a map from altanative name to standard name.
    alt_names = {item.name_alt:item.name for item in dsinfo.opts if item.name_alt is not None}

    # Standardize option names of argument vector.
    argv_std = list(standerdize_option_names_in_argument_vector(argv, alt_names))

    for usage in dsinfo.usgs:

        # Expand [OPTIONS] token in the usage.
        if "OPTIONS" in usage.opts:

            # Remove the OPTIONS key from the usage.
            usage.opts.pop("OPTIONS")

            # Append all options.
            usage.opts = {opt.name: (opt.has_value, False) for opt in dsinfo.opts}

        # Standardize option names of usage pattern.
        usage.opts = {alt_names.get(key, key): value for key, value in usage.opts.items()}

        # Try to match the argument vector and usage pattern.
        user_input = match_argvec_and_usage(argv_std, usage)

        # If matched, returns the UserInput instance.
        if user_input is not None:

            # Append all unused precesing tokens as False.
            for u in dsinfo.usgs:
                for token_pre in u.pres[1:]:
                    if token_pre not in user_input.pres:
                        user_input.pres[token_pre] = False

            return user_input

    return None


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

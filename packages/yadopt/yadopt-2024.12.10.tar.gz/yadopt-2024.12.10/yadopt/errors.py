"""
Custom error classes.
"""

# Declare published functins and variables.
__all__ = ["YadOptError"]

# Import custom modules.
from .utils import get_error_marker, remove_indent


class YadOptErrorBase(Exception):
    """
    Base class of exception in YadOpt.
    """
    EPILOGUE = remove_indent("""
    If you find a bug in YadOpt, please let me know via GitHub issue.
    <https://github.com/tiskw/yadopt/issues>
    """.rstrip())

    def __init__(self, *pargs: tuple):
        """
        Constructor.
        """
        self.pargs = pargs

    def __str__(self) -> str:
        """
        Returns string expression of this error.
        """
        return self.stringify(*self.pargs)

    def stringify(self, *pargs: tuple, **kwargs: dict) -> str:
        """
        Convert myself to a string.
        """
        return "\n" + remove_indent(self.__doc__).format(*pargs, **kwargs) + self.EPILOGUE


class YadOptErrorUsageParse(YadOptErrorBase):
    """
    Error summary:
      YadOpt failed to parse a token in the usage section.

    Location:
      The following line in the usage setion.

        {0}

    Details:
      Each token in the usage section have to follow the specific format.
      For example, all argument tokens should be enclosed by angle bracket,
      all option tokens should be enclosed by bracket, and so on.
      Please see the YadOpt documentation for more details.

    Solution:
      This is unknown token error therefore no concrete solution can be suggest,
      sorry. Please see the YadOpt documentation and modigy your usage pattern
      in the usage section.
    """
    def __str__(self) -> str:
        """
        Returns string expression of this error.
        """
        line = self.pargs[0].strip()
        return self.stringify(line)


class YadOptErrorInvalidConstant(YadOptErrorBase):
    """
    Error summary:
      The error occurred because a constant token appears after an argument or
      option token. This pattern is now allowed in YadOpt, sorry.

    Location:
      The following line in the usage setion.

        {1}
        {2}

    Details:
      Constant tokens are only allowed at the beginning of a usage.
      For example,

        sample.py subcmd <arg1> bad_constant_token
                                ^^^^^^^^^^^^^^^^^^

      the above "bad_constant_token" cause the error because it appears after
      the argument <arg1>. The same error occurs if a constant token follows
      an option token, for example,

        sample.py subcmd [--opt1 val1] bad_constant_token
                                       ^^^^^^^^^^^^^^^^^^

    Solution:
      Please remove the constant token from the usage pattern. In some cases,
      you may need to reconsider the usage of your command. If you intended
      the argument, not constant token, please enclose the token in angle brackets
      because all arguments should be enclosed by brackets in the usage section.
    """
    def __str__(self) -> str:
        """
        Returns string expression of this error.
        """
        token  = self.pargs[0]
        line   = self.pargs[1].strip()
        marker = get_error_marker(line, token)
        return self.stringify(token, line, marker)


class YadOptErrorUsageArgMismatch(YadOptErrorBase):
    """
    Error summary:
      The usage does not match with the arguments/options section.

    Details:
      The user input "{0}" (= {1}) does exist in arguments/options section.

    Solution:
      Modify user input or arguments/options section in your docstring.
    """


class YadOptErrorInvalidTypeFunc(YadOptErrorBase):
    """
    Error summary:
      Invalid type function.

    Location:
      Argument "type_func" in "yadopt.parse" or "yadopt.wrap" function.

    Details:
      The type function should be a callable object or None, but the spacified
      object "{0}" does not satisfy either of them.

    Solution:
      Modify the value of the "type_func" argument.
    """


class YadOptErrorInvalidFileType(YadOptErrorBase):
    """
    Error summary:
      Invalid file type

    Location:
      Argument of {0}: {1}

    Details:
      The "yadopt.save" and "yadopt.load" functions support only ".txt" format, and gzipped
      version of it. However, this error indicates that the other suffixe than
      ".txt", ".txt.gz" is specified.

    Solution:
      Please specify the supported file type.
    """


YadOptError = {
    "usage_parse"       : YadOptErrorUsageParse,
    "invalid_constant"  : YadOptErrorInvalidConstant,
    "usage_arg_mismatch": YadOptErrorUsageArgMismatch,
    "invalid_type_func" : YadOptErrorInvalidTypeFunc,
    "invalid_file_type" : YadOptErrorInvalidFileType,
}


# vim: expandtab tabstop=4 shiftwidth=4 fdm=marker

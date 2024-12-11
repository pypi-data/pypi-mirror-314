from typing import Any

from functional_parsing_library.parser import Parser, T


def ignore_right(left: Parser[T], right: Parser[Any]) -> Parser[T]:
    """
    Parses using the left parser, and then parses using the right. The result from the left parser is discarded. If the
    right parser is unable to match something, the parser fails. The `<` operator is overloaded to call this function.
    For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = char('a') < char('b')
    >>> parser('ab').result
    'a'
    >>> from functional_parsing_library.parser import CouldNotParse
    >>> isinstance(parser('a'), CouldNotParse)
    True
    """
    return (lambda t, s: t) * left & right

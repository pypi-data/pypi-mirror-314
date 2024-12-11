from typing import Any

from functional_parsing_library.combinators.sequence.until.some_till_exclusive import some_till_exclusive
from functional_parsing_library.parser import Parser, U


def some_till(parser: Parser[U], until: Parser[Any]) -> Parser[list[U]]:
    """
    Parses zero or more matches for parser, followed by a match for until. Consumes the match for until. For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = some_till(char('a'), char('b'))
    >>> parser('aab').result
    ['a', 'a']
    >>> parser('aab').remainder
    ''
    >>> parser('b').result
    []
    """
    return some_till_exclusive(parser, until) < until

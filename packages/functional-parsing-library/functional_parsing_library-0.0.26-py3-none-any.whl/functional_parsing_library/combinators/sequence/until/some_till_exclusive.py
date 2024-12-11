from typing import Any

from functional_parsing_library.parser import Parser, U, ParseResults, CouldNotParse


def some_till_exclusive(parser: Parser[U], until: Parser[Any]) -> Parser[list[U]]:
    """
    Parses zero or more matches for parser, followed by a match for until. Does not consume the match for until.
    For example,
    >>> from functional_parsing_library.strings import char
    >>> parser = some_till_exclusive(char('a'), char('b'))
    >>> parser('aab').result
    ['a', 'a']
    >>> parser('aab').remainder
    'b'
    >>> parser('b').result
    []
    """
    def parse_function(to_parse: str) -> ParseResults[list[U]] | CouldNotParse:
        results: list[U] = []
        remainder = to_parse
        while True:
            delimiter = until(remainder)
            if not isinstance(delimiter, CouldNotParse):
                return ParseResults(results, remainder)
            parse_results = parser(remainder)
            if isinstance(parse_results, CouldNotParse):
                return parse_results
            results.append(parse_results.result)
            remainder = parse_results.remainder

    return Parser(parse_function)

from typing import Callable

from functional_parsing_library.parser import Parser, T, S, ParseResults, CouldNotParse


def bind(parser: Parser[T], parser_function: Callable[[T], Parser[S]]) -> Parser[S]:
    def _parser_function(to_parse: str) -> ParseResults[S] | CouldNotParse:
        parse_results = parser(to_parse)
        if isinstance(parse_results, CouldNotParse):
            return parse_results
        s_parser = parser_function(parse_results.result)
        return s_parser(parse_results.remainder)

    return Parser(_parser_function)

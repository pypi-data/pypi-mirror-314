from functional_parsing_library.combinators.sequence.separated_by import nothing
from functional_parsing_library.examples.person import const
from functional_parsing_library.parser import Parser, S


def n_times(n: int, parser: Parser[S]) -> Parser[list[S]]:
    if n == 0:
        return const([]) * nothing
    return (lambda t, ts: [t, *ts]) * parser & n_times(n - 1, parser)

import itertools

from learntools.python.utils import bind_exercises
from learntools.python.problem import *
from learntools.python.richtext import *
CS = CodeSolution

from learntools.python.solns.word_search import word_search
from learntools.python.solns.multi_word_search import multi_word_search
from learntools.python.solns.diamond import diamond

class ZipValidator(FunctionProblem):
    _var = 'is_valid_zip'

    _hint = ("Try looking up `help(str.isdigit)`")

    _solution = CS(
"""def is_valid_zip(zip_str):
    return len(zip_str) == 5 and zip_str.isdigit()""")

    _test_cases = [
            ('12345', True),
            ('1234x', False),
            ('1234', False),
            ('00000', True),
            ('', False),
            ('?', False),
    ]

class WordSearch(FunctionProblem):
    _var = 'word_search'

    _solution = CS.load('solns/word_search.py')

    _test_docs_a = [
            "The Learn Python Challenge Casino",
            "They bought a car",
            "Casinoville?",
    ]
    _test_docs_b = _test_docs_a + ["He bought a casino. That's crazy."]

    _test_inputs = [
            (_test_docs_a, 'casino'),
            (_test_docs_a, 'ear'),
            (_test_docs_b, 'crazy'),
            (_test_docs_b, 'bought'),
            ([], 'spam'),
    ]
    _test_cases = [
            (args, word_search(*args))
            for args in _test_inputs
    ]


class MultiWordSearch(FunctionProblem):
    _var = 'multi_word_search'
    _solution = CS.load('solns/multi_word_search.py')

    _test_docs_a = [
            "The Learn Python Challenge Casino",
            "They bought a car",
            "Casinoville?",
    ]
    _test_docs_b = _test_docs_a + ["He bought a casino. That's crazy."]
    _test_keywords = [
            [],
            ['casino'],
            ['casino', 'ear'],
            ['casino', 'ear', 'bought'],
    ]

    _test_cases = [
            (args, multi_word_search(*args))
            for args in itertools.product(
                [_test_docs_a, _test_docs_b, []],
                _test_keywords,
                )
            ]


class DiamondArt(FunctionProblem):
    _var = 'diamond'

    _solution = CS.load('solns/diamond.py')

    _test_heights = [2, 4, 0, 6]
    _test_cases = [
            (h, diamond(h))
            for h in _test_heights
            ]



qvars = bind_exercises(globals(), [
    ZipValidator,
    WordSearch,
    MultiWordSearch,
    DiamondArt,
    ],
)
__all__ = list(qvars)

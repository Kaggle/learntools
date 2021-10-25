import itertools

from learntools.core import *

import learntools.python.solns.word_search as word_search_module
word_search = word_search_module.word_search
import learntools.python.solns.multi_word_search as mws_module
multi_word_search = mws_module.multi_word_search
import learntools.python.solns.diamond as d_module
diamond = d_module.diamond
import learntools.python.solns.roulette_analysis as rou_module
roulette_gt = rou_module.conditional_roulette_probs

class ZA(EqualityCheckProblem):
    _var = 'length'
    _default_values = [-1]
    _expected = 0
    _solution = ("The empty string has length zero. Note that the empty "
            "string is also the only string that Python considers as False"
            " when converting to boolean.")
class ZB(EqualityCheckProblem):
    _var = 'length'
    _default_values = [-1]
    _expected = 7
    _solution = ("Keep in mind Python includes spaces (and punctuation) when"
            " counting string length.")
class ZC(EqualityCheckProblem):
    _var = 'length'
    _default_values = [-1]
    _expected = 7
    _solution = ("Even though we use different syntax to create it, the string"
            " `c` is identical to `b`. In particular, note that the backslash"
            " is not part of the string, so it doesn't contribute to its length.")
class ZD(EqualityCheckProblem):
    _var = 'length'
    _default_values = [-1]
    _expected = 3
    _solution = ("The fact that this string was created using triple-quote syntax"
            " doesn't make any difference in terms of its content or length. This"
            " string is exactly the same as `'hey'`.")
class ZE(EqualityCheckProblem):
    _var = 'length'
    _default_values = [-1]
    _expected = 1
    _solution = ("The newline character is just a single character! (Even though"
            " we represent it to Python using a combination of two characters.)")

LightningLen = MultipartProblem(
        ZA,ZB,ZC,ZD,ZE,
        )

class ZipValidator(FunctionProblem):
    _var = 'is_valid_zip'

    _hint = ("Try looking up `help(str.isdigit)`")

    _solution = CS(
"""def is_valid_zip(zip_code):
    return len(zip_code) == 5 and zip_code.isdigit()""")

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

    _solution = CS.load(word_search_module.__file__)

    _hint = ("Some methods that may be useful here: `str.split()`, `str.strip()`,"
            " `str.lower()`."
            )

    _test_docs_a = [
            "The Learn Python Challenge Casino",
            "They bought a car, and a horse",
            "Casinoville?",
    ]
    _test_docs_b = _test_docs_a + ["He bought a casino. That's crazy."]
    _test_docs_c = [
            "The Learn Python Challenge Casino has a big casino full of casino games",
            "They bought a car",
            "Casinoville",
    ]

    _test_inputs = [
            (_test_docs_a, 'casino'),
            (_test_docs_a, 'ear'),
            (_test_docs_a, 'car'),
            (_test_docs_b, 'crazy'),
            (_test_docs_b, 'bought'),
            # Test for not double-counting repeated instances within a document
            (_test_docs_c, 'casino'),
            ([], 'spam'),
    ]
    _test_cases = [
            (args, word_search(*args))
            for args in _test_inputs
    ]


class MultiWordSearch(FunctionProblem):
    _var = 'multi_word_search'
    _solution = CS.load(mws_module.__file__)

    _test_docs_a = [
            "The Learn Python Challenge Casino",
            "They bought a car",
            "Casinoville?",
    ]
    _test_docs_b = _test_docs_a + ["He bought a casino. A casino! That's crazy."]
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
    _bonus = True
    _var = 'diamond'

    _solution = CS.load(d_module.__file__)

    _hint = ("`str` has a few methods that help with the problem of padding"
            " a string to a certain size: two that might help here are"
            " `str.rjust()` or `str.center()`"
            )

    _test_heights = [2, 4, 0, 6]
    _test_cases = [
            (h, diamond(h))
            for h in _test_heights
            ]

    def check(self, fn):
        for args, expected in self._test_cases:
            orig_args = args
            # Wrap in tuple if necessary
            if not isinstance(args, tuple):
                args = args,
            try:
                actual = fn(*args)
            except Exception as e:
                actual = e

            assert actual is not None, ("Got a return value of `None`"
                    " given height = {}."
                    " Did you forget the return statement?").format(args[0])
            orig_actual = actual
            # Ignore spaces to the right of the diamond itself for purposes
            # of comparison.
            # Also, okay, fine, allow final newline in their answer. I guess.
            if len(actual) > 0 and actual[-1] == '\n':
                actual = actual[:-1]
            normalize = lambda di: '\n'.join(line.rstrip() for line in di.split('\n'))
            anorm = normalize(actual)
            enorm = normalize(expected)
            actual_shown = (
                    repr(orig_actual) if (orig_actual + ' ').isspace()
                    else actual
                    )
            assert anorm == enorm, (
                    "Expected diamond looking something like...\n\n"
                    "```\n{}\n```\n for height={}, but instead got this thing...\n\n"
                    "```\n{}\n```\n").format(
                            expected,
                            args[0],
                            actual_shown,
                            )

class RouletteAnalyzer(FunctionProblem):
    _bonus = True
    _var = 'conditional_roulette_probs'

    _solution = CS.load(rou_module.__file__)

    _test_inputs = [
            [1, 3, 1, 5, 1],
            [1, 1, 1, 1,],
            [1, 2, 1],
            [5, 1, 3, 1, 2, 1 , 3, 3, 5, 1, 2],
            [1, 2, 1, 2, 1, 2, 1, 3],
    ]

    _test_cases = [
            (args, roulette_gt(args))
            for args in _test_inputs
            ]


qvars = bind_exercises(globals(), [
    LightningLen,
    ZipValidator,
    WordSearch,
    MultiWordSearch,
    DiamondArt,
    RouletteAnalyzer
    ],
    start=0,
)
__all__ = list(qvars)

from abc import ABC, abstractmethod
# TODO: An annoying limitation of abc is that I can't mark an attribute as abstract, only a property.
# And I don't want to impose on each problem subclass to go to the work of defining a property for stuff like
# vars, expected.
# cf. https://stackoverflow.com/questions/43790040/how-to-create-an-abstract-class-attribute-potentially-read-only
from typing import List
import math
import numbers

from learntools.core.richtext import *
from learntools.core.exceptions import NotAttempted
from learntools.core import utils

# TODO: I'm sure there's a more elegant way to do this.
# Some kind of decorator on top of property?
def optionally_plural_property(obj, name):
    single_attr = getattr(obj, name, None)
    plural_attr = getattr(obj, name + 's', None)
    assert single_attr is None or plural_attr is None, ("Subclass should not implement"
            " both {0} and {0}s").format(name)
    if single_attr is not None:
        return [single_attr]
    elif plural_attr is not None:
        return plural_attr
    else:
        return []

class Problem(ABC):

    _solution = ''

    @property
    def solution(self):
        return self._solution

    @property
    def hints(self) -> List[str]:
        return optionally_plural_property(self, '_hint')

    def correct_message(self):
        if (
                self.show_solution_on_correct 
                or (self.show_solution_on_correct is None 
                    and isinstance(self.solution, str)
                    )
                ):
            return '\n\n' + self.solution
        else:
            return ''

    @abstractmethod
    def check(self, *args):
        pass

    def check_whether_attempted(self, *args):
        pass

class ThoughtExperiment(Problem):
    
    def check(self, *args):
        # TODO: Would be nice to be able to put the variable name this problem is
        # bound to here. (If we want to do that, it should probably live up one
        # level in the ProblemView?)
        msg = ("Nothing to check! (Just do this one in your head, then"
                " call `.solution()` to see if your prediction was correct.)")
        return msg

class CodingProblem(Problem):
    # What do we show when the user calls .check() and their code is correct?
    # False: just tell them they were right
    # True: tell them they were right, and show them the solution (as if they had 
    #       called problem.solution())
    # None: Use the default heuristic, which shows the solution iff solution is
    #       a string (i.e. not an instance of CodeSolution).
    show_solution_on_correct = None

    _var = None
    _vars = None
    
    @property
    def injectable_vars(self) -> List[str]:
        return optionally_plural_property(self, '_var')


class VarCreationProblem(CodingProblem):

    @property
    def expected(self):
        # This is somewhat fraught
        ex = self._expected
        if len(self.injectable_vars) == 1:
            return [ex]
        else:
            assert len(ex) == len(self.injectable_vars)
            return ex

    def failure_message(self, var, actual, expected):
        return "Incorrect value for variable `{}`: `{}`".format(
                    var, repr(actual))

    def assert_equal(self, var, actual, expected):
        if isinstance(expected, float):
            assert isinstance(actual, numbers.Number), \
                "Expected `{}` to be a number, but had value `{}` (type = `{}`)".format(
                    var, actual, type(actual))
            check = math.isclose(actual, expected, rel_tol=1e-06)
        else:
            check = actual == expected
        assert check, self.failure_message(var, actual, expected)

    def check(self, *args):
        for (var, actual, expected) in zip(self.injectable_vars, args, self.expected):
            self.assert_equal(var, actual, expected)


class FunctionProblem(CodingProblem):

    # Must have a single _var, corresponding to a function name
    
    # List of (input, expected_output) pairs, where input may be a scalar or tuple of args.
    _test_cases = []
    
    def check_whether_attempted(self, fn):
        # Not sure if inspect.getsource() will work reliably? Seems like it does
        # work okay with ipython notebooks. 
        def dummy(): 
            pass
        def dummy_w_docstring():
            """blah blah fishcakes"""
            pass
        # NB: looks like in terms of bytecode, a "pass" is treated like "return None", meaning this will 
        # possibly match other fns that just return some constant. Could be a little dangerous/brittle.
        src = lambda f: f.__code__.co_code
        if src(fn) in (src(dummy), src(dummy_w_docstring)):
            raise NotAttempted

    def check(self, fn):
        assert self._test_cases, "Oops, someone forgot to write test cases."
        for args, expected in self._test_cases:
            orig_args = args
            # Wrap in tuple if necessary
            if not isinstance(args, tuple):
                args = args,
            # TODO: ugh, need to guard against mutation :(
            args = [(arg.copy() if hasattr(arg, 'copy') else arg) for arg in args]
            orig_args = [(arg.copy() if hasattr(arg, 'copy') else arg) for arg in args]
            try:
                actual = fn(*args)
            except Exception as e:
                actual = e
            assert actual == expected, ("Expected return value of `{}` given {},"
                    " but got `{}` instead.").format(
                            repr(expected), utils.format_args(fn, orig_args), repr(actual))

class MultipartProblem:
    """A container for multiple related Problems grouped together in one 
    question. If q1 is a MPP, its subquestions are accessed as q1.a, q1.b, etc.
    """
    
    def __init__(self, *probs):
        self.problems = probs
        self._prob_map = {}
        assert len(probs) <= 26
        for i, prob in enumerate(probs):
            letter = chr(ord('a')+i)
            setattr(self, letter, prob)
            self._prob_map[letter] = prob

    def _repr_markdown_(self):
        return repr(self)

    def __repr__(self):
        varname = self.__class__.__name__
        part_names = ['`{}.{}`'.format(varname, letter) for letter in self._prob_map]
        return """This question is in {} parts. Those parts can be accessed as {}.
For example, to get a hint about part a, you would type `{}.a.hint()`.""".format(
            len(self._prob_map), ', '.join(part_names), varname
        )

__all__ = ['Problem', 'VarCreationProblem', 'FunctionProblem',
        'MultipartProblem', 'ThoughtExperiment',
        ]

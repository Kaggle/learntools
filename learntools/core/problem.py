from abc import ABC, abstractmethod
# TODO: An annoying limitation of abc is that I can't mark an attribute as abstract, only a property.
# And I don't want to impose on each problem subclass to go to the work of defining a property for stuff like
# vars, expected.
from typing import List
import math

from learntools.core.richtext import *

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

    # What do we show when the user calls .check() and their code is correct?
    # False: just tell them they were right
    # True: tell them they were right, and show them the solution (as if they had 
    #       called problem.solution())
    # None: Use the default heuristic, which shows the solution iff solution is
    #       a string (i.e. not an instance of CodeSolution).
    show_solution_on_correct = None

    # TODO: Not clear whether these should exist at this level or in subclass(es)
    # (also, initializing them to None is currently redundant)
    _var = None
    _vars = None

    _solution = ''

    @property
    def solution(self):
        return self._solution

    @property
    def injectable_vars(self) -> List[str]:
        return optionally_plural_property(self, '_var')

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

# TODO: Maybe separate this out between problems that simply involve creating one
# or more variables, and the more specific case where correctness entails checking
# the values of those variables against some static groundtruth values known ahead
# of time.
class VarCreationProblem(Problem):

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
            check = math.isclose(actual, expected, rel_tol=1e-06)
        else:
            check = actual == expected
        assert check, self.failure_message(var, actual, expected)

    def check(self, *args):
        for (var, actual, expected) in zip(self.injectable_vars, args, self.expected):
            self.assert_equal(var, actual, expected)


__all__ = ['Problem', 'VarCreationProblem']

from abc import ABC, abstractmethod
from typing import List
import functools

from learntools.core.richtext import *
from learntools.core.exceptions import NotAttempted, Uncheckable, UserlandExceptionIncorrect
from learntools.core import utils, asserts, constants

# I'm sure there's a more elegant way to do this.
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

    # used for valueTowardsCompletion bookkeeping
    _counts_for_points = True
    _bonus = False

    @property
    def solution(self):
        return self._solution

    @property
    def hints(self) -> List[str]:
        return optionally_plural_property(self, '_hint')

    @property
    def _correct_message(self):
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
        """If this method runs without exceptions, it indicates that checking passed
        and the solution is correct. To indicate other outcomes, implementations of 
        this method should raise one of the following:
        - Uncheckable: If this problem explicitly has no checking logic.
        - NotAttempted: If it seems the problem hasn't been attempted (i.e. the 
            starter code hasn't been modified.
        - Incorrect, AssertionError: If there's a problem with the user's solution.

        Any messages attached to these exceptions will be passed on in the message shown
        to the user.
        """
        pass

    def check_whether_attempted(self, *args):
        pass

class ThoughtExperiment(Problem):

    show_solution_on_correct = True
    def check(self, *args):
        pass

# TODO: apply directly to EqualityCheckProblem.check etc.?
def injected(method):
    """A decorator for (custom) methods of Problem subclasses which want to receive
    injected values from the student's notebook as arguments - in the same way that
    .check(), .check_whether_attempted() etc. are automatically supplied injected
    args in CodingProblem subclasses.

    Injected methods may also receive additional, explicit, user-supplied arguments.
    They should come after any injected args.
    """
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        # More muddying of the waters btwn Problem and ProblemView :/
        # XXX: Handling of unset variables. This call may throw NotAttempted/Incorrect.
        injargs = self._view._get_injected_args()
        # Sometimes there are user-supplied args to pass on in addition to the
        # ones we're injecting (see python.ex3 Blackjack problem for an example of this)
        # Injected args first, then any additional ones.
        newargs = list(injargs) + list(args)
        return method(self, *newargs, **kwargs)

    return wrapped

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
    # Can optionally set _default_values class attr (for purposes of NotAttempted checking)
    
    @property
    def injectable_vars(self) -> List[str]:
        return optionally_plural_property(self, '_var')

    def check_whether_attempted(self, *args):
        # TODO: copy-paste from EqualityCheckProblem.check_whether_attempted
        varnames = self.injectable_vars
        def _raise_not_attempted():
            raise NotAttempted("You need to update the code that creates"
                    " variable{} {}".format('s' if len(varnames) > 1 else '',
                        ', '.join(map(utils.backtickify, varnames))))
        # First, check whether any vars have placeholder values
        for (var, val) in zip(varnames, args):
            # NB: Yoda condition to ensure that it's PlaceholderValue's __eq__ that gets called.
            if constants.PLACEHOLDER == val:
                _raise_not_attempted()


class EqualityCheckProblem(CodingProblem):
    """A problem which is considered solved iff some user-defined variables 
    are equal to some groundtruth expected values.

    The conventional way for subclasses to specify expected values is with a _expected
    member, containing a list of expected values (of the same length as _vars and in
    the same order).

    In the common case where there is only one variable of interest (_var), subclasses
    can set _expected to be a simple scalar (rather than wrapping the value in a list of
    length 1). (Special case: to avoid ambiguity, if the expected value is itself a list 
    of length 1, it must be wrapped)
    """

    @property
    def expected(self):
        """A list of expected values. Matches length and order of _var/_vars
        """
        ex = self._expected
        if len(self.injectable_vars) == 1:
            # Don't wrap length-1 lists (i.e. assume that ex[0] is the expected value
            # of our single variable of interest, rather than ex itself)
            if (isinstance(ex, list) or isinstance(ex, tuple)) and len(ex) == 1:
                return ex
            else:
                return [ex]
        else:
            assert len(ex) == len(self.injectable_vars)
            return ex

    def check(self, *args):
        for (var, actual, expected) in zip(self.injectable_vars, args, self.expected):
            asserts.assert_equal(actual, expected, var=var,
                    failure_factory=getattr(self, '_failure_message', None)
                    )

    def check_whether_attempted(self, *args):
        varnames = self.injectable_vars
        def _raise_not_attempted():
            raise NotAttempted("You need to update the code that creates"
                    " variable{} {}".format('s' if len(varnames) > 1 else '',
                        ', '.join(map(utils.backtickify, varnames))))
        # First, check whether any vars have placeholder values
        for (var, val) in zip(varnames, args):
            # NB: Yoda condition to ensure that it's PlaceholderValue's __eq__ that gets called.
            if constants.PLACEHOLDER == val:
                _raise_not_attempted()
        if not hasattr(self, '_default_values'):
            return
        for var, val, default in zip(
                varnames, args, self._default_values
                ):
            try:
                neq = val != default
            except:
                # If we get an exception comparing the actual value to the expected,
                # we can reasonably infer they're not equal.
                neq = True
            # If the actual value is an ndarray or DataFrame or something, the result of != may
            # be something more complicated than a bool. If this is the case, let's assume the
            # actual value differs from the default. (Default values will probably never be anything
            # as complicated an ndarray/df/series anyways)
            if not isinstance(neq, bool):
                return
            if neq:
                return
        # It'd be kind of odd if a EqualityCheckProblem didn't have any associated
        # vars, but I guess it's not worth raising a fuss over...
        if len(args):
            _raise_not_attempted()


class FunctionProblem(CodingProblem):

    # Must have a single _var, corresponding to a function name
    
    # List of (input, expected_output) pairs, where input may be a scalar or tuple of args.
    _test_cases = []
    
    @classmethod
    def check_whether_attempted(cls, fn):
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
            # XXX: ugh, need to guard against mutation :(
            # Beware of more exotic mutable types (which lack a copy method, or which
            # require a deep copy). Maybe this shouldn't be handled at this level -
            # maybe cleaner to have a method that can repeatedly spit out fresh lists
            # of test cases every time it's called, rather than having test cases be
            # a static attribute.
            args = [(arg.copy() if hasattr(arg, 'copy') else arg) for arg in args]
            orig_args = [(arg.copy() if hasattr(arg, 'copy') else arg) for arg in args]
            try:
                actual = fn(*args)
            except Exception as e:
                raise UserlandExceptionIncorrect(e, orig_args)
            assert not (actual is None and expected is not None), ("Got a return value of `None`"
                    " given {}, but expected a value of type `{}`. (Did you forget a `return` statement?)"
                    ).format(utils.format_args(fn, orig_args), type(expected).__name__)
            assert actual == expected, ("Expected return value of `{}` given {},"
                    " but got `{}` instead.").format(
                            repr(expected), utils.format_args(fn, orig_args), repr(actual))


__all__ = ['Problem', 'EqualityCheckProblem', 'FunctionProblem',
        'ThoughtExperiment', 'CodingProblem',
        ]

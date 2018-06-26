import functools
from collections import Counter

from IPython.display import display

from learntools.core.richtext import *
from learntools.core.exceptions import *
from learntools.core.problem import Problem, CodingProblem

def displayer(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        res = fn(*args, **kwargs)
        display(res)
        # Don't propagate the return to avoid double printing.
    return wrapped

def record(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        self.interactions[method.__name__] += 1
        return method(self, *args, **kwargs)
    return wrapped

class ProblemView:

    _not_attempted_msg = ("When you've updated the starter code, `check()` will"
            " tell you whether your code is correct."
    )

    def __init__(self, problem:Problem, globals_):
        self.problem = problem
        self.globals = globals_
        self.interactions = Counter()

    def __getattr__(self, attr):
        """By default, expose methods of the contained Problem object if
        they're not marked private.
        """
        val = getattr(self.problem, attr)
        if not attr.endswith('_') and callable(val):
            return val
        raise AttributeError
    
    @record
    @displayer
    def check(self):
        try:
            if isinstance(self.problem, CodingProblem):
                args = self._get_injected_args()
            else:
                args = ()
            self.problem.check_whether_attempted(*args)
            self.problem.check(*args)
        except NotAttempted as e:
            return ProblemStatement(self._not_attempted_msg + ' ' + str(e))
        # TODO: switch over to just Incorrect (wrap AssertionErrors at some level)
        except (Incorrect, AssertionError) as e:
            return TestFailure(str(e))
        except Uncheckable as e:
            return RichText(str(e) or 'Sorry, no auto-checking available for this question.', 
                    color='#cc5533')
        else:
            return Correct(self.problem.correct_message)

    def _get_injected_args(self):
        names = self.problem.injectable_vars 
        missing = set(names) - self.globals.keys()
        if len(missing) == 0:
            return self.globals.lookup(names)
        elif len(missing) == len(names):
            # Hm, maybe RichText objects should be raisable? Or is that too much?
            raise NotAttempted("Remember, you must create the following variable{}: {}"\
                    .format('s' if len(missing) > 1 else '', 
                        ', '.join('`{}`'.format(v) for v in missing)
                        )
                    )
        else:
            raise Incorrect("You still need to define the following variables: {}".format(
                    ', '.join('`{}`'.format(v) for v in missing)
                    ))

    
    @record
    @displayer
    def hint(self, n=1):
        hints = self.problem.hints
        if not hints:
            # TODO: magic colors
            return RichText('Sorry, no hints available for this question.', 
                    color='#cc5533')
        # TODO: maybe wrap these kinds of user errors to present them in a nicer way?
        assert n <= len(hints), "No further hints available!"
        hint = hints[n-1]
        assert isinstance(hint, str)
        return Hint(hint)

    @record
    @displayer
    def solution(self):
        soln = self.problem.solution
        if isinstance(soln, RichText):
            return soln
        return Solution(soln)

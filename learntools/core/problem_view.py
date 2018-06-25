import functools

from IPython.display import display

from learntools.core.richtext import *
from learntools.core.exceptions import *
from learntools.core.problem import Problem

def displayer(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        res = fn(*args, **kwargs)
        display(res)
        # Don't propagate the return to avoid double printing.
    return wrapped

class ProblemView:

    _not_attempted_msg = ("When you've updated the starter code, `check()` will"
            " tell you whether your code is correct."
    )

    def __init__(self, problem:Problem, globals_):
        self.problem = problem
        self.globals = globals_
    
    @displayer
    def check(self):
        try:
            args = self._get_injected_args()
            self.problem.check_whether_attempted(*args)
            self.problem.check(*args)
        except NotAttempted as e:
            return ProblemStatement(self._not_attempted_msg + ' ' + str(e))
        # TODO: switch over to just Incorrect (wrap AssertionErrors at some level)
        except (Incorrect, AssertionError) as e:
            return TestFailure(str(e))
        else:
            return Correct(self.problem.correct_message())

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

    @displayer
    def solution(self):
        soln = self.problem.solution
        if isinstance(soln, RichText):
            return soln
        return Solution(soln)

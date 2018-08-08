import functools
import traceback
from collections import Counter

from IPython.display import display

from learntools.core.richtext import *
from learntools.core.exceptions import *
from learntools.core.problem import Problem, CodingProblem
from learntools.core import colors, tracking

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

    def __init__(self, problem:Problem, globals_, tutorial_id):
        self.problem = problem
        self.globals = globals_
        self.tutorial_id = tutorial_id
        self.interactions = Counter()

    def __getattr__(self, attr):
        """By default, expose methods of the contained Problem object if
        they're not marked private.
        """
        val = getattr(self.problem, attr)
        if not attr.endswith('_') and callable(val):
            return val
        raise AttributeError
    
    @property
    def questionId(self):
        # e.g. '3_MyHardProblem'
        id = self.problem.__class__.__name__
        if hasattr(self, '_order'):
            id = '{}_{}'.format(self._order, id)
        return id

    def _track_event(self, interactionType, **kwargs):
       kwargs['interactionType'] = interactionType
       problem_fields = dict(
               learnTutorialId=self.tutorial_id,
               questionId=self.questionId,
        )
       kwargs.update(problem_fields)
       tracking.track(kwargs)

    def _track_check(self, outcome, **kwargs):
        if outcome == tracking.OutcomeType.PASS:
            kwargs['valueTowardsCompletion'] = self.problem.point_value
        self._track_event(tracking.InteractionType.CHECK, outcomeType=outcome, **kwargs)
    
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
            self._track_check(tracking.OutcomeType.UNATTEMPTED)
            return ProblemStatement(self._not_attempted_msg + ' ' + str(e))
        except (Incorrect, AssertionError) as e:
            if isinstance(e, UserlandExceptionIncorrect):
                wrapped = e.wrapped_exception
                tb_lines = traceback.format_tb(wrapped.__traceback__)
                tb_str = '\n'.join(tb_lines)
                self._track_check(tracking.OutcomeType.EXCEPTION,
                    exceptionClass=wrapped.__class__.__name__,
                    trace=tb_str,
                    failureMessage=str(e),
                    )
            else:
                self._track_check(tracking.OutcomeType.FAIL,
                    failureMessage=str(e),
                    )
            return TestFailure(str(e))
        except Uncheckable as e:
            msg = str(e) or 'Sorry, no auto-checking available for this question.' 
            self._track_check(tracking.OutcomeType.EXCEPTION, 
                failureMessage=msg,
                exceptionClass='Uncheckable',
                trace='',
            )
            return RichText(msg, color=colors.WARN)
        else:
            self._track_check(tracking.OutcomeType.PASS)
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
            msg = 'Sorry, no hints available for this question.'
            self._track_event(tracking.InteractionType.HINT, failureMessage=msg)
            return RichText(msg, color=colors.WARN)
        self._track_event(tracking.InteractionType.HINT)
        # TODO: maybe wrap these kinds of user errors to present them in a nicer way?
        # (e.g. LearnUserError, LearnUsageError)
        assert n <= len(hints), "No further hints available!"
        hint = hints[n-1]
        assert isinstance(hint, str)
        return Hint(hint, n, last=(n == len(hints)))

    @record
    @displayer
    def solution(self):
        self._track_event(tracking.InteractionType.SOLUTION)
        soln = self.problem.solution
        if isinstance(soln, RichText):
            return soln
        return Solution(soln)

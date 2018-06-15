import math
from IPython.display import display
from learntools.python.globals_binder import binder 
from learntools.python.richtext import *
from learntools.python.utils import backtickify

#XXX: This is probably problematic from a testing point of view...
G = binder.readonly_globals()

def displayer(fn):
    """Decorator taking a function returning a str/RichText object, and 
    making it instead display that value (and return nothing)
    """
    def wrapped(cls, *args):
        res = fn(cls, *args)
        cls.display(res)
        # Don't propagate the return to avoid double printing.
    return wrapped

# TODO: Might even be worth overhauling the whole architecture of having a class
# for each problem (rather than having each problem be an instance).
# TODO: Might want to rethink this Metaclass cleverness. I've tried to structure
# the code such that concrete Problem subclasses will (almost?) never need to directly
# implement check(), is_attempted(), hint(), or solution(). They usually just need
# to define some class attributes. In a complicated case, they might have to define
# their own is_attempted(), or _do_check().
# SO, the automatic wrapping of those methods doesn't really save many lines of code,
# and maybe isn't worth the added crypticness and debugging difficulty.
class ProblemMeta(type):
    """Metaclass for Problems. Does stuff like...
    - Decorates all methods with classmethod
    - wraps certain methods with displayer()
    - wraps certain attrs in corresponding RichText classes (e.g. Hint() around _hint(s))
    """
    # Wrap methods with these names with the displayer decorator
    display_wraps = ['check', 'hint', 'solution',]
    def __new__(meta, name, parents, dct):
        # TODO: I don't think this is really used/needed anymore?
        # Set _varname attr (q1, q2...)
        dct.setdefault('_varname', name)

        # Wrap methods
        for attr, val in dct.items():
            if callable(val):
                if attr in meta.display_wraps:
                    val = displayer(val)
                val = classmethod(val)
                dct[attr] = val

        # Wrap hints
        hints = dct.get('_hints', [])
        for i, hint_text in enumerate(hints):
            assert isinstance(hint_text, str)
            hints[i] = Hint(hint_text, n=i+1, 
                    last = (i == (len(hints)-1))
                    )
        if dct.get('_hint') and not hints:
            hints.append( Hint(dct['_hint']) )
            dct['_hints'] = hints

        return super().__new__(meta, name, parents, dct)


class NotAttempted(Exception):
    pass

class Incorrect(Exception):
    pass


class Problem(object, metaclass=ProblemMeta):
    """Problem objects are what will be presented to the user for (almost) every problem in the 
    exercise notebooks for the Python track. They can be interacted with using the standard methods:
    - check
    - hint
    - solution
    """

    # Subclasses should fill in no more than one of the two attributes below. 
    # _hints is for the case where you want to offer multiple hints (presumably
    # of increasing explicitness). _hint is a convenience for the most common
    # case where you want just one.
    _hint = ''
    _hints = []

    _solution = ''

    # subclasses should define up to 1 of these attrs. Names of variables the
    # user must define to solve the problem. Will be injected into subclass
    # method calls.
    _var = None
    _vars = None

    # TODO: would be nice if this said q1.check() or q2.check() or whatever
    # Probably doable once we tie problems together into "Exercise" containers
    _problem = ("When you've updated the starter code, `check()` will"
            " tell you whether your code is correct."
            )

    # How many times this problem has been attempted (by calling .check())
    _tries = 0
    _hinted = False
    _peeked = False

    def _injectable_vars(cls):
        assert cls._var is None or cls._vars is None, ("Subclass should not implement"
                " both _var and _vars")
        if cls._var:
            names = [cls._var]
        elif cls._vars:
            names = cls._vars
        else:
            names = []
        return names

    def _get_injected_args(cls):
        """Snoop notebook global namespace for variables whose value we should
        inject into calls to check() and is_attempted()
        Return their values as a list (in the same order as cls._vars)
        """
        names = cls._injectable_vars()
        missing = set(names) - G.keys()
        if len(missing) == 0:
            return G.lookup(names)
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

    def check(cls):
        """Check the given answer. 3 possibilities:
        1. If we can detect that the user has probably not attempted the problem
           (i.e. the starter code is unchanged), then 'yellow light'. Remind them
           what they have to do (and that they can get hints/solutions?).
        2. If their answer is wrong, red light. Maybe give some idea of in what
            way their answer is wrong. (Remind about hints/solutions?)
        3. If their answer is right, green light. Congratulations. Possibly some coda.
        """
        cls._tries += 1
        try:
            args = cls._get_injected_args()
            cls._check_whether_attempted(*args)
            cls._do_check(*args)
        except NotAttempted as e:
            return ProblemStatement(cls._problem + ' ' + str(e))
        # TODO: switch over to just Incorrect (wrap AssertionErrors at some level)
        except (Incorrect, AssertionError) as e:
            return TestFailure(str(e))
        else:
            return Correct(cls._correct_message())

    def _correct_message(cls):
        # This is a heuristic that will probably fail at some point.
        if cls._solution and isinstance(cls._solution, str):
            return '\n\n' + cls._solution
        return ''

    def _check_whether_attempted(cls, *args):
        # TODO: just have subclasses implement this directly rather than is_attempted?
        if not cls.is_attempted(*args):
            raise NotAttempted

    def hint(cls, n=1):
        cls._hinted = True
        if not cls._hints:
            return RichText('Sorry, no hints available for this question.', 
                    color='#cc5533')
        # TODO: maybe wrap these kinds of user errors to present them in a nicer way?
        assert n <= len(cls._hints), "No further hints available!"
        hint = cls._hints[n-1]
        assert isinstance(hint, Hint)
        return hint

    def solution(cls, *args):
        cls._peeked = True
        soln = cls._solution
        if isinstance(soln, RichText):
            return soln
        return Solution(soln)

    def display(cls, text):
        if isinstance(text, str):
            text = RichText(text)
        display(text)

    def is_attempted(cls, *args):
        # TODO: I wonder if there's some kind of magic IPython introspection that
        # we could use to read the contents of the code corresponding code cell? Seems tricky.
        # esp. given that the user may interact with the Problem obj in a different cell
        # or in the console.
        return True

    def _do_check(cls, *args):
        """Subclasses must implement. If a problem is found with the given solution, 
        they should raise an AssertionError with an appropriate message. If none are
        raised, the solution is presumed correct.
        """
        # TODO: maybe expose to the user the fact that k/n tests passed?
        pass

class ThoughtExperiment(Problem):
    """A Problem with no checking logic."""

    def check(cls, *args):
        msg = ("Nothing to check! (Just do this one in your head, then"
                " call {}.solution() to see if your prediction was correct.)").format(
                        cls._varname)
        return msg

class VarCreationProblem(Problem):
    """A problem that requires creating one or more variables. We know ahead of
    time the values that those variables should have.

    If none of the variables have been created, we treat the problem as unattempted.
    If some but not all have been created, it's incorrect.
    Otherwise, it's correct if and only if all the variables' values are equal to
    their expected values.
    """
    # Expected value of variable or variables (corresponding to class attrs
    # _var/_vars)
    _expected = None

    _default_values = []

    # In future, may need to handle situation where our checking logic depends on a
    # few variables, at least one of which the user must create, and at least one
    # of which we will have already created for them in the starter code.
    # (assuming we want to automatically inject the latter variables)

    def _expecteds(cls):
        ex = cls._expected
        # TODO: Bleh, this is dangerous.
        if isinstance(ex, (list, tuple)) and len(ex) == len(cls._injectable_vars()):
            return ex
        return [ex]

    def _check_whether_attempted(cls, *values):
        # TODO: bleh, this overrides the is_attempted checking base implementation
        # maybe need to call super or something.
        if cls._default_values:
            defaulty = []
            for var, actual, default in zip(
                    cls._injectable_vars(),
                    values,
                    cls._default_values
                    ):
                if actual == default:
                    defaulty.append(var)
            if defaulty:
                raise NotAttempted("You need to update the code that creates"
                        " variable{} {}".format('s' if len(defaulty) > 1 else '',
                            ', '.join(map(backtickify, defaulty))))

    def _failure_message(cls, var, actual, expected):
        return "Incorrect value for variable `{}`: `{}`".format(
                    var, repr(actual))

    def _do_check(cls, *args):
        for (var, actual, expected) in zip(
                cls._injectable_vars(),
                args,
                cls._expecteds()):
            if isinstance(expected, float):
                check = math.isclose(actual, expected, rel_tol=1e-06)
            else:
                check = actual == expected
            assert check, cls._failure_message(var, actual, expected)

# TODO: would be nice to have some way to specify a canonical implementation of
# the function. That way for our test cases we only need to specify some set of
# inputs - we wouldn't need to manually specific the expected outputs.
# TODO: Maybe give some generically useful message when the user's function
# returns None but it's expected to return something? (e.g. "did you forget
# a return statement?")
class FunctionProblem(Problem):
    """A Problem that requires filling in the body of a function.
    (The name of the function should be specified as _var)
    """
    
    # List of (input, expected_output) pairs, where input may be a scalar or tuple of args.
    _test_cases = []

    def is_attempted(cls, fn):
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
        return src(fn) not in (src(dummy), src(dummy_w_docstring))

    @staticmethod
    def _format_args(fn, args):
        # I guess technically not portable to other python implementations...
        c = fn.__code__
        params = c.co_varnames[:c.co_argcount]
        assert len(args) == len(params)
        return ', '.join([
            '`{}={}`'.format(param, repr(arg))
            for (param, arg) in zip(params, args)
            ])

    def _do_check(cls, fn):
        # TODO: maybe for this checking stuff could hook into unittest machinery somehow?
        assert cls._test_cases, "Oops, someone forgot to write test cases."
        for args, expected in cls._test_cases:
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
                            repr(expected), cls._format_args(fn, orig_args), repr(actual))

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

# TODO: do something slightly cleverer here
class DummyProblem:
    pass

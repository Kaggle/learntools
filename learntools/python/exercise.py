from IPython.display import display

def displayer(fn):
    """Decorator taking a function returning a str/RichText object, and 
    making it instead display that value (and return nothing)
    """
    def wrapped(cls, *args):
        res = fn(cls, *args)
        cls.display(res)
        # Don't propagate the return to avoid double printing.
    return wrapped

class ExerciseMeta(type):
    """Metaclass for Exercises. Does stuff like...
    - Decorates all methods with classmethod
    - wraps certain methods with displayer()
    - wraps certain attrs in corresponding RichText classes (e.g. Hint() around _hint(s))
    """
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

def colorify(text, color):
    return '<span style="color:{}">{}</span>'.format(color, text)

# TODO: would probably have made more sense to define this as a mixin?
class RichText:
    """Crucially this defines methods for both rich and plaintext representations.
    If displayed from a code cell, it will render the nice rich output. If in the console,
    we'll fall back to the simple representation.
    """
    def __init__(self, txt, color=None):
        self.txt = txt
        self.color = color

    def _repr_markdown_(self):
        if self.color:
            return colorify(self.txt, self.color)
        return self.txt

    def __repr__(self):
        # TODO: filter out markdown
        return self.txt

class PrefixedRichText(RichText):
    label_color = 'black'
    @property
    def label(self):
        if hasattr(self, '_label'):
            return self._label
        return self.__class__.__name__

    def _repr_markdown_(self):
        pre = colorify(self.label+':', self.label_color)
        return pre + ' ' + self.txt


# Might be worth also investigating other formatting options. Maybe set a bg-color throughout?
class Hint(PrefixedRichText):
    label_color = "#3366cc"
    def __init__(self, txt, n=1, last=True):
        self.n = n
        # Is this one of a series of hints?
        self.is_multi = n > 1 or not last
        if not last:
            # TODO: include _varname?
            # TODO: colorify?
            coda = '\n(For another hint, call `.hint({})`)'.format(n+1)
            txt += coda
        super().__init__(txt)

    @property
    def label(self):
        if self.is_multi:
            return 'Hint {}'.format(self.n)
        return 'Hint'

class Solution(PrefixedRichText):
    label_color = "#33cc99"

class CodeSolution(Solution):
    _label = 'Solution'    

    def __init__(self, txt):
        wrapped = "\n```python\n{}\n```".format(txt)
        super().__init__(wrapped)

class TestFailure(PrefixedRichText):
    label_color = "#cc3333"
    _label = 'Incorrect'

class ProblemStatement(PrefixedRichText):
    label_color = '#ccaa33'
    _label = 'Check'


class Exercise(object, metaclass=ExerciseMeta):
    """Exercise objects are what will be presented to the user for (almost) every problem in the 
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

    # TODO: would be nice if this said q1.check() or q2.check() or whatever
    _problem = ("When you've updated the starter code, `check()` will"
            " tell you whether your code is correct."
            )

    def check(cls, *args):
        """Check the given answer. 3 possibilities:
        1. If we can detect that the user has probably not attempted the problem
           (i.e. the starter code is unchanged), then 'yellow light'. Remind them
           what they have to do (and that they can get hints/solutions?).
        2. If their answer is wrong, red light. Maybe give some idea of in what
            way their answer is wrong. (Remind about hints/solutions?)
        3. If their answer is right, green light. Congratulations. Possibly some coda.
        """
        if not cls.is_attempted(*args):
            return ProblemStatement(cls._problem)
        else:
            try:
                cls._do_check(*args)
                return RichText('Correct!', color='#33cc33')
            except AssertionError as e:
                return TestFailure(str(e))

    def hint(cls, n=1):
        if not cls._hints:
            return RichText('Sorry, no hints available for this question.', 
                    color='#cc5533')
        # TODO: maybe wrap these kinds of user errors to present them in a nicer way?
        assert n <= len(cls._hints), "No further hints available!"
        hint = cls._hints[n-1]
        assert isinstance(hint, Hint)
        return hint

    def solution(cls, *args):
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
        # esp. given that the user may interact with the Exercise obj in a different cell
        # or in the console.
        return True

    def _do_check(cls, *args):
        """Subclasses must implement. If a problem is found with the given solution, 
        they should raise an AssertionError with an appropriate message. If none are
        raised, the solution is presumed correct.
        """
        # TODO: maybe expose to the user the fact that k/n tests passed?
        pass

class ThoughtExperiment(Exercise):
    """An Exercise with no checking logic."""

    def check(cls, *args):
        msg = ("Nothing to check! (Just do this one in your head, then"
                " call {}.solution() to see if your prediction was correct.)").format(
                        cls._varname)
        return msg

class FunctionExercise(Exercise):
    """An exercise that requires filling in the body of a function.
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
            '`{}={}`'.format(param, arg)
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
            actual = fn(*args)
            assert actual == expected, ("Expected return value of `{}` given {},"
                    " but got `{}` instead.").format(
                            expected, cls._format_args(fn, args), actual)

class MultipartExercise:
    """A container for multiple related exercises grouped together in one 
    question. If q1 is a MPE, its subquestions are accessed as q1.a, q1.b, etc.
    """
    
    def __init__(self, *exs):
        self.exercises = exs
        self._ex_map = {}
        assert len(exs) <= 26
        for i, ex in enumerate(exs):
            letter = chr(ord('a')+i)
            setattr(self, letter, ex)
            self._ex_map[letter] = ex

    def _repr_markdown_(self):
        return repr(self)

    def __repr__(self):
        varname = self.__class__.__name__
        part_names = ['`{}.{}`'.format(varname, letter) for letter in self._ex_map]
        return """This question is in {} parts. Those parts can be accessed as {}.
For example, to get a hint about part a, you would type `{}.a.hint()`.""".format(
        len(self._ex_map), ', '.join(part_names), varname)

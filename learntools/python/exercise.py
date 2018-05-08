from IPython.display import display

"""
TODO: if we do go the IPython.display route, we probably need some way to detect 
whether we're in a code cell, or if we're being run from the console. :/
If we are going to direct them to call stuff like hint() and solution() in the 
console rather than in a code cell, then I guess it's not even worth trying to
implement Ipython display fanciness.

Maybe if we implement both __repr__ and _repr_[html/markdown/whatever]_
then display() will be smart enough to fall back to printing the plain text
repr when called in the console? Yeah, seems like this works. (Though it's
mildly annoying that when run in a code cell, it writes the rich output
*and* displays the basic output in the console.

IPython display options
- Code (6.3)
- HTML
- Latex
- Markdown
- cf. _repr_html_, _repr_latex_, etc. (_repr_markdown_?)

- color coding?

When defining new exercise, may need to specify...
- how to tell whether starter code is unchanged
- test cases
- hint(s)
- solution text
- 
"""

def displayer(fn):
    def wrapped(cls, *args):
        res = fn(cls, *args)
        cls.display(res)
        # Don't propagate the return to avoid double printing.
    return wrapped

class ExerciseMeta(type):
    display_wraps = ['check', 'hint', 'solution',]
    """Decorate all methods with classmethod"""
    def __new__(meta, name, parents, dct):
        # Set _varname attr (q1, q2...)
        dct.setdefault('_varname', name)
        for attr, val in dct.items():
            if callable(val):
                if attr in meta.display_wraps:
                    val = displayer(val)
                val = classmethod(val)
                dct[attr] = val
        return super().__new__(meta, name, parents, dct)

def colorify(text, color):
    return '<span style="color:{}">{}</span>'.format(color, text)

class RichText:
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
        #pre = '<span style="color:{}">{}</span> '.format(self.label_color, self.label)
        pre = colorify(self.label+':', self.label_color)
        return pre + ' ' + self.txt


class Solution(RichText): # XXX
    def _repr_markdown_(self):
        # This doesn't really work. Would need to import markdown, use markdown.markdown
        # to get the html repr, and then wrap *that* in a styled div (in _repr_html_).
        return "<div style='background-color:green'>{}</div>".format(self.txt)

class Hint(PrefixedRichText):
    label_color = "#3366cc"

class Solution(PrefixedRichText):
    label_color = "#33cc99"

class TestFailure(PrefixedRichText):
    label_color = "#cc3333"
    _label = 'Incorrect'

class ProblemStatement(PrefixedRichText):
    label_color = '#ccaa33'
    _label = 'Check'


class Exercise(object, metaclass=ExerciseMeta):

    _hint = ''
    _solution = ''

    # TODO: would be nice if this said q1.check() or q2.check() or whatever
    _problem = ("When you've updated the starter code, `check()` will"
            " tell you whether your code is correct."
            )

    def check(cls, *args):
        """Check the given answer. 3 possibilities:
        1. If we can detect that the user has probably not attempted the problem
           (i.e. the starter code is unchanged), then 'yellow light'. Remind them
           what they have to do, and that they can get hints/solutions.
        2. If their answer is wrong, red light. Maybe give some idea of in what
            way their answer is wrong. Remind about hints/solutions.
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

    def hint(cls, *args):
        if not cls._hint:
            return RichText('Sorry, no hints available for this question.', 
                    color='#cc5533')
        return Hint(cls._hint)

    def solution(cls, *args):
        return Solution(cls._solution)

    def display(cls, text): # XXX
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
        # XXX: Maybe the nicest way to handle this is to let subclasses just
        # implement a method that does a bunch of asserts, and they get wrapped
        # in a method that intercepts the messages and renders them nicely.
        # TODO: Also, maybe expose to the user the fact that k/n tests passed?
        pass

class ThoughtExperiment(Exercise):
    """An Exercise with no checking logic."""

    def check(cls, *args):
        msg = ("Nothing to check! (Just do this one in your head, then"
                " call {}.solution() to see if your prediction was correct.)").format(
                        cls._varname)
        return msg

class FunctionExercise(Exercise):
    
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

    def _do_check(cls, fn):
        # TODO: format assertion failures nicely. (And maybe don't propagate as
        # actual exceptions, so they don't halt the rest of the code in the cell
        # in which they're run?)
        assert cls._test_cases, "Oops, someone forgot to write test cases."
        for args, expected in cls._test_cases:
            orig_args = args
            if not isinstance(args, tuple):
                args = args,
            actual = fn(*args)
            assert actual == expected, ("Expected return value of {} given {},"
                    " but got {} instead.").format(expected, orig_args, actual)

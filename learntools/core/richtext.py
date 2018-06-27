from . import colors

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
        # TODO: we should strip out markdown syntax here
        # (Though, in practice, this will basically never be seen. These exercises
        # were really designed to be run in notebooks.)
        return self.txt

class PrefixedRichText(RichText):
    """A RichText message prefixed with some label (which may optionally be styled
    with a distinct color).
    """
    label_color = 'black' # This can be overridden with any valid CSS color
    @property
    def label(self):
        # If no _label attribute is present, fall back to the class name.
        if hasattr(self, '_label'):
            return self._label
        return self.__class__.__name__

    def _repr_markdown_(self):
        if not self.txt:
            # TODO: hm, this fallback behaviour makes sense for Correct and
            # TestFailure, but not really for the others.
            return colorify(self.label, self.label_color)
        pre = colorify(self.label+':', self.label_color)
        return pre + ' ' + self.txt

    def __repr__(self):
        if not self.txt:
            return self.label
        return self.label + ':' + ' ' + self.txt


# Might be worth also investigating other formatting options. Maybe set a bg-color throughout? (Would help distinguish markdown output from a code cell and rendered markdown cells - they can sometimes bleed together visually)
class Hint(PrefixedRichText):
    label_color = colors.HINT
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

class Correct(PrefixedRichText):
    _label = 'Correct'
    label_color = colors.CORRECT

class Solution(PrefixedRichText):
    label_color = colors.SOLUTION

class CodeSolution(Solution):
    """A solution consisting entirely of Python code. We wrap this in a 
    syntax-highlighted code block.
    """
    _label = 'Solution'    

    def __init__(self, *lines):
        """As a convenience, may pass in one string per line of code, rather than
        one big multi-line string.
        """
        txt = '\n'.join(lines)
        wrapped = "\n```python\n{}\n```".format(txt)
        super().__init__(wrapped)

    @classmethod
    def load(cls, path):
        """Return a CodeSolution containing the code located in the source file
        at the given path.
        """
        with open(path) as f:
            lines = f.readlines()
            # Strip trailing newlines (cause constructor adds them back...)
            lines = [line[:-1] for line in lines 
                    # Hack
                    if not line.startswith('from learntools.python.solns')
                    ]
            return cls(*lines)

class TestFailure(PrefixedRichText):
    label_color = colors.INCORRECT
    _label = 'Incorrect'

class ProblemStatement(PrefixedRichText):
    label_color = colors.INFO
    _label = 'Check'

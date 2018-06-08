from learntools.python.utils import bind_exercises
from learntools.python.problem import *
from learntools.python.richtext import *

class ExerciseFormatTutorial(VarCreationProblem):
    _var = 'color'
    _expected = 'blue'

    _hint = "Your favorite color rhymes with *glue*."
    _solution = CodeSolution('color = "blue"')

    def _correct_message(cls):
        if not cls._hinted and not cls._peeked:
            return ("What?! You got it right without needing a hint or anything?"
                    " Drats. Well hey, you should still continue to the next step"
                    " to get some practice asking for a hint and checking solutions."
                    " (Even though you obviously don't need any help here.)"
                    )
        return ''

    def _failure_message(cls, var, actual, expected):
        if (
                any(actual.endswith(suff) for suff in ['oo', 'ue', 'ew'])
                and actual.strip().lower() != 'blue'
            ):
            return "Ha ha, very funny."
        elif actual.strip(' .!').lower() == 'ni':
            return "Please! Please! No more! We will find you a shrubbery."
        return ("{} is not your favorite color!"
                " Well, maybe it is, but we're writing the rules. The point"
                " of this question is to force you to get some practice asking"
                " for a hint. Go ahead and uncomment the call to `q0.hint()`"
                " in the code cell below, for a hint at what your favorite color"
                " *really* is.")


class CircleArea(VarCreationProblem):
    _vars = ['radius', 'area']
    _expected = [3/2, (3/2)**2 * 3.14159]

    _hint = "The syntax to raise a to the b'th power is `a ** b`"
    _solution = CodeSolution('radius = diameter / 2',
            'area = pi * radius ** 2')

# Not used.
class MemModelAliasing(ThoughtExperiment):
    # No hint?
    _solution = CodeSolution(
            'The value of `y` is still `1`. You can verify this by adding a line to the end of the cell with the code `print(y)`.',
            "#TODO: maybe this actually isn't a great question, since it ultimately comes down to mutability, which is really too advanced a topic to be going into right now, and isn't talked about in the tutorial...")

class VariableSwap(Problem):

    _hint = "Try using a third variable."
    _solution = """Use a third variable to temporarily store one of the old values. e.g.:

    tmp = a
    a = b
    b = tmp

If you've read lots of Python code, you might have seen the following trick to swap two variables in one line:

    a, b = b, a

We'll demystify this bit of Python magic later when we talk about **tuples**."""

    def store_original_ids(cls):
        cls.id_a = id(G['a'])
        cls.id_b = id(G['b'])

    def _do_check(cls):
        ida = id(G['a'])
        idb = id(G['b'])
        orig_values = [1, 2, 3], [3, 2, 1]
        a, b = G['a'], G['b']
        if ida == cls.id_b and idb == cls.id_a:
            return
        assert not (ida == cls.id_a and idb == cls.id_b), ("`a` and `b` still"
                " have their original values.")
        orig_ids = (cls.id_a, cls.id_b)
        if (b, a) == orig_values:
            # well this is ridiculous in its verbosity
            assert False, ("You successfully set `a` to `[3, 2, 1]` and `b` to"
                    " `[1, 2, 3]`, but you didn't succeed at swapping the variables.\n\n"
                    "How can that be? Imagine the following scenario:\n" +
"""
- Al is in Albania holding an alabaster piece of paper
- Brad is in Brazil holding a brown piece of paper

You're tasked with getting them to swap papers. You might decide that a clever shortcut is to have Al toss his paper in the recycling and go to a stationary shop to get a brown piece of paper, and have Brad buy a white piece of paper. But even if the paper that Al acquires is the exact same shade of brown as Brad's, and the same size, it's not the same piece of paper. It may be *equivalent*, but it's not *identical*. The only way to truly execute our task is to have Al and Brad ship their papers across the Atlantic to each other.

Similarly, in Python, if `a = [1, 2, 3]`, then running `b = [1, 2, 3]` assigns a value to `b` which is *equivalent* to `a`'s value, but not *identical*. If we want the latter, we need to assign `b = a`. Why does this matter? If `a` and `b` refer to the same object, then modifying one of them (for example by calling `a.append(4)` - we'll learn more about that later) will modify both of them.""")
        assert ida in orig_ids, ("`a` was assigned something weird (its id has changed,"
                " but to something other than `b`'s id)")
        assert idb in orig_ids, ("`b` was assigned something weird (its id has changed,"
                " but to something other than `a`'s id)")
        assert ida != idb, "`b` and `a` are the same! Both have value `{}`".format(
                repr(G['a']))
        assert False, "This fails in a way we did not anticipate!"

# It's an interesting question whether to make these parens questions checkable.
# Making them non-checkable for now.
class ArithmeticParensEasy(ThoughtExperiment):

    _hint = ('Following its default "BEDMAS"-like rules for order of operations,'
            ' Python will first divide 3 by 2, then subtract the result from 5.'
            ' You need to add parentheses to force it to perform the subtraction first.')
    _solution = CodeSolution("(5 - 3) // 2")

class ArithmeticParensHard(ThoughtExperiment):

    _hint = 'You may need to use several pairs of parentheses.'
    _solution = "`(8 - 3) * (2 - (1 + 1))` is one solution. There may be others."

ArithmeticParens = MultipartProblem(ArithmeticParensEasy, ArithmeticParensHard)

class CandySplitting(VarCreationProblem):
    _var = 'to_smash'
    _expected = (121 + 77 + 109) % 3

    _hints = [
            "You'll probably want to use the modulo operator, `%`.",
            "`j % k` is the remainder after dividing `j` by `k`",
    ]
    _solution = CodeSolution("(alice_candies + bob_candies + carol_candies) % 3")


class MysteryExpression(VarCreationProblem): 
    _var = 'ninety_nine_dashes'
    _expected = 4

    _hint = ("What would the value of the expression be if there were exactly one `-`?"
            " What about two? Can you add parentheses to make it clearer?")
    _solution = """The original expression's value is `10`. If we had used 99 `-`s, the expression's value would be 4. But why? Let's start with a simpler version...
`7-3` is of course just 3 subtracted from 7: 4. The key is what happens when we add another `-`.

`7--3` is `10`. To match how Python evaluates this expression, we would parenthesize it as `7-(-3)`. The first `-` is treated as a subtraction operator, but the second one is treated as *negation*. We're subtracting negative 3 (which is equivalent to adding 3). Subsequent `-`s are all treated as additional negations, so they cause the subtracted quantity to flip back and forth between 3 and negative 3. Therefore, when there are an even number of `-`s, the expression equals 4. When there's an odd number, the expression equals 10.
"""

# TODO: mention side effects.
class SameValueInitializationRiddle(ThoughtExperiment):

    _hints = [
            "You're unlikely to see any practical difference when the value we're initializing to is an int. But think about other Python types you're familiar with...",
            """`a = b = <expression>` is equivalent to...
```python
b = <expression>
a = b```""",
    ]

    _solution = """The one-line syntax results in `a` and `b` having the same memory address - i.e. they refer to the same object. This matters if that object is of a **mutable** type, like list. Consider the following code:
```python
odds = evens = []
for i in range(5):
    if (i % 2) == 0:
        evens.append(i)
    else:
        odds.append(i)
print(odds)
print(evens)```

We might expect this would print `[1, 3]`, then `[0, 2, 4]`. But actually, it will print `[0, 1, 2, 3, 4]` twice in a row. `evens` and `odds` refer to the same object, so appending an element to one of them appends it to both of them. This is occasionally the source of hair-pulling debugging sessions. :)"""


qvars = bind_exercises(globals(), [
    ExerciseFormatTutorial,
    CircleArea,
    #MemModelAliasing,
    VariableSwap,
    ArithmeticParens,
    CandySplitting,
    MysteryExpression,
    SameValueInitializationRiddle,
    ],
    start=0,
    )
__all__ = list(qvars)

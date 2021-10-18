from learntools.core import *
from learntools.core.problem import injected

class ExerciseFormatTutorial(CodingProblem):
    _var = 'color'
    _hint = "Your favorite color rhymes with *glue*."
    _solution = CS('color = "blue"')
    def check(self, color):
        assert color.lower() == "blue"

    @property
    def _correct_message(self):
        history = self._view.interactions
        if history['hint'] == 0 and history['solution'] == 0:
            return ("What?! You got it right without needing a hint or anything?"
                    " Drats. Well hey, you should still continue to the next step"
                    " to get some practice asking for a hint and checking solutions."
                    " (Even though you obviously don't need any help here.)"
                    )
        return ''

    def _failure_message(self, var, actual, expected):
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
                " *really* is.").format(actual)


class CircleArea(EqualityCheckProblem):
    _vars = ['radius', 'area']
    _expected = [3/2, (3/2)**2 * 3.14159]

    _hint = "The syntax to raise a to the b'th power is `a ** b`"
    _solution = CS('radius = diameter / 2',
            'area = pi * radius ** 2')

class VariableSwap(CodingProblem):
    _vars = ['a', 'b']

    _hint = "Try using a third variable."
    _solution = """The most straightforward solution is to use a third variable to temporarily store one of the old values. e.g.:

    tmp = a
    a = b
    b = tmp

If you've read lots of Python code, you might have seen the following trick to swap two variables in one line:

    a, b = b, a

We'll demystify this bit of Python magic later when we talk about *tuples*."""

    @injected
    def store_original_ids(self, a, b):
        self.id_a = id(a)
        self.id_b = id(b)

    def check(self, a, b):
        ida = id(a)
        idb = id(b)
        orig_values = [1, 2, 3], [3, 2, 1]
        if ida == self.id_b and idb == self.id_a:
            return
        assert not (ida == self.id_a and idb == self.id_b), ("`a` and `b` still"
                " have their original values.")
        orig_ids = (self.id_a, self.id_b)
        if (b, a) == orig_values:
            # well this is ridiculous in its verbosity
            assert False, (
        "Did you write something like...\n"
        "```python\na = [3, 2, 1]\nb = [1, 2, 3]```\n?\n"
        "That's not an unreasonable think to try, but there are two problems:\n"
        "1. You're relying on knowing the values of `a` and `b` ahead of time."
        " What if you wanted to swap two variables whose values weren't known"
        " to you ahead of time?\n"
        "2. Your code actually results in `a` referring to a *new* object (whose value is the same as `b`'s previous value), and similarly for `b`. To see why this is, consider that the code...\n"
        "```python\n"
        "a = [1, 2, 3]\n"
        "b = [1, 2, 3]```\n"
        "Is actually *different* from:\n"
        "```python\n"
        "a = [1, 2, 3]\n"
        "b = a```\n"
        "In the second case, `a` and `b` refer to the same object. In the first case, `a` and `b` refer to different objects which happen to be equivalent. This may seem like a merely philosophical difference, but it matters when we start *modifying* objects. In the second scenario, if we run `a.append(4)`, then `a` and `b` would both have the value `[1, 2, 3, 4]`. If we run `a.append(4)` in the first scenario, `a` refers to `[1, 2, 3, 4]`, but `b` remains `[1, 2, 3]`. (We'll talk more about lists and mutability in a later lesson.)"
        )
        assert ida in orig_ids, ("`a` was assigned something weird (its id has changed,"
                " but to something other than `b`'s id)")
        assert idb in orig_ids, ("`b` was assigned something weird (its id has changed,"
                " but to something other than `a`'s id)")
        assert ida != idb, "`b` and `a` are the same! Both have value `{}`".format(
                repr(a))
        assert False, "This fails in a way we did not anticipate!"

# It's an interesting question whether to make these parens questions checkable.
# Making them non-checkable for now.
class ArithmeticParensEasy(ThoughtExperiment):
    _hint = ('Following its default "BEDMAS"-like rules for order of operations,'
            ' Python will first divide 3 by 2, then subtract the result from 5.'
            ' You need to add parentheses to force it to perform the subtraction first.')
    _solution = CS("(5 - 3) // 2")

class ArithmeticParensHard(ThoughtExperiment):
    _hint = 'You may need to use several pairs of parentheses.'
    _solution = "`(8 - 3) * (2 - (1 + 1))` is one solution. There may be others."

ArithmeticParens = MultipartProblem(ArithmeticParensEasy, ArithmeticParensHard)

class CandySplitting(EqualityCheckProblem):
    _var = 'to_smash'
    _expected = (121 + 77 + 109) % 3
    _default_values = [-1]

    _hints = [
            "You'll probably want to use the modulo operator, `%`.",
            "`j % k` is the remainder after dividing `j` by `k`",
    ]
    _solution = CS("(alice_candies + bob_candies + carol_candies) % 3")


class MysteryExpression(EqualityCheckProblem): 
    _bonus = True
    _var = 'ninety_nine_dashes'
    _expected = 4

    _hint = ("What would the value of the expression be if there were exactly one `-`?"
            " What about two? Can you add parentheses to make it clearer?")
    _solution = """The original expression's value is `10`. If we had used 99 `-`s, the expression's value would be 4. But why? Let's start with a simpler version...
`7-3` is of course just 3 subtracted from 7: 4. The key is what happens when we add another `-`.

`7--3` is `10`. To match how Python evaluates this expression, we would parenthesize it as `7-(-3)`. The first `-` is treated as a subtraction operator, but the second one is treated as *negation*. We're subtracting negative 3 (which is equivalent to adding 3). Subsequent `-`s are all treated as additional negations, so they cause the subtracted quantity to flip back and forth between 3 and negative 3. Therefore, when there are an odd number of `-`s, the expression equals 4. When there's an even number, the expression equals 10.
"""

class QuickdrawGridProblem(ThoughtExperiment):
    _bonus = True
    _hint = """There are a few ways to solve this. Of the tools we've talked about so far, `//` and `%` (the integer division and modulo operators) and the `min` function may be useful."""
    _solution = """Here's one possible solution:
```python
rows = n // 8 + min(1, n % 8)
cols = min(n, 8)
height = rows * 2
width = cols * 2
```
Calculating `rows` is the trickiest part. Here's another way of doing it:
```python
rows = (n + 7) // 8```
We haven't shown the `math` module, but if you're familiar with the ceiling function, you might find this approach more intuitive:
```python
import math
rows = math.ceil(n / 8)
rows = int(rows) # ceil returns a float```
"""

class SameValueInitializationRiddle(ThoughtExperiment):
    _bonus = True
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

We might expect this would print `[1, 3]`, then `[0, 2, 4]`. But actually, it will print `[0, 1, 2, 3, 4]` twice in a row. `evens` and `odds` refer to the same object, so appending an element to one of them appends it to both of them. This is occasionally the source of hair-pulling debugging sessions. :)

Another consideration is expressions that have side effects. For example, `list.pop` is a method which removes and returns the final element of a list. If we have `L = [1, 2, 3]`, then `a = b = L.pop()`, will result in `a` and `b` both having a value of 3. But running `a = L.pop()`, then `b = L.pop()` will result in `a` having value 3 and `b` having value 2.
"""


qvars = bind_exercises(globals(), [
    ExerciseFormatTutorial,
    CircleArea,
    VariableSwap,
    ArithmeticParens,
    CandySplitting,
    MysteryExpression,
    QuickdrawGridProblem,
    SameValueInitializationRiddle,
    ],
    start=0,
    )
__all__ = list(qvars)

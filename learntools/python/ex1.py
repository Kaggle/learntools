from utils import bind_exercises

class ExerciseFormatTutorial(VarCreationExercise):
    _varname = 'color'
    _expected = 'blue'

    _hint = "Your favorite color rhymes with *glue*."
    _solution = CodeSolution('color = "blue"')


class CircleArea(VarCreationExercise):
    _varnames = ['radius', 'area']
    # TODO: make sure we do approx-equal checks when appropriate
    _expected = [3/2, (3/2)**2 * 3.14159]

    _hint = "The syntax to raise a to the b'th power is `a ** b`"
    _solution = CodeSolution('radius = diameter / 2',
            'area = pi * radius ** 2')

class MemModelAliasing(ThoughtExperiment):
    # No hint?
    _solution = [
            'The value of `y` is still `1`. You can verify this by adding a line to the end of the cell with the code `print(y)`.',
            "**TODO**: maybe this actually isn't a great question, since it ultimately comes down to mutability, which is really too advanced a topic to be going into right now, and isn't talked about in the tutorial..."]

class VariableSwap(Exercise):

    _hint = "Try using a third variable."
    _solution = """Use a third variable to temporarily store one of the old values. e.g.:

    tmp = a
    a = b
    b = tmp

If you've read lots of Python code, you might have seen the following trick to swap two variables in one line:

    a, b = b, a

We'll demystify this bit of Python magic later when we talk about **tuples**."""

    def store_original_ids(cls, ida, idb):
        cls.id_a = ida
        cls.id_b = idb

    def _do_check(cls, ida, idb):
        if ida == cls.id_b and idb == cls.id_a:
            return
        assert not (ida == cls.id_a and idb == cls.id_b), ("`a` and `b` still"
                " have their original values.")
        orig_ids = (cls.id_a, cls.id_b)
        assert ida in orig_ids, ("`a` was assigned something weird (its id has changed,"
                " but to something other than `b`'s id)")
        assert idb in orig_ids, ("`b` was assigned something weird (its id has changed,"
                " but to something other than `a`'s id)")
        assert ida != idb, "`b` and `a` are the same!"
        assert False, "This fails in a way we did not anticipate!"

class ArithmeticParensEasy(ThoughtExperiment):

    _hint = ('Following its default "BEDMAS"-like rules for order of operations,'
            ' Python will first divide 3 by 2, then subtract the result from 5.'
            ' You need to add parentheses to force it to perform the subtraction first.')
    _solution = CodeSolution("(5 - 3) // 2")

class ArithmeticParensHard(ThoughtExperiment):

    _hint = 'You may need to use several pairs of parentheses.'
    _solution = "`(8 - 3) * (2 - (1 + 1))` is one solution. There may be others."

ArithmeticParens = MultipartExercise(ArithmeticParensEasy, ArithmeticParensHard)

class CandySplitting(FunctionExercise):

    _hints = [
            "You'll probably want to use the modulo operator, `%`.",
            "`j % k` is the remainder after dividing `j` by `k`",
    ]
    _solution = CodeSolution("return (a_candies + b_candies + c_candies) % 3")

    _test_cases = [
            ((1, 1, 1), 0),
            ((8, 2, 0), 1),
            ((0, 0, 0), 0),
    ]

class MysteryExpression(ThoughtExperiment): 

    _hint = ("What would the value of the expression be if there were exactly one `-`?"
            "What about two? Can you add parentheses to make it clearer?")
    _solution = """The expression's value is `10`. But why? Let's start with a simpler version...
`7-3` is of course just 3 subtracted from 7: 4. The key is what happens when we add another `-`.

`7--3` is `10`. To match how Python evaluates this expression, we would parenthesize it as `7-(-3)`. The first `-` is treated as a subtraction operator, but the second one is treated as *negation*. We're subtracting negative 3 (which is equivalent to adding 3). Subsequent `-`s are all treated as additional negations, so they cause the subtracted quantity to flip back and forth between 3 and negative 3. Therefore, when there are an even number of `-`s, the expression equals 4. When there's an odd number, the expression equals 10.
"""


qvars = bind_exercises(globals(), [
    ExerciseFormatTutorial,
    CircleArea,
    MemModelAliasing,
    VariableSwap,
    ArithmeticParens,
    CandySplitting,
    MysteryExpression
    ])
__all__ = list(qvars)

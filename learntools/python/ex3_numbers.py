from exercise import *

class q1a(ThoughtExperiment):

    _hint = ('Following its default "BEDMAS"-like rules for order of operations,'
            ' Python will first divide 3 by 2, then subtract the result from 5.'
            ' You need to add parentheses to force it to perform the subtraction first.')
    _solution = CodeSolution("(5 - 3) // 2")

class q1b(ThoughtExperiment):

    _hint = 'You may need to use several pairs of parentheses.'
    _solution = "`(8 - 3) * (2 - (1 + 1))` is one solution. There may be others."

q1 = MultipartExercise(q1a, q1b)

class q2(FunctionExercise):

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

class q3(ThoughtExperiment): 

    _hint = ("What would the value of the expression be if there were exactly one `-`?"
            "What about two? Can you add parentheses to make it clearer?")
    _solution = """The expression's value is `10`. But why? Let's start with a simpler version...
`7-3` is of course just 3 subtracted from 7: 4. The key is what happens when we add another `-`.

`7--3` is `10`. To match how Python evaluates this expression, we would parenthesize it as `7-(-3)`. The first `-` is treated as a subtraction operator, but the second one is treated as *negation*. We're subtracting negative 3 (which is equivalent to adding 3). Subsequent `-`s are all treated as additional negations, so they cause the subtracted quantity to flip back and forth between 3 and negative 3. Therefore, when there are an even number of `-`s, the expression equals 4. When there's an odd number, the expression equals 10.
"""

from exercise import Exercise, FunctionExercise, ThoughtExperiment

class q1(FunctionExercise):

    # Maybe should give a special message if they've modified the function body
    # but they don't have a return statement?

    _test_cases = [
            (1.000001, 1.00),
            (1.23456, 1.23),
    ]
    _hint = ("Type `help(round)` into the console to learn more about the round function."
            " You'll need to use the function's optional second argument.")
    _solution = "`return round(num, 2)`"

class q2(ThoughtExperiment):

    _solution = """As you've seen, `ndigits=-1` rounds to the nearest 10, `ndigits=-2` rounds to the nearest 100 and so on. Where might this be useful? Suppose we're dealing with large numbers:

> The area of Finland is 338,424 km²  
> The area of Greenland is 2,166,086 km²

We probably don't care whether it's really 338,424, or 338,425, or 338,177. All those digits of accuracy are just distracting. We can chop them off by calling `round()` with `ndigits=-3`:

> The area of Finland is 338,000 km²  
> The area of Greenland is 2,166,000 km²
"""

class q4(ThoughtExperiment):

    _hint = "Think about what happened when we called `help(abs(-2))`"
    
    _solution = """If you've tried running the code, you've seen that it prints:

    Spam
    None

What's going on here? The inner call to the `print` function prints the string "Spam" of course. The outer call prints the value returned by the `print` function - which we've seen is `None`.

Why do they print in this order? Python evaluates the arguments to a function before running the function itself. This means that nested function calls are evaluated from the inside out. Python needs to run `print("Spam")` before it knows what value to pass to the outer `print`."""


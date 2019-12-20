from learntools.core import *
from learntools.core.exceptions import Incorrect

class RoundFunctionProblem(FunctionProblem):
    _var = 'round_to_two_places'

    _test_cases = [
            (1.000001, 1.00),
            (1.23456, 1.23),
    ]
    _hint = ("Run `help(round)` in the console (or in a code cell) to learn more about the round function."
            " You'll need to use the function's optional second argument.")
    _solution = CS("return round(num, 2)")

class RoundNdigitsProblem(ThoughtExperiment):

    _solution = """As you've seen, `ndigits=-1` rounds to the nearest 10, `ndigits=-2` rounds to the nearest 100 and so on. Where might this be useful? Suppose we're dealing with large numbers:

> The area of Finland is 338,424 km²  
> The area of Greenland is 2,166,086 km²

We probably don't care whether it's really 338,424, or 338,425, or 338,177. All those digits of accuracy are just distracting. We can chop them off by calling `round()` with `ndigits=-3`:

> The area of Finland is 338,000 km²  
> The area of Greenland is 2,166,000 km²

(We'll talk about how we would get the commas later when we talk about string formatting :))
"""

class PrintPrintProblem(ThoughtExperiment):

    _hint = "Think about what happened when we called `help(abs(-2))` in the tutorial"
    
    _solution = """If you've tried running the code, you've seen that it prints:

    Spam
    None

What's going on here? The inner call to the `print` function prints the string "Spam" of course. The outer call prints the value returned by the `print` function - which we've seen is `None`.

Why do they print in this order? *Python evaluates the arguments to a function before running the function itself*. This means that nested function calls are evaluated from the inside out. Python needs to run `print("Spam")` before it knows what value to pass to the outer `print`."""

class CandySmashingFunctionProblem(FunctionProblem):
    _var = 'to_smash'

    _test_cases = [
           ((10, 2), 0),
           ((10, 3), 1),
           ((10, 4), 2),
           (10, 1),
           (9, 0),
           ((10, 10), 0),
           ((10, 11), 10),
            ]
    _hint = "Refer to the section of the last tutorial notebook where we talked about default arguments"
    _solution = CS(
"""def to_smash(total_candies, n_friends=3):
    return total_candies % n_friends""")

    def check(self, fn):
        try:
            x = fn(10, 2)
        except TypeError:
            raise Incorrect("`to_smash` should be callable with two arguments (e.g. `to_smash(10, 2)`")
        try:
            x = fn(10)
        except TypeError:
            raise Incorrect("`to_smash` should be callable with a single argument (e.g. `to_smash(10)`")
        super().check(fn)

# How the heck to test this?
class TimeCallProblem(ThoughtExperiment):
    _var = 'time_call'

    _hint = "You'll need to call `time()` before and after calling the input function in order to measure its running time. The `sleep` function will be very useful for testing."
    # TODO: Write out the whole function
    _solution = '''Example function body:
```python
t0 = time()
fn(arg)
t1 = time()
elapsed = t1 - t0
return elapsed
```
To test your function, you can run something like `time_call(sleep, 2)` and make sure its return value is close to 2. 
'''

class SlowestCallProblem(ThoughtExperiment):
    _hint = "You'll want to call the function you wrote in the previous question (`time_call`) in the body of `slowest_call`."
    _solution = """
```python
return max(time_call(fn, arg1), time_call(fn, arg2), time_call(fn, arg3))
```

You *could* copy-paste the code you wrote for `time_call` three times with some slight variable changes. But that's highly not recommended. It's more typing, and if you later noticed a bug in `time_call`, you'd have to fix it in 4 places. [Laziness is one of the three great virtues of a programmer.](http://threevirtues.com/)
"""

class SmallestStringyDebug(ThoughtExperiment):
    _solution = (
"""`smallest_stringy_number('10', '2', '3')` is one example of a failure - it evaluates to '10' rather than '2'.

The problem is that when `min` is applied to strings, Python returns the earliest one in *lexicographic order* (i.e. something like the logic used to order dictionaries or phonebooks) rather than considering their numerical value.
""")

class SmallestStringyFix(FunctionProblem):
    _var = 'smallest_stringy_number'
    
    _test_cases =  [
            ( ('1', '2', '3'), '1'),
            ( ('10', '2', '3'), '2'),
            ( ('2', '3', '10'), '2'),
            ( ('-100', '10', '5'), '-100'),
            ]

    _hint = "Remember that `min` can optionally take a `key` argument representing a function to apply to each element before comparing them."
    _solution = CS('return min(s1, s2, s3, key=int)')

SmallestStringyProblem = MultipartProblem(SmallestStringyDebug,
        SmallestStringyFix)

qvars = bind_exercises(globals(), [
    RoundFunctionProblem,
    RoundNdigitsProblem,
    CandySmashingFunctionProblem,
    None, # Reading exceptions
    TimeCallProblem,
    SlowestCallProblem,
    PrintPrintProblem,
    SmallestStringyProblem,
    ],
)
__all__ = list(qvars)

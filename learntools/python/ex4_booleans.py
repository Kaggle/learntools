from exercise import *

class q1(Exercise):

    _hint = ("Take a look at how we fixed our original expression in the main"
            " lesson. We added parentheses around certain subexpressions. "
            "The bug in this code is caused by Python evaluating certain operations "
            "in the \"wrong\" order.")

    _solution = """One example of a failing test case is:

```python
have_umbrella = False
rain_level = 0.0
have_hood = False
is_workday = False
```

Clearly we're prepared for the weather in this case. It's not raining. Not only that, it's not a workday, so we don't even need to leave the house! But our function will return False on these inputs.

The key problem is that Python implictly parenthesizes the last part as:

```python
(not (rain_level > 0)) and is_workday
```

Whereas what we were trying to express would look more like:

```python
not (rain_level > 0 and is_workday)
```
"""

    @staticmethod
    def canonical_prepared(have_umbrella, rain_level, have_hood, is_workday):
        return (have_umbrella or
                       (rain_level < 5 and have_hood) or
                        not (rain_level > 0 and is_workday)
                       )
    @staticmethod
    def ill_prepared(have_umbrella, rain_level, have_hood, is_workday):
        return have_umbrella or rain_level < 5 and have_hood or not rain_level > 0 and is_workday

    # XXX: Copy paste from FnExercise. bad.
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

    def _do_check(cls, *args):
        expected = cls.canonical_prepared(*args)
        actual = cls.ill_prepared(*args)
        assert actual != expected, ("Given {}, `prepared_for_weather` returned"
                " {}. But I think that's correct. (We want inputs that lead to"
                " an incorrect result from `prepared_for_weather`.)").format(
                        cls._format_args(cls.ill_prepared, args),
                        actual,
                        )


class q2(FunctionExercise):
    # XXX: blah, looks like there's no clean way to check for single-line-ness. 
    # But they'll know whether they've accomplished it or not, and there's not much
    # point in cheating.

    _test_cases = [
            (1, False),
            (0, False),
            (-100, True),
    ]

    _hint = ("If the value of the expression `number < 0` is `True`, then we return"
            " `True`. If it's `False`, then we return `False`...")
    _solution = CodeSolution("return number < 0")

class q3a(FunctionExercise):

    _hint = "You'll need to use the `and` operator."
    _solution = CodeSolution("return ketchup and mustard and onion")

    _test_cases = [
            ((True, True, True), True),
            ((False, True, True), False),
            ((False, False, False), False),
            ((True, False, True), False),
    ]

class q3b(FunctionExercise):

    _hint = "You'll need to use the `not` operator."
    # TODO: might mention the demorgans'd alternative
    # TODO: a generally useful thing would be being able to pass multiple solution
    # strings to CodeSolution, and have them presented with some text like "here's
    # another possible solution..."
    _solution = CodeSolution("return not ketchup and not mustard and not onion")

    _test_cases = [
            ((True, True, True), False),
            ((False, True, True), False),
            ((False, False, False), True),
            ((True, False, True), False),
    ]

class q3c(FunctionExercise):

    _hint = ("There are exactly two ways to set ketchup and mustard to make this"
            " true. What are they?"
            )
    _solution = CodeSolution("return (ketchup and not mustard) or (mustard and not ketchup)")

    _test_cases = [
            ((True, True, True), False),
            ((False, True, True), True),
            ((False, False, False), False),
            ((True, False, True), True),
    ]

q3 = MultipartExercise(q3a, q3b, q3c)

class q4(FunctionExercise):

    _hint = ("You may have already found that `int(True)` is 1, and `int(False)` is 0."
            " Think about what kinds of basic arithmetic operations you might want to"
            " perform on `ketchup`, `mustard`, and `onion` after converting them to integers."
            )
    _solution = CodeSolution("return (int(ketchup) + int(mustard) + int(onion)) == 1")
    
    _test_cases = [
            ((True, True, True), False),
            ((False, True, True), False),
            ((False, False, False), False),
            ((True, False, True), False),
            ((False, False, True), True),
    ]

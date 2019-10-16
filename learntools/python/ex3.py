import inspect

from learntools.core import *
from learntools.core.problem import injected
from learntools.core.exceptions import Uncheckable
from learntools.core.utils import format_args

from learntools.python.blackjack import BlackJack

class SignFunctionProblem(FunctionProblem):
    _var = 'sign'

    _test_cases = [
            (-1, -1),
            (-100, -1),
            (-.001, -1),
            (0, 0),
            (0.0, 0),
            (0.001, 1),
            (1, 1),
            (1812, 1),
    ]

    _solution = CS(
"""def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0""")

# TODO: could try to intercept stdout to actually check this I guess?
class PluralizationProblem(ThoughtExperiment):

    _solution = """A straightforward (and totally fine) solution is to replace the original `print` call with:

```python
if total_candies == 1:
    print("Splitting 1 candy")
else:
    print("Splitting", total_candies, "candies")
```

Here's a slightly more succinct solution using a conditional expression:

```python
print("Splitting", total_candies, "candy" if total_candies == 1 else "candies")
```"""

class WeatherDebug(EqualityCheckProblem):

    _vars = ['have_umbrella', 'rain_level', 'have_hood', 'is_workday']
    # Default EqualityCheckProblem logic says that if any vars haven't changed
    # from their initial/default values then the problem isn't attempted. Which
    # doesn't work here...
    #_default_values = [True, 0.0, True, True]

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

    def check(self, *args):
        expected = self.canonical_prepared(*args)
        actual = self.ill_prepared(*args)
        assert actual != expected, ("Given {}, `prepared_for_weather` returned"
                " `{}`. But I think that's correct. (We want inputs that lead to"
                " an incorrect result from `prepared_for_weather`.)").format(
                        format_args(self.ill_prepared, args),
                        repr(actual),
                        )


class ConciseIsNegative(FunctionProblem):
    # NB: looks like there's no clean way to check for single-line-ness. 
    # But they'll know whether they've accomplished it or not, and there's not much
    # point in cheating.

    _var = 'concise_is_negative'

    _test_cases = [
            (1, False),
            (0, False),
            (-100, True),
    ]

    _hint = ("If the value of the expression `number < 0` is `True`, then we return"
            " `True`. If it's `False`, then we return `False`...")
    _solution = CS("return number < 0")

class AllToppings(FunctionProblem):
    _var = 'wants_all_toppings'

    _hint = "You'll need to use the `and` operator."
    _solution = CS("return ketchup and mustard and onion")

    _test_cases = [
            ((True, True, True), True),
            ((False, True, True), False),
            ((False, False, False), False),
            ((True, False, True), False),
            ((True, True, False), False),
    ]

class PlainDog(FunctionProblem):
    _var = 'wants_plain_hotdog'

    _hint = "You'll need to use the `not` operator."
    _solution = (
"""One solution looks like:
```python
return not ketchup and not mustard and not onion
```

We can also ["factor out" the nots](https://en.wikipedia.org/wiki/De_Morgan%27s_laws) to get:

```python
return not (ketchup or mustard or onion)
```""")

    _test_cases = [
            ((True, True, True), False),
            ((False, True, True), False),
            ((False, False, False), True),
            ((True, False, True), False),
            ((False, False, True), False),
            ((False, True, False), False),
    ]

class OneSauce(FunctionProblem):
    _var = 'exactly_one_sauce'

    _hint = ("There are exactly two ways to set ketchup and mustard to make this"
            " true. What are they?"
            )
    _solution = CS("return (ketchup and not mustard) or (mustard and not ketchup)")

    _test_cases = [
            ((True, True, True), False),
            ((False, True, True), True),
            ((False, False, False), False),
            ((True, False, True), True),
    ]

HotDogGauntlet = MultipartProblem(
        AllToppings, PlainDog, OneSauce,
        )

class OneTopping(FunctionProblem):
    _var = 'exactly_one_topping'

    _hint = ("You may have already found that `int(True)` is 1, and `int(False)` is 0."
            " Think about what kinds of basic arithmetic operations you might want to"
            " perform on `ketchup`, `mustard`, and `onion` after converting them to integers."
            )
    _solution = ("""This condition would be pretty complicated to express using just `and`, `or` and `not`, but using boolean-to-integer conversion gives us this short solution:
```python
return (int(ketchup) + int(mustard) + int(onion)) == 1
```

Fun fact: we don't technically need to call `int` on the arguments. Just by doing addition with booleans, Python implicitly does the integer conversion. So we could also write...

```python
return (ketchup + mustard + onion) == 1
```""")
    
    _test_cases = [
            ((True, True, True), False),
            ((False, True, True), False),
            ((False, False, False), False),
            ((True, False, True), False),
            ((False, False, True), True),
    ]

class BlackJackProblem(CodingProblem):
    _counts_for_points = False
    _var = 'should_hit'


    def check(self, should_hit):
        raise Uncheckable

    def is_legacy(self, phit):
        # Check for old call signature of should_hit
        # i.e. should_hit(player_total, dealer_total, player_aces):
        sig = inspect.signature(phit)
        nparams = len(sig.parameters)
        assert nparams in (3, 4), ("Unexpected call signature for should_hit:"
                " `{}`\n(Did you add or remove parameters?)").format(
                        ', '.join(sig.parameters.keys())
                        )
        return nparams == 3


    @injected
    def simulate_one_game(self, phit):
        game = BlackJack(phit, True, self.is_legacy(phit))
        game.play()

    @injected
    def simulate(self, phit, n_games=100):
        wins = 0
        legacy = self.is_legacy(phit)
        for _ in range(n_games):
            wins += 1 == BlackJack(phit, legacy=legacy).play()
        print("Player won {} out of {} games (win rate = {:.1%})".format(
            wins, n_games, wins/n_games
            ))

qvars = bind_exercises(globals(), [
    SignFunctionProblem,
    PluralizationProblem,
    WeatherDebug,
    ConciseIsNegative,
    HotDogGauntlet,
    OneTopping,
    BlackJackProblem,
    ],
)
__all__ = list(qvars)

import random

from learntools.core import *

class EarlyExitDebugging(FunctionProblem):
    _var = 'has_lucky_number'

    _test_cases = [
            ([], False),
            ([7], True),
            ([14], True),
            ([3, 14], True),
            ([3, 21, 4], True),
            ([7, 7, 7], True),
            ([3], False),
            ([3, 4, 5], False),
    ]

    _hint = ("How many times does the body of the loop run for a list"
            " of length n? (If you're not sure, try adding a `print()`"
            " call on the line before the `if`.)")

    _solution = """Remember that `return` causes a function to exit immediately. So our original implementation always ran for just one iteration. We can only return `False` if we've looked at every element of the list (and confirmed that none of them are lucky). Though we can return early if the answer is `True`:

```python
def has_lucky_number(nums):
    for num in nums:
        if num % 7 == 0:
            return True
    # We've exhausted the list without finding a lucky number
    return False
```

Here's a one-line version using a list comprehension with Python's `any` function (you can read about what it does by calling `help(any)`):

```python
def has_lucky_number(nums):
    return any([num % 7 == 0 for num in nums])
```
"""

class ElementWiseComparison(FunctionProblem):
    _var = 'elementwise_greater_than'

    _test_cases = [
            ( ([1, 2, 3, 4], 2), [False, False, True, True] ),
            ( ([1, 2, 3, 4], 5), [False, False, False, False] ),
            ( ([], 2), [] ),
            ( ([1, 1], 0), [True, True] ),
    ]

    _solution = """Here's one solution:
```python
def elementwise_greater_than(L, thresh):
    res = []
    for ele in L:
        res.append(ele > thresh)
    return res
```

And here's the list comprehension version:
```python
def elementwise_greater_than(L, thresh):
    return [ele > thresh for ele in L]
```
"""

class BoringMenu(FunctionProblem):
    _var = 'menu_is_boring'

    _test_cases = [
            ( ['Egg', 'Spam',], False),
            ( ['Spam', 'Eggs', 'Bacon', 'Spam'], False),
            ( ['Spam', 'Eggs', 'Spam', 'Spam', 'Bacon', 'Spam'], True),
            ( ['Spam', 'Spam'], True),
            ( ['Lobster Thermidor aux crevettes with a Mornay sauce, garnished with truffle pâté, brandy and a fried egg on top', 'Spam'], False),
            ( ['Spam'], False),
            ( [], False),
    ]

    _hint = ("This is a case where it may be preferable to iterate over the *indices* of the list (using a call to `range()`) rather than iterating over the elements of the list itself. When indexing into the list, be mindful that you're not \"falling off the end\" (i.e. using an index that doesn't exist).")

    # TODO: I don't think I want to mention any of the more 'clever' solutions involving zip or itertools. Though it depends on whether
    # we end up covering zip in the tutorial notebook.
    _solution = """

```python
def menu_is_boring(meals):
    # Iterate over all indices of the list, except the last one
    for i in range(len(meals)-1):
        if meals[i] == meals[i+1]:
            return True
    return False
```

The key to our solution is the call to `range`. `range(len(meals))` would give us all the indices of `meals`. If we had used that range, the last iteration of the loop would be comparing the last element to the element after it, which is... `IndexError`! `range(len(meals)-1)` gives us all the indices except the index of the last element.

But don't we need to check if `meals` is empty? Turns out that `range(0) == range(-1)` - they're both empty. So if `meals` has length 0 or 1, we just won't do any iterations of our for loop.
"""

# Analytic solution for expected payout =
# .005 * 100 + (.05 - .005) * 5 + (.25 - .05) * 1.5
def play_slot_machine():
    r = random.random()
    if r < .005:
        return 100
    elif r < .05:
        return 5
    elif r < .25:
        return 1.5
    else:
        return 0

# TODO: Could probably make this checkable.
class ExpectedSlotsPayout(ThoughtExperiment):
    #_var = 'estimate_average_slot_payout'
    _solution = """
    
The exact expected value of one pull of the slot machine is 0.025 - i.e. a little more than 2 cents.  See?  Not every game in the Python Challenge Casino is rigged against the player!

In order to get this answer, you'll need to implement the `estimate_average_slot_payout(n_runs)` function to simulate pulling the slot machine `n_runs` times.  It should return the payout averaged over those `n_runs`.

Then, once the function is defined, in order to estimate the average slot payout, we need only call the function.

Because of the high variance of the outcome (there are some very rare high payout results that significantly affect the average) you might need to run your function with a very high value of `n_runs` to get a stable answer close to the true expectation.  For instance, you might use a value for `n_runs` of 1000000.

Here's an example for how the function could look:
```python
def estimate_average_slot_payout(n_runs):
    # Play slot machine n_runs times, calculate payout of each
    payouts = [play_slot_machine()-1 for i in range(n_runs)]
    # Calculate the average value
    avg_payout = sum(payouts) / n_runs
    return avg_payout
    
estimate_average_slot_payout(10000000)

```

This should return an answer close to 0.025!
            
"""

class SlotsSurvival(FunctionProblem):
    _bonus = True
    _var = 'slots_survival_probability'
    
    _solution = CS("""def slots_survival_probability(start_balance, n_spins, n_simulations):
    # How many times did we last the given number of spins?
    successes = 0
    # A convention in Python is to use '_' to name variables we won't use
    for _ in range(n_simulations):
        balance = start_balance
        spins_left = n_spins
        while balance >= 1 and spins_left:
            # subtract the cost of playing
            balance -= 1
            balance += play_slot_machine()
            spins_left -= 1
        # did we make it to the end?
        if spins_left == 0:
            successes += 1
    return successes / n_simulations""")

    def check(self, fn):
        actual = fn(10, 10, 1000)
        assert actual == 1.0, "Expected `slots_survival_probability(10, 10, 1000)` to be 1.0, but was actually {}".format(repr(actual))
        
        actual = fn(1, 2, 10000)
        assert .24 <= actual <= .26, "Expected `slots_survival_probability(1, 2, 10000)` to be around .25, but was actually {}".format(repr(actual))

        actual = fn(25, 150, 10000)
        assert .22 <= actual <= .235, "Expected `slots_survival_probability(25, 150, 10000)` to be around .228, but was actually {}".format(repr(actual))


qvars = bind_exercises(globals(), [
    EarlyExitDebugging,
    ElementWiseComparison,
    BoringMenu,
    ExpectedSlotsPayout,
    SlotsSurvival,
    ],
)
__all__ = list(qvars) + ['play_slot_machine']

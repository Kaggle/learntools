import random

from learntools.core import *

import learntools.python.solns.jimmygraph as jg_module
import learntools.python.solns.blackjack_gt as bj_module
hand_gt_soln = bj_module.blackjack_hand_greater_than

class JimmySlots(ThoughtExperiment):
    _solution = CS.load(jg_module.__file__)

class LuigiAnalysis(ThoughtExperiment):
    _hint = ("A couple things to consider:\n\n"
            "- What is the type of variable `i`?\n"
            "- What happens if you inspect the `full_dataset` list you imported?"
            " (Don't worry, it's not actually that big.) Can you find the racer"
            " that's causing the error?"
            )

    _solution = '''Luigi used the variable name `i` to represent each item in racer['items'].
However, he also used `i` as the loop variable for the outer loop (`for i in range(len(racers))`).
These i's are clobbering each other. This becomes a problem only if we encounter a racer
with a finish of 1 and a name of `None`. If that happens, when we try to print the "WARNING" message,
`i` refers to a string like "green shell", which python can't add to an integer, hence a `TypeError`.

This is similar to the issue we saw when we imported * from `math` and `numpy`. They both contained variables called `log`, and the one we got when we tried to call it was the wrong one.

We can fix this by using different loop variables for the inner and outer loops. `i` wasn't a very
good variable name for the inner loop anyways. `for item in racer['items']` fixes the bug and is 
easier to read.

Variable shadowing bugs like this don't come up super often, but when they do they can take an infuriating amount of time to diagnose!
'''

def gen_bj_hand():
    cards = list(map(str, range(2, 11))) + ['J', 'Q', 'K', 'A']
    ncards = random.randint(1, 6)
    hand = [random.choice(cards) for _ in range(ncards)]
    return hand

def gen_bj_inputs(n):
    random.seed(1)
    return [
            (gen_bj_hand(), gen_bj_hand())
            for _ in range(n)
            ]

class BlackjackCmp(FunctionProblem):
    _var = 'blackjack_hand_greater_than'
    _hint = ("This problem is a lot easier to solve if you define at least one 'helper' function."
            " The logic for calculating a hand's total points is a good candidate for extracting into a helper function."
            )
    _solution = CS.load(bj_module.__file__)

    # TODO: explicitly make sure to test multi-ace cases. e.g. [K, A, A]
    _test_cases = [
            (args, hand_gt_soln(*args))
            for args in gen_bj_inputs(100)
            ]


qvars = bind_exercises(globals(), [
    JimmySlots,
    LuigiAnalysis,
    BlackjackCmp,
    None,
    ],
    start=1,
)
__all__ = list(qvars)

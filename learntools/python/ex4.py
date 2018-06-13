from learntools.python.utils import bind_exercises, format_args
from learntools.python.problem import *
from learntools.python.richtext import *
CS = CodeSolution

# Complete fn that takes a list and returns the second element

class SelectSecondItem(FunctionProblem):
    '''TODO: Wrap index errors'''
    _var = 'select_second'

    _test_cases = [
            ([1, 2, 3], 2),
            ([[1], [2], [4]], [2]),
            (list(range(10)), 1),
    ]

    _hint = "Python starts counting at 0. So the second item isn't indexed with a 2"

    _solution = CS(
"""def select_second(L):
    return L[1]""")

class LosingTeamCaptain(FunctionProblem):
    _var = 'losing_team_captain'

    _test_cases = [
            ([["Paul", "John", "Ringo", "George"]], "John"),
            ([["Paul", "John", "Ringo", "George"], ["Jen", "Jamie"]], "Jamie"),
            ([["Who", "What", "I don't Know", "I'll tell you later"], ["Al", "Bonnie", "Clyde"]], "Bonnie"),
    ]

    _hint = ("The last item in a list a can be selected with a[-1]."
             "The first item in the first sublist would be selected as a[0][0]"
             )

    _solution = CS(
"""def losing_team_captain(teams):
    return teams[-1][1]""")

class PurpleShell(FunctionProblem):

    _var = 'purple_shell'


    _hint = ("Your function should change the list it receives, but not return anything\n\n"
            "You can store an item to a temporary variable so it isn't overwritten"
             "when you swap into that part of the list.\n Use -1 to index into the last"
             "item in the list."
             )

    def _do_check(cls, fn):
        lists = (["M","L"],
                 ["M","L","J"],
                 [1,2,3,4,5]
                )
        def sol_fn(x): x[0], x[-1] = x[-1], x[0]
        for l in lists:
            copy_for_soln_fn = l.copy()
            copy_for_user_fn = l.copy()
            sol_fn(copy_for_soln_fn) # create desired output for comparison
            user_output = fn(copy_for_user_fn) # also applies swap in this line
            assert(type(user_output) == type(None)), ("Your function should not return anything."
                                                      "Instead, change the list without returning it.")
            assert copy_for_user_fn == copy_for_soln_fn, \
                "Expected " + copy_for_soln_fn  + " on list " + l + \
                ".\nGot " + copy_for_user_fn + " instead."



    _solution = CS(
"""def purple_shell(racers):
    # One slick way to do the swap is x[0], x[-1] = x[-1], x[0].
    temp = racers[0]
    racers[0] = racers[-1]
    racers[-1] = temp
    return""")

class UnderstandLen(Problem):
    '''TODO: Wrap index errors'''
    _var = 'understand_len'

    _hint = "Use len to check the lengths of the lists. Call the solution function for an explanation"

    _solution = CS(
"""[1, 2, 3] - There are three items in this list. Nothing tricky yetself.
[1, [2, 3]] - The list [2, 3] counts as a single item. It has one item before it. So we have 2 items in the list
[] - The empty list has 0 items
[1, 2, 3][1:] - The expression is the same as the list [2, 3], which has length 2.""")

qvars = bind_exercises(globals(), [
    SelectSecondItem,
    LosingTeamCaptain,
    PurpleShell,
    UnderstandLen
    ],
)
__all__ = list(qvars)

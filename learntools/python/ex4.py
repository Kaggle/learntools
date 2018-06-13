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
"""def select_second(x):
    return x[1]""")

class SecondItemLastSublist(FunctionProblem):
    _var = 'second_item_last_sublist'

    _test_cases = [
            ([[0, 1, 2]], 1),
            ([[1,2], [[[1], [2]]]], [2]),
            ([[1], [2,3], [4,5,6]], 5),
    ]

    _hint = ("The last item in a list a can be selected with a[-1]."
             "The first item in the first sublist would be selected as a[0][0]"
             )

    _solution = CS(
"""def second_item_last_sublist(x):
    return x[-1][1]""")

class SwapFirstLast(FunctionProblem):

    _var = 'swap_first_last'


    _hint = ("Your function should change the list it receives, but not return anything\n\n"
            "You can store an item to a temporary variable so it isn't overwritten"
             "when you swap into that part of the list.\n Use -1 to index into the last"
             "item in the list."
             )

    def _do_check(cls, fn):
        lists = ([1,2],
                 [1,1],
                 [[1],[2]],
                 [1,2,3,4,5]
                )
        def sol_fn(x): x[0], x[-1] = x[-1], x[0]
        for l in lists:
            copy_for_soln_fn = l.copy()
            copy_for_user_fn = l.copy()
            sol_fn(copy_for_soln_fn) # create desired output for comparison
            fn_output = fn(copy_used_by_user_fn) # also applies swap in this line
            assert(type(fn_output) == NoneType), "Your function should not return anything"
            assert copy_for_user_fn == copy_for_soln_fn, \
                "Failed on list " + l + \
                ". Expected " + copy_for_soln_fn  + \
                ". Your function created " + copy_for_user_fn



    _solution = CS(
"""def swap_first_last(x):
    # One slick way to do the swap is x[0], x[-1] = x[-1], x[0].
    temp = x[0]
    x[0] = x[-1]
    x[-1] = temp
    return""")

qvars = bind_exercises(globals(), [
    SelectSecondItem,
    SecondItemLastSublist,
    SwapFirstLast,
    ],
)
__all__ = list(qvars)

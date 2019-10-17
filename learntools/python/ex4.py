from learntools.core import *

# Complete fn that takes a list and returns the second element

class SelectSecondItem(FunctionProblem):
    #TODO: Wrap index errors
    _var = 'select_second'

    _test_cases = [
            ([1, 2, 3], 2),
            ([[1], [2], [4]], [2]),
            (list(range(10)), 1),
            ([1], None),
            ([], None),
    ]

    _hint = "Python starts counting at 0. So the second item isn't indexed with a 2"

    _solution = CS(
"""def select_second(L):
    if len(L) < 2:
        return None
    return L[1]""")

class LosingTeamCaptain(FunctionProblem):
    _var = 'losing_team_captain'

    _test_cases = [
            ([["Paul", "John", "Ringo", "George"]], "John"),
            ([["Paul", "John", "Ringo", "George"], ["Jen", "Jamie"]], "Jamie"),
            ([["Who", "What", "I don't Know", "I'll tell you later"], ["Al", "Bonnie", "Clyde"]], "Bonnie"),
    ]

    _hint = ("The last item in a list `L` can be selected with `L[-1]`."
             " The first item in the first sublist would be selected as `L[0][0]`"
             )

    _solution = CS(
"""def losing_team_captain(teams):
    return teams[-1][1]""")

class PurpleShell(FunctionProblem):

    _var = 'purple_shell'


    _hint = ("Your function should change the list it receives, but not return anything\n\n"
            "To swap the list elements, think back to the code you used in the very first exercise to swap"
            " two variables."
             )

    def check(self, fn):
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
                                                      " Instead, change the list without returning it.")
            assert copy_for_user_fn == copy_for_soln_fn, (
                    "After running function on list {} expected its new value to be {}"
                    " but actually was {}").format(repr(l), repr(copy_for_soln_fn), repr(copy_for_user_fn))



    _solution = CS(
"""def purple_shell(racers):
    # One slick way to do the swap is x[0], x[-1] = x[-1], x[0].
    temp = racers[0]
    racers[0] = racers[-1]
    racers[-1] = temp""")

class UnderstandLen(EqualityCheckProblem):
    _var = 'lengths'
    _expected = [3, 2, 0, 2]
    _default_values = [ [] ]

    _hint = "Use len to check the lengths of the lists. Call the solution function for an explanation"

    _solution = (
            """
- a: There are three items in this list. Nothing tricky yet.
- b: The list `[2, 3]` counts as a single item. It has one item before it. So we have 2 items in the list
- c: The empty list has 0 items
- d: The expression is the same as the list `[2, 3]`, which has length 2.""")

class FashionablyLate(FunctionProblem):
    _var = 'fashionably_late'



    _test_cases = [
            ((['Adela', 'Fleda', 'Owen', 'May', 'Mona', 'Gilbert', 'Ford'], "Adela"), False),
            ((['Adela', 'Fleda', 'Owen', 'May', 'Mona', 'Gilbert', 'Ford'], "Fleda"), False),
            ((['Adela', 'Fleda', 'Owen', 'May', 'Mona', 'Gilbert', 'Ford'], "Owen"), False),
            ((['Adela', 'Fleda', 'Owen', 'May', 'Mona', 'Gilbert', 'Ford'], "May"), False),
            ((['Adela', 'Fleda', 'Owen', 'May', 'Mona', 'Gilbert', 'Ford'], "Mona"), True),
            ((['Adela', 'Fleda', 'Owen', 'May', 'Mona', 'Gilbert', 'Ford'], "Gilbert"), True),
            ((['Adela', 'Fleda', 'Owen', 'May', 'Mona', 'Gilbert', 'Ford'], "Ford"), False),
            ((["Paul", "John", "Ringo", "George"], "John"), False),
            ((["Paul", "John", "Ringo", "George"], "Ringo"), True),
            ((["Lebron", "Kevin"], "Lebron"), False),
            ((["Lebron", "Kevin"], "Kevin"), False),
    ]

    _hint = ("Use the index method to find when the person arrived. Check whether "
            "that is a fashionably late spot given the list length (`len`). Think about 0-indexing"
             )

    _solution = CS(
"""def fashionably_late(arrivals, name):
    order = arrivals.index(name)
    return order >= len(arrivals) / 2 and order != len(arrivals) - 1""")

class CountNegativesRiddle(FunctionProblem):
    _bonus = True
    _var = 'count_negatives'

    _test_cases = [
            ([], 0),
            ([0, -1, -1], 2),
            ([3, -3, 2, -1, 4, -4, 5, 5], 3),
            ([1, 2, 3, 4, 5, 0], 0),
    ]

    _hint = ('Can you think of a way you could solve this problem if the input list'
            ' was guaranteed to be sorted and guaranteed to contain 0?')

    _solution = """
Here's a non-obvious solution using only tools shown in the tutorial notebook:
```python
def count_negatives(nums):
    nums.append(0)
    # We could also have used the list.sort() method, which modifies a list, putting it in sorted order.
    nums = sorted(nums)
    return nums.index(0)
```

The above implementation relies on the fact that `list.index` returns the index of the *first* occurrence of a value. (You can verify this by calling `help(list.index)`.) So if, after sorting the list in ascending order, the value 0 is at index 0, then the number of negatives is 0. If 0 is at index 2 (i.e. the third element), then there are two elements smaller than 0. And so on.

*Note*: it's usually considered "impolite" to modify a list that someone passes to your function without giving them some warning (i.e. unless the docstring says that it modifies its input). So, if we wanted to be nice, we could have started by making a copy of nums using the `list.copy()` method (e.g. `our_nums = nums.copy()`), and then working with that copy rather than the original.

If you're a big Lisp fan, you might have written this technically compliant solution (we haven't talked about recursion, but I guess this doesn't use any syntax or functions we haven't seen yet...):

```python
def count_negatives(nums):
    # Equivalent to "if len(nums) == 0". An empty list is 'falsey'.
    if not nums:
        return 0
    else:
        # Implicitly converting a boolean to an int! See question 6 of the
        # exercise on booleans and conditionals
        return (nums[0] < 0) + count_negatives(nums[1:])
```"""


qvars = bind_exercises(globals(), [
    SelectSecondItem,
    LosingTeamCaptain,
    PurpleShell,
    UnderstandLen,
    FashionablyLate,
    CountNegativesRiddle,
    ],
)
__all__ = list(qvars)

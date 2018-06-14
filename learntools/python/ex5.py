from learntools.python.utils import bind_exercises
from learntools.python.problem import *
from learntools.python.richtext import *
CS = CodeSolution

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

qvars = bind_exercises(globals(), [
    EarlyExitDebugging,
    ElementWiseComparison,
    BoringMenu,
    ],
)
__all__ = list(qvars)

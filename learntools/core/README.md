The easiest way to get started implementing exercises using the `learntools.core` API is probably to look at some examples and emulate them. There are a number of exercises of various types implemented in `learntools.python` - you can see them in action in the "testing" notebooks in `learntools/python/nbs/`. But below is a bit of a more formal introduction.

# Implementing an exercise

I'll be using the term "exercise" to refer to a hands-on interactive notebook containing 1 or more "problems".

To implement an exercise, you'll need to do the following:

1. Create a python module for your exercise. It should contain definitions for one or more Problem subclasses, and end with a call to `learntools.core.bind_exercises`.
2. Create a notebook. It should begin with a code cell containing a few lines of boilerplate setup code. For each problem, there should probably be some markdown cell(s) describing the problem, then some starter code including some (possibly commented) calls to the check/hint/solution methods of the corresponding Problem(View) object.
3. (Optional but recommended) Make a fork of the above notebook for testing.

(You can do 1 and 2 in any order, or interleave work on them. I'm going to start by describing 2 in more detail.)

# Writing an exercise notebook

Closing the loop between Kernels and updated learntools code is a fairly tedious process. My recommended workflow is to develop exercise notebooks locally then upload to kernels as a final step.

## Setup code

Your notebook should begin with a code cell having some boilerplate setup code that looks like...

```python
from learntools.core import binder
binder.bind(globals())
from learntools.spam.spam_exercise import *
```

This will import variables like `q1, q2, q3`... (you can use the `var_format` kwarg to `bind_exercises` to get variables of a different format e.g. `step_n`, `problem_n`, etc.). Each variable corresponds to a problem defined in your exercise module (technically it refers to an object of type `ProblemView`).

## Interacting with problems

A standard problem can be interacted with in up to three ways:

- `q1.check()`, checks the student's code. It will display a message corresponding to one of three outcomes: correct, incorrect, or not attempted (if we can detect that the starter code hasn't been touched).
- `q1.hint()`, displays a hint. In some cases (if you define a `_hints` list of more than 1 element in your `Problem`), the student will be prompted to call `q1.hint(2)`, `q1.hint(3)`, etc. if they need further hints.
- `q1.solution()` displays the solution to question 1. This may be just in the form of a code snippet,or may also include some (markdown) explanatory prose.

## Problem starter code

After any markdown describing the cell, I recommend having a code cell with starter code for the problem, ending with a call to `qn.check()`. e.g.

```python
pi = 3.14159 # approximate
diameter = 3
# Create a variable called 'radius' equal to half the diameter

# Create a variable called 'area', using the formula for the area of
# a circle: pi times the radius squared
q1.check()
```

I recommend following that with one or two code cells with commented-out calls to `q1.hint()` and `q1.solution()`.

# Writing an exercise module - defining Problems

The majority of the work in writing an exercise module is defining a `learntools.core.Problem` subclass for each of your problems. Your `Problem` is essentially responsible for taking care of the three forms of interaction described above - checking code, hinting, and showing solutions.

## Hints

All problems may define a `_hint` class attribute containing a markdown string.

You may instead specify a list of markdown strings in `_hints`. If you do this, then when the student calls `qn.hint()`, they'll see the first hint, and a prompt like "if you'd like another hint, call `qn.hint(2)`". 

Hints are optional. If none is defined and the student tries to call `qn.hint()`, they'll see a message like "Sorry, no hints available for this question".

## Solutions

All problems should define a `_solution` class attribute. If your solution is just in the form of code, you can create a `learntools.core.CodeSolution`, passing the source to its constructor. This will render it in a code block with Python syntax highlighting.

If the solution is more than a couple lines, you might want to actually write it out in a separate module. If you do this, check out the `CodeSolution.load()` helper (see `learntools/python/ex7.py` for an example of it in use).

Otherwise, `_solution` should be a markdown string.

## Checking

This is the aspect of problem definition with the most potential for complication. There are a number of abstract `Problem` subclasses defined in `learntools/core/problem.py` (you'll rarely write a concrete `Problem` subclass that inherits directly from `Problem`). What distinguishes these abstract subclasses is mostly how they approach checking. Below is a rundown of those subclasses.

### No checking / code interaction? `ThoughtExperiment`

A `ThoughtExperiment` has a solution (and probably a hint), but no checking logic. If the student calls `qn.check()`, they'll get an appropriate failure message.

(Occasionally you may want to implement a problem without checking but which has some code interaction, in which case you'd inherit from `CodingProblem`. See `BlackjackProblem` in the python track for an example. See also the 'custom interactions' section below.) 

### Checking one or more variables against static expected values? `EqualityCheckProblem`

A `EqualityCheckProblem` has a variable name (`_var`) or names (`_vars`), and corresponding expected values, `_expected`.

In the common case where the problem involves defining a single variable, `_expected` can be a simple scalar value rather than a list of length 1. Otherwise, `_expected` should be a list of values of the same length as `_vars` and in the same order.

When the student calls `qn.check()` we'll say their answer is correct iff it matches `_expected` (within some tolerance, in the case of floats). By default, the failure message will tell them the first value whose variable was wrong as well as the offending value - it will not tell them the expected value.

### Checking the implementation of a function? `FunctionProblem`

A `FunctionProblem` should have a `_var` member with the name of the function the student is to implement.

It should define a `_test_cases` member, containing a list of (input, expected-output) pairs, where input may be a scalar (for unary functions) or tuple of args. 

### else: `CodingProblem`

The above abstract classes provide convenient shortcuts for defining a problem class without having to explicitly implement the checking logic. When they aren't up to the task, you can always implement a `check` method on your `Problem` subclass. See the docstring for `Problem.check` for the semantics of this method.

If you're overriding `Problem.check`, you will probably want to inherit from `CodingProblem`.

A common use case is a problem where the student has to create or modify one or more variables, but correctness can't be reduced to an equality check. In this case, you can implement `check` to do more granular inspection of those variables - e.g. asserting that a DataFrame has a column of a certain name, or that a numpy array has a certain shape, or that a model has been fit.

## Custom interactions

Occasionally you may want to attach some custom functionality to your problem which can be invoked by the student in the exercise notebook. See for example the `VariableSwap` question in the Python track, with its `store_original_ids` method.

Any methods of your `Problem` not marked with a leading underscore (which are taken to be for internal use) will be callable by the user. e.g. if you define a `spam` method, the user will be able to invoke `qn.spam()` in the exercise notebook.

## A note on injected arguments

All `CodingProblem` subclasses define a `_var` or `_vars` to indicate the names of the variables (from the exercise notebook's namespace) which are of interest to this problem. The standard methods `check` and `check_whether_attempted` will receive the values of those variables as arguments when called. If any of the variables are undefined (or if a `_default_values` member is defined, and all current values match those) any call to `check()` will be aborted, and the user will get an Incorrect/NotAttempted message with a hopefully-useful message about which variables they still need to define.

If you define a custom method on your problem which you'd like to also receive injected arguments when called, mark it with the `@injected` decorator, defined in `learntools.core.problem`.

## `bind_exercises`

Exercise notebooks end with some boilerplate that looks something like...

```python
qvars = bind_exercises(globals(), [
    JimmySlots,
    LuigiAnalysis,
    BlackjackCmp,
    ],
)
__all__ = list(qvars)
```

The net effect of this is to instantiate instances of the given problem classes, assign them to a regularly named sequence of variables (e.g. q1, q2, q3), and make it so that `from my_exercise_module import *` imports precisely those auto-generated variables. You can check out `bind_exercises` and its docstring if you want more of the gory details.

# Interaction/Progress Tracking

For the most part, you shouldn't need to worry about this when creating problems/exercises.

One consideration: by default, a problem 'counts' for the purposes of progress tracking iff it's not a `ThoughtExperiment`. To explicitly control this (e.g. if you have a non-checkable `CodingProblem`), set the class attribute `_counts_for_points`.

Set `_bonus = True` to mark a problem as being a bonus (i.e. the user doesn't need to get the question right in order to pass this exercise and earn a checkmark).

Sending tracking events is managed at the `ProblemView` layer. See `problem_view.py` and `tracking.py` for details.


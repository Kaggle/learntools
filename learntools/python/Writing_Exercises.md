
# Writing Exercises

An exercise consists of one or more `Problem` objects. `Problem` and its generic subclasses are defined in `problem.py`.

## Defining a `Problem`

In general, a `Problem` has 3 public API methods. Subclass implementers must do a bit of work corresponding to each of these 3 methods:

- **hint**: your subclass should define exactly one of the class attributes `_hint` or `_hints`. The latter is a list of strings which will each be wrapped in a Hint object and displayed sequentially on calling `problem.hint()`, `problem.hint(2)`, `problem.hint(3)`, etc. `_hint` is a single string - a convenience for the most common scenario when a problem has only one hint.
- **solution**: your subclass should define the class attribute `_solution`. This may be a richtext.Solution instance, or a string, or list of strings (each representing one line of text/code). The latter 2 cases will end up wrapped in a richtext.Solution.
- **check**: Subclasses must implement `_do_check` (see docstring), and should probably implement `is_attempted`. This is typically a lot of work compared to the above 2 requirements. Most `Problem` subclasses exist to reduce the amount of code you have to write for checking.

Some generic `Problem` subclasses are briefly described below.

### ThoughtExperiment

A `Problem` with no checking logic! Subclasses only need to worry about providing hints and solutions.

### FunctionProblem

A problem that asks the user to define a function (or, to be more precise, fill in the body of a function we've defined).

Subclasses just need to provide a list of test cases of the form `(input, expected_output)`.

**TODO**: write some stuff about globals binding, arg injection for check/is\_attempted, \_var/\_vars and so on.

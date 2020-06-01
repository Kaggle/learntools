from learntools.core import *

class Q1(ThoughtExperiment):
    _solution = "This is the solution!"

    
class Q2(EqualityCheckProblem):
    _var = "a_variable"
    _expected = 12
    _hint = "What is ten plus two?"
    _solution = CS(
"""
a_variable = 10 + 2
""")

class Q3(FunctionProblem):
    _var = "a_function"
    _test_cases = [
        (-1, 1),
        (1, 1),
        (0, 0),
    ]
    _hint = "It is the absolute value function."
    _solution = CS("a_function = lamda x: abs(x)")

class Q4(CodingProblem):
    _hint = "You want to import the math module."
    _solution = CS("import math")
    def check(self):
        pass

class Q5A(CodingProblem):
    _vars = ['function_1', 'variable_1']
    _hint = "."
    _solution = CS("""
def function_1(var):
    return var + 1

variable_1 = 3
""")
    def check(self, function_1, variable_1):
        correct_answer = 4
        print("Checking your answer.")
        your_answer = function_1(variable_1)
        assert (your_answer is not None), ("You didn't return an answer!")
        assert (your_answer-1 < 4), ("{} is too big!".format(your_answer))
        assert (your_answer+1 > 4), ("{} is too small!".format(your_answer))
        print("The value of `correct_answer` is {}.".format(correct_answer))


class Q5B(FunctionProblem):
    _hint = "This is a hint."
    _solution = "This is the solution."

Q5 = MultipartProblem(Q5A, Q5B)


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4, Q5,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)

from learntools.core import *
import tensorflow as tf


class Q1(ThoughtExperiment):
    _solution = ""


class Q2(ThoughtExperiment):
    _solution = ""


class Q3A(ThoughtExperiment):
    _hint = ""
    _solution = ""

class Q3B(ThoughtExperiment):
    _hint = ""
    _solution = ""

class Q3C(ThoughtExperiment):
    _hint = ""
    _solution = ""

Q3 = MultipartProblem(Q3A, Q3B, Q3C)


class Q4(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
    

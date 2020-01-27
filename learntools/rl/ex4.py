from learntools.core import *

class JustPass(CodingProblem):
    _congrats = ""
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    JustPass
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
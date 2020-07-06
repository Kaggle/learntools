from learntools.core import *

class InternetOn(CodingProblem):
    _hint = ""
    _solution = ""
    _congrats = "Setup complete."
    _correct_message = ""
    def check(self):
        pass 

qvars = bind_exercises(globals(), [
    InternetOn
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)

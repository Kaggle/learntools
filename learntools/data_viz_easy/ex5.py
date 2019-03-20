from learntools.core import *

class Completion(CodingProblem):
    def check(self):
        pass    

qvars = bind_exercises(globals(), [
    Completion
    ],
    tutorial_id=193,
    var_format='step_{n}',
    )
__all__ = list(qvars)

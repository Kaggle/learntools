from learntools.core import *

class NumLeaves(EqualityCheckProblem):
    _var = num_leaves
    _expected = 7**3
    _hint =  "Try drawing the game tree.  How many moves (columns) are possible at each turn?"
    _solution = CS("num_leaves = 7*7*7")
    
class AlphaBeta(CodingProblem):
    _var = 
    _hint = ""
    _solution = ""
    def check(self):
        pass

class JustSubmitEx3(CodingProblem):
    _hint = "Follow the instructions to submit your agent to the competition."
    _solution = "Follow the instructions to submit your agent to the competition."
    _congrats = "Thank you for submitting your agent to the competition!"
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    NumLeaves, 
    BothLose,
    JustSubmitEx3
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
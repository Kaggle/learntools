from learntools.core import *

class WorseHeuristic(ThoughtExperiment):
    _hint = ("The first heuristic assigns a score of 0 to column 2, and a score of -99 to "
             "column 3.  What scores do you get with the second heuristic?")
    _solution = ("The first heuristic is guaranteed to select column 2 to block "
                 "the opponent from winning.  The second heuristic selects either "
                 "column 2 or column 3 (where it selects each with 50% probability). "
                 "Thus, for this game board, the first heuristic is better. In general, "
                 "we can expect that the first heuristic is a better heuristic, "
                 "since we cannot trust the second heuristic to block the opponent "
                 "from winning.") 

class NumLeaves(EqualityCheckProblem):
    _var = "num_leaves"
    _expected = 7**3
    _hint =  "Try drawing the game tree.  How many moves (columns) are possible at each turn?"
    _solution = CS("num_leaves = 7*7*7")

class JustSubmitEx3(CodingProblem):
    _hint = "Follow the instructions to submit your agent to the competition."
    _solution = "Follow the instructions to submit your agent to the competition."
    _congrats = "Thank you for submitting your agent to the competition!"
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    WorseHeuristic,
    NumLeaves, 
    JustSubmitEx3
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
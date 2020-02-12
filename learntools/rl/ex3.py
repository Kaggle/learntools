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
    
class WhichMove(CodingProblem):
    _var = "selected_move"
    _hint = "For each potential move, how will the opponent respond?"
    _solution = CS("selected_move = 3")
    def check(self, ans):
        try: 
            move = int(ans)
        except:
            assert 1==0, "Your answer should be one of `'1'`, `'2'`, or `'3'`."
        assert move in [1, 2, 3], "Your answer should be one of `'1'`, `'2'`, or `'3'`."
        assert move == 3, "{} is incorrect.  Please try again.".format(move)
        
class Assumptions(ThoughtExperiment):
    _hint = "hi"
    _solution = "yo!"

class JustSubmitEx3(CodingProblem):
    _hint = "Follow the instructions to create an agent."
    _solution = "Follow the instructions to create an agent."
    _congrats = "Thank you for creating an agent!"
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    WorseHeuristic,
    NumLeaves, 
    WhichMove,
    Assumptions,
    JustSubmitEx3
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
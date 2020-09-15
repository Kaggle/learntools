from learntools.core import *

class PickBestOption(CodingProblem):
    _var = "best_option"
    _solution = CS("best_option = 'C'")
    _correct_message = "If we use a similar network as in the tutorial, the network should output a probability for each possible move."
    def check(self, ans):
        assert ans in ['A', 'B', 'C', 'D'], "Your answer should be one of `'A'`, `'B'`, `'C'`, or `'D'`."
        assert ans == 'C', "{} is incorrect.  Please try again.".format(ans)
    
class DecideReward(ThoughtExperiment):
    _solution = ("Here's a possible solution - after each move, we give the agent a reward that tells it how well it did:\n"
                 "- If agent wins the game in that move, it gets a reward of `+1`.\n"
                 "- Else if the agent selects an invalid move, it gets a reward of `-10`.\n"
                 "- Else if it detonates a mine, it gets a reward of `-1`.\n"
                 "- Else if the agent clears a square with no hidden mine, it gets a reward of `+1/100`.\n\n"
                 "To check the validity of your answer, note that the reward for selecting an invalid move and for detonating "
                 "a mine should both be negative.  The reward for winning the game should be positive.  And, the reward for "
                 "clearing a square with no hidden mine should be either zero or slightly positive."
                )
 
qvars = bind_exercises(globals(), [
    PickBestOption,
    DecideReward
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
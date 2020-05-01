from learntools.core import *
import numpy as np
from kaggle_environments import evaluate
import random


# Calculates score if agent drops piece in selected column
def score_move(A, B, C, D, E, prev_grid, col, mark, config):
    grid = drop_piece(prev_grid, col, mark, config)
    num_twos = count_windows(grid, 2, mark, config)
    num_threes = count_windows(grid, 3, mark, config)
    num_fours = count_windows(grid, 4, mark, config)
    num_twos_opp = count_windows(grid, 2, mark%2+1, config)
    num_threes_opp = count_windows(grid, 3, mark%2+1, config)
    score = A*num_fours + B*num_threes + C*num_twos + D*num_twos_opp + E*num_threes_opp 
    return score

# Helper function for score_move: gets board at next step if agent drops piece in selected column
def drop_piece(grid, col, mark, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = mark
    return next_grid

# Helper function for get_heuristic: checks if window satisfies heuristic conditions
def check_window(window, num_discs, piece, config):
    return (window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs)
    
# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
def count_windows(grid, num_discs, piece, config):
    num_windows = 0
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    return num_windows    

def my_agent(obs, config, A, B, C, D, E):
    valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    scores = dict(zip(valid_moves, [score_move(A, B, C, D, E, grid, col, obs.mark, config) for col in valid_moves]))
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    move = random.choice(max_cols)
    return move

def get_win_percentage(agent1, agent2, n_rounds=50):
    config = {'rows': 6, 'columns': 7, 'inarow': 4}
    outcomes = evaluate("connectx", [agent1, agent2], config, [], n_rounds//2)
    outcomes += [[b,a] for [a,b] in evaluate("connectx", [agent2, agent1], config, [], n_rounds-n_rounds//2)]
    print("Your Agent's Win Percentage (in 50 game rounds):", np.round(outcomes.count([1,-1])/len(outcomes), 2))
    print("Tutorial Agent's Win Percentage (in 50 game rounds):", np.round(outcomes.count([-1,1])/len(outcomes), 2))
    exercise_agent_win_percentage = np.round(outcomes.count([1,-1])/len(outcomes), 2)
    return exercise_agent_win_percentage

########################################################################

class BetterHeuristic(CodingProblem):
    _vars = ["A", "B", "C", "D", "E"]
    _hint =  "Use the agent from the tutorial as a starting point \
    (`A = 1e6`, `B = 1`, `C = 0`, `D = 0`, `E = -1e2`)."
    _solution = CS(
"""# There are many values that can work, but here is one solution
A = 1e10
B = 1e4
C = 1e2
D = -1
E = -1e6
""")
    def check(self, A, B, C, D, E):
        random.seed(0)
        def tutorial_agent(obs, config):
            return my_agent(obs, config, 1e6, 1, 0, 0, -1e2)
        def exercise_agent(obs, config):
            return my_agent(obs, config, A, B, C, D, E)
        # C and D are nonzero
        assert C != 0, "`C` must be nonzero."
        assert D != 0, "`D` must be nonzero."
        # Check if tutorial agent is outperformed
        win_percentage = get_win_percentage(exercise_agent, tutorial_agent)
        is_outperformed = (win_percentage > .5)
        # If tutorial agent not outperformed, some tailored feedback
        failure_msg = "Your agent's win percentage was only {}\%. Your agent did not outperform the agent from the tutorial. ".format(np.round(win_percentage*100,2))
        if is_outperformed == False:
            assert A > 0, (failure_msg + "\n\n**Hint**: `A` should be a positive value, so that the agent is encouraged to win the game.")
            assert all([A > val for val in [B, C, D, E]]), (failure_msg + "\n\n**Hint**: `A` should be the largest number, so that the heuristic sees the biggest increase when the agent gets four in a row.")
            assert B > 0, (failure_msg + "\n\n**Hint**: `B` should be a positive value, so that the agent is encouraged to form this pattern.")
            assert E < 0, (failure_msg + "\n\n**Hint**: Try changing `E` to a negative value, so that the heuristic is lowered when the opponent forms this pattern.")
        assert is_outperformed == True, failure_msg
        
    
class BothLose(ThoughtExperiment):
    _hint = ("The agent only has two options: which column should the agent select "
             "to certainly win the game?")
    _solution = ("The agent has two choices: it can play in either column 0 "
                 "(the leftmost column), or column 6 (the rightmost column). "
                 "If the agent plays in column 0, it definitely wins the game "
                 "in its next move.  And, if it plays in column 6, it likely "
                 "loses the game (since, if the opponent responds by playing in "
                 "the same column, then the opponent wins the game). "
                 "\n\nIf the agent uses the heuristic **from the tutorial**, both "
                 "columns are scored equally, and so the agent will select from "
                 "them (uniformly) at random.  In this case, the agent has about "
                 "a 50/50 chance of winning the game. \n\nAs for the heuristic **that** "
                 "**you just implemented**, this will depend on your implementation, "
                 "so we'll provide an answer for the solution heuristic that we "
                 "provided -- in this case, the agent most likely loses the game, "
                 "since it will definitely select the final column. \n\nThis is an "
                 "interesting situation, because on average, we see that the "
                 "agent with the new heuristic performs better than the agent "
                 "from the tutorial (and yet, for this board, it's guaranteed "
                 "to make the wrong decision).")

class CreateAgentEx2(CodingProblem):
    _hint = "Follow the instructions to create an agent."
    _solution = "Follow the instructions to create an agent."
    _congrats = "Thank you for creating an agent!"
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    BetterHeuristic, 
    BothLose,
    CreateAgentEx2
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
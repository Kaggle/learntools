from learntools.core import *
import numpy as np

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

config = dotdict({'columns': 7, 'rows': 6, 'inarow': 4})

def flip_mark(board):
    return list(np.where(np.array(board)==2, 1, np.array(board)*2))

pos_diag_board = [0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 1, 0, 0,
                  0, 0, 0, 1, 2, 0, 0,
                  0, 0, 1, 2, 2, 0, 0,
                  0, 0, 2, 1, 2, 0, 0]
pos_diag_col = 1

obs_pos_diag_win_1 = dotdict({'board': pos_diag_board, 'mark': 1})
obs_pos_diag_win_2 = {'board': flip_mark(pos_diag_board), 'mark': 2}
obs_pos_diag_block_1 = {'board': flip_mark(pos_diag_board), 'mark': 1}
obs_pos_diag_block_2 = {'board': pos_diag_board, 'mark': 2}

neg_diag_board = [0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 1, 0, 0, 0, 0,
                  0, 0, 2, 1, 0, 0, 0,
                  0, 0, 2, 2, 1, 0, 0,
                  0, 0, 1, 1, 2, 0, 0]
neg_diag_col = 5

obs_neg_diag_win_1 = {'board': neg_diag_board, 'mark': 1}
obs_neg_diag_win_2 = {'board': flip_mark(neg_diag_board), 'mark': 2}
obs_neg_diag_block_1 = {'board': flip_mark(neg_diag_board), 'mark': 1}
obs_neg_diag_block_2 = {'board': neg_diag_board, 'mark': 2}

horizontal_board = [0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0,
                    0, 0, 2, 2, 0, 0, 0,
                    0, 2, 1, 1, 1, 0, 0]
horizontal_col = 5

obs_horizontal_win_1 = {'board': horizontal_board, 'mark': 1}
obs_horizontal_win_2 = {'board': flip_mark(horizontal_board), 'mark': 2}
obs_horizontal_block_1 = {'board': flip_mark(horizontal_board), 'mark': 1}
obs_horizontal_block_2 = {'board': horizontal_board, 'mark': 2}

vertical_board = [0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 1, 0, 0, 0, 0,
                  0, 0, 1, 2, 0, 0, 0,
                  0, 0, 1, 2, 2, 0, 0]
vertical_col = 2

obs_vertical_win_1 = {'board': vertical_board, 'mark': 1}
obs_vertical_win_2 = {'board': flip_mark(vertical_board), 'mark': 2}
obs_vertical_block_1 = {'board': flip_mark(vertical_board), 'mark': 1}
obs_vertical_block_2 = {'board': vertical_board, 'mark': 2}

#################################################################################

class SelectWinning(CodingProblem):
    _hint = ""
    _solution = CS(
"""def agent_q1(obs, config):
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    for col in valid_moves:
        if check_winning_move(obs, config, col, obs.mark):
            return col
    return random.choice(valid_moves)
""")
    _var = 'agent_q1'
    
    """
    _test_cases = [
    ((obs_pos_diag_win_1, config), pos_diag_col),
    ((obs_pos_diag_win_2, config), pos_diag_col),
    ((obs_neg_diag_win_1, config), neg_diag_col),
    ((obs_neg_diag_win_2, config), neg_diag_col),
    ((obs_horizontal_win_1, config), horizontal_col),
    ((obs_horizontal_win_2, config), horizontal_col),
    ((obs_vertical_win_1, config), vertical_col),
    ((obs_vertical_win_2, config), vertical_col),
    ]
    """

class BlockOpponent(FunctionProblem):
    _hint = ""
    _solution = CS(
"""def agent_q2(obs, config):
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    for col in valid_moves:
        if check_winning_move(obs, config, col, obs.mark):
            return col
    for col in valid_moves:
        if check_winning_move(obs, config, col, obs.mark%2+1):
            return col
    return random.choice(valid_moves)
""")
    _var = 'agent_q2'
    _test_cases = [
    # win
    ((obs_pos_diag_win_1, config), pos_diag_col),
    ((obs_pos_diag_win_2, config), pos_diag_col),
    ((obs_neg_diag_win_1, config), neg_diag_col),
    ((obs_neg_diag_win_2, config), neg_diag_col),
    ((obs_horizontal_win_1, config), horizontal_col),
    ((obs_horizontal_win_2, config), horizontal_col),
    ((obs_vertical_win_1, config), vertical_col),
    ((obs_vertical_win_2, config), vertical_col),
    # block
    ((obs_pos_diag_block_1, config), pos_diag_col),
    ((obs_pos_diag_block_2, config), pos_diag_col),
    ((obs_neg_diag_block_1, config), neg_diag_col),
    ((obs_neg_diag_block_2, config), neg_diag_col),
    ((obs_horizontal_block_1, config), horizontal_col),
    ((obs_horizontal_block_2, config), horizontal_col),
    ((obs_vertical_block_1, config), vertical_col),
    ((obs_vertical_block_2, config), vertical_col),
    ]

class WhyNotOptimal(ThoughtExperiment):
    _hint = ("Consider this board: `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 0, 0]` "
        "or this board: `[2, 1, 2, 2, 2, 0, 2, 1, 2, 1, 1, 1, 0, 1, 2, 1, 2, 2, 2, 0, 2, 1, 2, 1, 1, 1, 0, 1, 2, 1, 2, 2, 2, 0, 2, 1, 2, 1, 1, 2, 0, 1]`.")
    _solution = ("The agent can still lose the game, if (1) the opponent has set up the board so that it can win "
        "in the next move by dropping a disc in either of 2 or more columns, or (2) the only move that is available "
        "to the agent is one where, once played, the opponent can win in the next move.")

class JustSubmit(CodingProblem):
    _hint = "Follow the instructions to submit your agent to the competition."
    _solution = "Follow the instructions to submit your agent to the competition."
    _congrats = "Thank you for submitting your agent to the competition!"
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    SelectWinning, # todo
    BlockOpponent, # todo
    WhyNotOptimal, # todo
    JustSubmit
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
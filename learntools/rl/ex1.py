from learntools.core import *
import numpy as np
import os
    
class MyConfig(object):
    def __init__(self):
        self.columns = 7
        self.rows = 6
        self.inarow = 4
config = MyConfig()

class MyBoard(object):
    def __init__(self, board, mark):
        self.board = board
        self.mark = mark

def flip_mark(board):
    return list(np.where(np.array(board)==2, 1, np.array(board)*2))

def check_column(agent, my_board, true_column):
    sel_column = agent(my_board, config)
    reshaped_board = np.array(my_board.board).reshape([config.rows,config.columns]).__str__().replace('[', '').replace(']', '').replace('\n ','\n')
    assert sel_column == true_column, \
"""For the game board below, the agent has mark {}, and the opponent has mark {}.  \nThe agent should have selected column {}, but it selected column {}.  \n(_Recall that column indexing starts at 0: so, column 0 is the leftmost column, and column 6 is the rightmost column._)
\n`{}`
""".format(my_board.mark, my_board.mark%2+1, true_column, sel_column, reshaped_board)

pos_diag_board = [0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 1, 0, 0,
                  0, 0, 0, 1, 2, 0, 0,
                  0, 0, 1, 2, 2, 0, 0,
                  0, 0, 2, 1, 2, 0, 0]
pos_diag_col = 1

obs_pos_diag_win_1 = MyBoard(pos_diag_board, 1)
obs_pos_diag_win_2 = MyBoard(flip_mark(pos_diag_board), 2)
obs_pos_diag_block_1 = MyBoard(flip_mark(pos_diag_board), 1)
obs_pos_diag_block_2 = MyBoard(pos_diag_board, 2)

neg_diag_board = [0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 1, 0, 0, 0, 0,
                  0, 0, 2, 1, 0, 0, 0,
                  0, 0, 2, 2, 1, 0, 0,
                  0, 0, 1, 1, 2, 0, 0]
neg_diag_col = 5


obs_neg_diag_win_1 = MyBoard(neg_diag_board, 1)
obs_neg_diag_win_2 = MyBoard(flip_mark(neg_diag_board), 2)
obs_neg_diag_block_1 = MyBoard(flip_mark(neg_diag_board), 1)
obs_neg_diag_block_2 = MyBoard(neg_diag_board, 2)

horizontal_board = [0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0,
                    0, 0, 2, 2, 0, 0, 0,
                    0, 2, 1, 1, 1, 0, 0]
horizontal_col = 5

obs_horizontal_win_1 = MyBoard(horizontal_board, 1)
obs_horizontal_win_2 = MyBoard(flip_mark(horizontal_board), 2)
obs_horizontal_block_1 = MyBoard(flip_mark(horizontal_board), 1)
obs_horizontal_block_2 = MyBoard(horizontal_board, 2)

vertical_board = [0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0,
                  0, 0, 1, 0, 0, 0, 0,
                  0, 0, 1, 2, 0, 0, 0,
                  0, 0, 1, 2, 2, 0, 0]
vertical_col = 2

obs_vertical_win_1 = MyBoard(vertical_board, 1)
obs_vertical_win_2 = MyBoard(flip_mark(vertical_board), 2)
obs_vertical_block_1 = MyBoard(flip_mark(vertical_board), 1)
obs_vertical_block_2 = MyBoard(vertical_board, 2)


#################################################################################

class SelectWinning(CodingProblem):
    _var = "agent_q1"
    _hint = ("Use the `check_winning_move()` function, and set `piece=obs.mark`.  You can check if "
    "the agent can win the game by dropping its piece in a specific column by supplying the column "
    "as the `col` argument to the function.")
    _solution = CS(
"""def agent_q1(obs, config):
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    for col in valid_moves:
        if check_winning_move(obs, config, col, obs.mark):
            return col
    return random.choice(valid_moves)
""")
    _var = 'agent_q1'
    def check(self, agent_q1):
        check_column(agent_q1, obs_pos_diag_win_1, pos_diag_col)
        check_column(agent_q1, obs_pos_diag_win_2, pos_diag_col)
        check_column(agent_q1, obs_neg_diag_win_1, neg_diag_col)
        check_column(agent_q1, obs_neg_diag_win_2, neg_diag_col)
        check_column(agent_q1, obs_horizontal_win_1, horizontal_col)
        check_column(agent_q1, obs_horizontal_win_2, horizontal_col)
        check_column(agent_q1, obs_vertical_win_1, vertical_col)
        check_column(agent_q1, obs_vertical_win_2, vertical_col)
    
class BlockOpponent(CodingProblem):
    _hint = ("Start with the code from the agent you created above.  To check if the opponent can "
    "win in its next move, use the same `check_winning_move()` function, and set `piece=obs.mark%2+1`.")
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
    def check(self, agent_q2):
        # win
        check_column(agent_q2, obs_pos_diag_win_1, pos_diag_col)
        check_column(agent_q2, obs_pos_diag_win_2, pos_diag_col)
        check_column(agent_q2, obs_neg_diag_win_1, neg_diag_col)
        check_column(agent_q2, obs_neg_diag_win_2, neg_diag_col)
        check_column(agent_q2, obs_horizontal_win_1, horizontal_col)
        check_column(agent_q2, obs_horizontal_win_2, horizontal_col)
        check_column(agent_q2, obs_vertical_win_1, vertical_col)
        check_column(agent_q2, obs_vertical_win_2, vertical_col)
        # block
        check_column(agent_q2, obs_pos_diag_block_1, pos_diag_col)
        check_column(agent_q2, obs_pos_diag_block_2, pos_diag_col)
        check_column(agent_q2, obs_neg_diag_block_1, neg_diag_col)
        check_column(agent_q2, obs_neg_diag_block_2, neg_diag_col)
        check_column(agent_q2, obs_horizontal_block_1, horizontal_col)
        check_column(agent_q2, obs_horizontal_block_2, horizontal_col)
        check_column(agent_q2, obs_vertical_block_1, vertical_col)
        check_column(agent_q2, obs_vertical_block_2, vertical_col)

class WhyNotOptimal(ThoughtExperiment):
    board1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1, 0, 0]
    board1_shaped = np.array(board1).reshape([config.rows,config.columns]).__str__().replace('[', '').replace(']', '').replace('\n ','\n')
    board2 = [2, 1, 2, 2, 2, 0, 2, 1, 2, 1, 1, 1, 0, 1, 2, 1, 2, 2, 2, 0, 2, 1, 2, 1, 1, 1, 0, 1, 2, 1, 2, 2, 2, 0, 2, 1, 2, 1, 1, 2, 0, 1]
    board2_shaped = np.array(board2).reshape([config.rows,config.columns]).__str__().replace('[', '').replace(']', '').replace('\n ','\n')
    _hint = \
"""\
Consider this board: \n
`{}`\n
or this board: \n
`{}`
""".format(board1_shaped, board2_shaped)
    _solution = (
"""The agent can still lose the game, if 
- the opponent has set up the board so that it can win in the next move by dropping a disc in any of 2 or more columns, or 
- the only move that is available to the agent is one where, once played, the opponent can win in the next move.
""")

class CreateAgentEx1(CodingProblem):
    _hint = "Follow the instructions to create an agent."
    _solution = "Follow the instructions to create an agent."
    _congrats = "Thank you for creating an agent!"
    _correct_message = ""
    def check(self):
        pass
    
class SubmissionEx1(CodingProblem):
    _hint = "Follow the instructions to create a submission file."
    _solution = "Follow the instructions to create a submission file."
    _congrats = "Thank you for creating a submission file!"
    _correct_message = ""
    def check(self):
        assert os.path.exists("./submission.py"), "You do not yet have a submission file."

qvars = bind_exercises(globals(), [
    SelectWinning, 
    BlockOpponent, 
    WhyNotOptimal, 
    CreateAgentEx1,
    SubmissionEx1
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
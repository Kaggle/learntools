import json
from os import path
from random import choice

EMPTY = 0


def random_agent(obs, config):
    return choice([c for c in range(config.columns) if obs.board[c] == EMPTY])


def interpreter(state, env):
    columns = env.configuration.columns
    rows = env.configuration.rows
    inarow = env.configuration.inarow

    # Get the active agent and action.
    agent1 = state[0]
    agent2 = state[1]
    active = agent1 if agent2.done else agent2
    column = active.action

    # 1st agents board is the master.
    board = agent1.observation.board

    # Ensure the board is properly initialized.
    if len(board) != (rows * columns):
        board = [EMPTY] * (rows * columns)
        agent1.observation.board = board

    # Clone board to second agent as they share the same view.
    agent2.observation.board = board

    # Specification can fully handle the reset apart from board reset.
    if env.done:
        return state

    # Illegal column, agent loses.
    if active.action < 0 or active.action > columns or board[column] != EMPTY:
        active.reward = 0
        active.done = True
        return state

    # Find the lowest row in the column to fill.
    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])

    # Mark the position.
    board[column + (row * columns)] = active.observation.mark

    # Check for a win.
    def count(offset_row, offset_column):
        for i in range(0, inarow):
            r = row + offset_row * i
            c = column + offset_column * i
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= columns
                or board[c + (r * columns)] != active.observation.mark
            ):
                return i
        return inarow

    # Check for a win.
    if (
        count(1, 0) >= inarow  # vertical.
        or (count(0, 1) + count(0, -1)) > inarow  # horizontal.
        or (count(-1, -1) + count(1, 1)) > inarow  # top left diagonal.
        or (count(-1, 1) + count(1, -1)) > inarow  # top right diagonal.
    ):
        agent1.reward = 0 if agent1.done else 1
        agent2.reward = 0 if agent2.done else 1
        active.done = True
        return state

    # Check for a tie.
    if all(mark != EMPTY for mark in board):
        active.done = True
        return state

    # Swap done agents to switch turns.
    agent1.done = not agent1.done
    agent2.done = not agent2.done

    return state


def renderer(state, env):
    columns = env.configuration.columns
    rows = env.configuration.rows
    board = state[0].observation.board

    def print_row(values, delim="|"):
        return f"{delim} " + f" {delim} ".join(str(v) for v in values) + f" {delim}\n"

    rowBar = "+" + "+".join(["---"] * columns) + "+\n"
    out = rowBar
    for r in range(rows):
        out = out + print_row(board[r * columns : r * columns + columns]) + rowBar

    return out


dirpath = path.dirname(__file__)
jsonpath = path.abspath(path.join(dirpath, "connectx.json"))
with open(jsonpath) as f:
    specification = json.load(f)


def get_html_renderer():
    jspath = path.abspath(path.join(dirpath, "connectx.js"))
    with open(jspath) as f:
        return f.read()


connectx = {
    "specification": specification,
    "interpreter": interpreter,
    "renderer": renderer,
    "html_renderer": get_html_renderer,
    "agents": {"random": random_agent},
}

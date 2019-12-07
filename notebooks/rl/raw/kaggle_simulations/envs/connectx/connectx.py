import json
from os import path
from random import choice

EMPTY = 0


def play(board, column, mark, config):
    columns = config.columns
    rows = config.rows
    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
    board[column + (row * columns)] = mark


def is_win(board, column, mark, config, has_played=True):
    columns = config.columns
    rows = config.rows
    inarow = config.inarow - 1
    row = (
        min([r for r in range(rows) if board[column + (r * columns)] == mark])
        if has_played
        else max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
    )

    def count(offset_row, offset_column):
        for i in range(1, inarow + 1):
            r = row + offset_row * i
            c = column + offset_column * i
            if (
                r < 0
                or r >= rows
                or c < 0
                or c >= columns
                or board[c + (r * columns)] != mark
            ):
                return i - 1
        return inarow

    return (
        count(1, 0) >= inarow  # vertical.
        or (count(0, 1) + count(0, -1)) >= inarow  # horizontal.
        or (count(-1, -1) + count(1, 1)) >= inarow  # top left diagonal.
        or (count(-1, 1) + count(1, -1)) >= inarow  # top right diagonal.
    )


def random_agent(obs, config):
    return choice([c for c in range(config.columns) if obs.board[c] == EMPTY])


def negamax_agent(obs, config):
    columns = config.columns
    rows = config.rows
    size = rows * columns

    # Due to compute/time constraints the tree depth must be limited.
    max_depth = 4

    def negamax(board, mark, depth):
        moves = sum(1 if cell != EMPTY else 0 for cell in board)

        # Tie Game
        if moves == size:
            return (0, None)

        # Can win next.
        for column in range(columns):
            if board[column] == EMPTY and is_win(board, column, mark, config, False):
                return ((size + 1 - moves) / 2, column)

        # Recursively check all columns.
        best_score = -size
        best_column = None
        for column in range(columns):
            if board[column] == EMPTY:
                # Max depth reached. Score based on cell proximity for a clustering effect.
                if depth <= 0:
                    row = max(
                        [
                            r
                            for r in range(rows)
                            if board[column + (r * columns)] == EMPTY
                        ]
                    )
                    score = (size + 1 - moves) / 2
                    if column > 0 and board[row * columns + column - 1] == mark:
                        score += 1
                    if (
                        column < columns - 1
                        and board[row * columns + column + 1] == mark
                    ):
                        score += 1
                    if row > 0 and board[(row - 1) * columns + column] == mark:
                        score += 1
                    if row < rows - 2 and board[(row + 1) * columns + column] == mark:
                        score += 1
                else:
                    next_board = board[:]
                    play(next_board, column, mark, config)
                    (score, _) = negamax(next_board, 1 if mark == 2 else 2, depth - 1)
                    score = score * -1
                if score > best_score:
                    best_score = score
                    best_column = column

        return (best_score, best_column)

    _, column = negamax(obs.board[:], obs.mark, max_depth)
    if column == None:
        column = choice([c for c in range(columns) if obs.board[c] == EMPTY])
    return column


def interpreter(state, env):
    columns = env.configuration.columns
    rows = env.configuration.rows

    # Ensure the board is properly initialized.
    board = state[0].observation.board
    if len(board) != (rows * columns):
        board = [EMPTY] * (rows * columns)
        state[0].observation.board = board

    # Clone board to inactive agent as they share the same observation.
    state[1].observation.board = board

    # Specification can fully handle the reset apart from board reset.
    if env.done:
        return state

    # Isolate the active and inactive agents.
    active = state[0] if state[0].status == "ACTIVE" else state[1]
    inactive = state[0] if state[0].status == "INACTIVE" else state[1]
    if active.status != "ACTIVE" or inactive.status != "INACTIVE":
        active.status = "DONE" if active.status == "ACTIVE" else active.status
        inactive.status = "DONE" if inactive.status == "INACTIVE" else inactive.status
        return state

    # Active agent action.
    column = active.action

    # Invalid column, agent loses.
    if column < 0 or active.action > columns or board[column] != EMPTY:
        active.status = f"Invalid column: {column}"
        inactive.status = "DONE"
        return state

    # Mark the position.
    play(board, column, active.observation.mark, env.configuration)

    # Check for a win.
    if is_win(board, column, active.observation.mark, env.configuration):
        active.reward = 1
        active.status = "DONE"
        inactive.reward = 0
        inactive.status = "DONE"
        return state

    # Check for a tie.
    if all(mark != EMPTY for mark in board):
        active.status = "DONE"
        inactive.status = "DONE"
        return state

    # Swap active agents to switch turns.
    active.status = "INACTIVE"
    inactive.status = "ACTIVE"

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
    "agents": {"random": random_agent, "negamax": negamax_agent},
}

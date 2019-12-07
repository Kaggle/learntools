import json
from os import path
from random import choice

checks = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

EMPTY = 0


def random_agent(obs):
    return choice([c for c in range(len(obs.board)) if obs.board[c] == EMPTY])


def reaction_agent(obs):
    # Connect 3 in a row to win.
    for check in checks:
        left = list(filter(lambda c: obs.board[c] != obs.mark, check))
        if len(left) == 1 and obs.board[left[0]] == EMPTY:
            return left[0]

    # Block 3 in a row to prevent loss.
    opponent = 2 if obs.mark == 1 else 1
    for check in checks:
        left = list(filter(lambda c: obs.board[c] != opponent, check))
        if len(left) == 1 and obs.board[left[0]] == EMPTY:
            return left[0]

    # No 3-in-a-rows, return random unmarked.
    return choice(list(filter(lambda m: m[1] == EMPTY, enumerate(obs.board))))[0]


def interpreter(state, env):
    # Specification can fully handle the reset.
    if env.done:
        return state

    # Isolate the active and inactive agents.
    active = state[0] if state[0].status == "ACTIVE" else state[1]
    inactive = state[0] if state[0].status == "INACTIVE" else state[1]
    if active.status != "ACTIVE" or inactive.status != "INACTIVE":
        active.status = "DONE" if active.status == "ACTIVE" else active.status
        inactive.status = "DONE" if inactive.status == "INACTIVE" else inactive.status
        return state

    # Keep the board in sync between both agents.
    board = active.observation.board
    inactive.observation.board = board

    # Illegal move by the active agent.
    if board[active.action] != EMPTY:
        active.status = f"Invalid move: {active.action}"
        inactive.status = "DONE"
        return state

    # Mark the position.
    board[active.action] = active.observation.mark

    # Check for a win.
    if any(all(board[p] == active.observation.mark for p in c) for c in checks):
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

    # Swap active and inactive agents to switch turns.
    active.status = "INACTIVE"
    inactive.status = "ACTIVE"

    return state


def renderer(state, env):
    rowBar = "\n---+---+---\n"
    marks = [" ", "X", "O"]

    def printPos(pos):
        str = ""
        if pos % 3 == 0 and pos > 0:
            str += rowBar
        if pos % 3 != 0:
            str += "|"
        return str + f" {marks[state[0].observation.board[pos]]} "

    return "".join(printPos(p) for p in range(9))


dirpath = path.dirname(__file__)
jsonpath = path.abspath(path.join(dirpath, "tictactoe.json"))
with open(jsonpath) as f:
    specification = json.load(f)


def get_html_renderer():
    jspath = path.abspath(path.join(dirpath, "tictactoe.js"))
    with open(jspath) as f:
        return f.read()


tictactoe = {
    "specification": specification,
    "interpreter": interpreter,
    "renderer": renderer,
    "html_renderer": get_html_renderer,
    "agents": {"random": random_agent, "reaction": reaction_agent},
}

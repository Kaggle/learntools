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
    # return choice(list(filter(lambda m: m[1] == 0, enumerate(obs.board))))[0]


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

    agent1 = state[0]
    agent2 = state[1]
    active = agent1 if agent2.done else agent2

    # Keep the board in sync between both agents.
    board = agent1.observation.board
    agent2.observation.board = board

    # Illegal move, agent losses, all agents are done.
    if board[active.action] != EMPTY:
        active.reward = 0
        active.done = True
        return state

    # Mark the position.
    board[active.action] = active.observation.mark

    # Check for a win.
    if any(all(board[p] == active.observation.mark for p in c) for c in checks):
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

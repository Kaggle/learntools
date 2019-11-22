from chess import Board
from random import choice


def agent(state):
    observation = state.get("observation", {})
    board = observation.get("board", "")
    cb = Board(board)
    moves = list(cb.legal_moves)
    return "" if not moves else cb.uci(choice(moves))

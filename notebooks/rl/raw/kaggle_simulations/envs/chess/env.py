from chess import Board, Move


def interpreter(state):
    agents = state.get("agents", [])
    observation = state.get("observation", {})
    board = observation.get("board", "")

    # The Environment should handle resetting all fields for chess.
    if state["done"]:
        return state

    # Get the active agent.
    agent = next(a for a in agents if a["active"])

    # Build and validate the chess board.
    cb = Board(board)
    if not cb.is_valid():
        agent["reward"] = 0
        return {**state, "done": True}

    if cb.is_game_over():
        return {**state, "done": True}

    # Build and validate the agent move.
    move = Move.from_uci(agent.get("action", ""))
    if move not in cb.legal_moves:
        agent["reward"] = 0
        return {**state, "done": True}

    # Update the board
    cb.push(move)
    observation["board"] = cb.fen()

    # Check if there is a final result.
    result = cb.result()
    if result != "*":
        # Default rewards are 0.5 / 0.5 for a draw.
        if result == "1-0" or result == "0-1":
            agents[0]["reward"] = int(result[0])
            agents[1]["reward"] = int(result[2])
        return {**state, "done": True}

    # Toggle active agents to switch turns.
    agents[0]["active"] = not agents[0]["active"]
    agents[1]["active"] = not agents[1]["active"]

    return state


def renderer(state):
    observation = state.get("observation", {})
    board = observation.get("board", "")
    return str(Board(board))

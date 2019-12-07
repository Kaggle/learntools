import json
import math
from os import path
from random import choice, randint


def random_agent(obs):
    shipyard = None
    ships = []
    dropoffs = []
    player = obs.player

    for pos, cell in enumerate(obs.board):
        _, shipyard, dropoff, ship, ship_halite = cell

    return []


def interpreter(state, env):
    config = env.configuration
    num_agents = len(state)
    size = config.size
    num_cells = size ** 2

    # Initialize the board.
    if env.done:
        # Distribute the Halite evenly.
        def generate_halite(cols, rows, halite):
            num_cells = cols * rows
            grid = [[0, randint(0, num_cells) ** 2] for i in range(num_cells)]
            total = sum([amp for _, amp in grid])
            for cell in grid:
                cell[0] = math.floor(halite * cell[1] / total)
            return [h for h, _ in grid]

        board = [[0, -1, -1, -1, 0] for _ in range(num_cells)]
        for agent in state:
            agent.observation.board = board

        greedy_half = math.ceil(size / 2)
        halite = generate_halite(greedy_half, greedy_half, config.halite / 4)
        for index, h in enumerate(halite):
            col = index % greedy_half
            row = math.floor(index / greedy_half)
            board[size * row + col][0] = h
            board[size * row + (size - 1 - col)][0] = h
            board[(size * (size - 1)) - (size * row) + col][0] = h
            board[(size * (size - 1)) - (size * row) + (size - 1 - col)][0] = h

        # Fixed placement of shipyards.
        if num_agents == 1:
            board[size * (size // 2) + size // 2] = [0, 0, -1, -1, 0]

        elif num_agents == 2:
            board[size * (size // 2) + size // 4] = [0, 0, -1, -1, 0]
            board[size * (size // 2) + math.ceil(3 * size / 4) - 1] = [0, 1, -1, -1, 0]

        elif num_agents == 4:
            board[size * (size // 4) + size // 4] = [0, 0, -1, -1, 0]
            board[size * (size // 4) + 3 * size // 4] = [0, 1, -1, -1, 0]
            board[size * (3 * size // 4) + size // 4] = [0, 2, -1, -1, 0]
            board[size * (3 * size // 4) + 3 * size // 4] = [0, 3, -1, -1, 0]

        return state

    # Break-down the board for easier consumption.
    # [shipyard:pos, dropoffs:[pos], new_dropoffs:[pos], ships:{pos:halite}, new_ships:[[pos, halite],...]]
    players = [[-1, [], [], {}, []] for _ in state]

    for pos, cell in enumerate(state[0].observation.board):
        _, shipyard, dropoff, ship, ship_halite = cell
        if shipyard != -1:
            if players[shipyard][0] != -1:
                raise "Invalid board state - every player should have one shipyard."
            players[shipyard][0] = pos
        if dropoff != -1:
            if pos in players[dropoff][1]:
                raise "Invalid board state - multiple dropoffs in same cell."
            players[dropoff][1].append(pos)
        if ship != -1:
            if pos in players[ship][3]:
                raise "Invalid board state - multiple ships in same cell."
            players[ship][3][pos] = ship_halite

    # Validate every player has a shipyard.
    for player in players:
        if player[0] == -1:
            raise "Invalid board state - every player should have one shipyard."

    # Convert actions into player ship/dropoff updates.
    for index, agent in enumerate(state):
        if agent.status != "ACTIVE":
            break

        shipyard, dropoffs, new_dropoffs, ships, new_ships = players[index]

        for pos, action in agent.action:
            if action == "SPAWN":
                # The players shipyard is not at this position.
                if shipyard != pos:
                    agent.status = f"Shipyard not present at: {pos}"
                    break

                agent.reward -= config.spawn_cost
                new_ships.append([pos, 0])
                continue

            # No ship is at this position to perform an action with.
            if pos not in ships:
                agent.status = f"Ship not present at: {pos}"
                break

            ship_halite = ships[pos]
            del ships[pos]

            if action == "CONVERT":
                # There is already a dropoff in this position.
                if pos in dropoffs:
                    agent.status = f"Dropoff already at: {pos}"
                    break

                agent.reward += ship_halite - config.convert_cost
                new_dropoffs.append(pos)
                continue

            # Move the ship to a new location.
            col = pos % size
            row = pos // size
            new_pos = -1
            new_ship_halite = ship_halite - round(ship_halite * config.move_cost)

            if action == "NORTH":
                new_pos = pos - size
                if new_pos < 0:
                    new_pos += num_cells
            elif action == "SOUTH":
                new_pos = pos + size
                if new_pos >= num_cells:
                    new_pos = new_pos % size
            elif action == "EAST":
                new_pos = pos + 1 if col < size - 1 else row * size
            elif action == "WEST":
                new_pos = pos - 1 if col > 0 else (row + 1) * size - 1
            else:
                # Unknown action, agent is terminated.
                agent.status = f"Unknown action: {action}"
                break
            new_ships.append([new_pos, new_ship_halite])

    # Remove players which:
    # 1. overspent halite (negative reward).
    # 2. marked not as active.
    # 3. have no ships and not enough halite to spawn another.
    for index, agent in enumerate(state):
        player = players[index]
        if agent.reward < 0 or (
            len(players[index][3]) == 0 and agent.reward < config.spawn_cost
        ):
            agent.status = "DONE"
        if agent.status != "ACTIVE":
            agent.reward = max(0, agent.reward)
            players[index] = [-1, [], [], {}, []]

    # Check for collisions.
    ship_counts = {}
    for _, __, ___, ships, new_ships in players:
        positions = [*ships.keys(), *[pos for pos, _ in new_ships]]
        for pos in positions:
            ship_counts[pos] = 1 if pos not in ship_counts else ship_counts[pos] + 1

    # Mark collided ships (invert halite aboard in mark for deletion, otherwise delete if empty).
    for _, __, ___, ships, new_ships in players:
        for pos in list(ships.keys()):
            if ship_counts[pos] > 1:
                ships[pos] *= -1
                if ships[pos] == 0:
                    del ships[pos]

        for ship in new_ships:
            if ship_counts[ship[0]] > 1:
                ship[1] *= -1
                if ship[1] == 0:
                    ship[0] = -1

    # Build the new board.
    board = [[cell[0], -1, -1, -1, 0] for cell in state[0].observation.board]

    for index, player in enumerate(players):
        shipyard, dropoffs, new_dropoffs, ships, new_ships = player
        agent = state[index]
        agent.observation.board = board

        # Place shipyards and destroy halite in the cell.
        if shipyard > -1:
            board[shipyard][0] = 0
            board[shipyard][1] = index

        # Place dropoffs and destroy halite in dropoff cells.
        for pos in [*dropoffs, *new_dropoffs]:
            board[pos][0] = 0
            board[pos][2] = index

        # Existing Unmoved Ships - collide, dropoff, collect, and mark.
        for pos, ship_halite in ships.items():
            is_dropoff = board[pos][2] >= 0
            is_shipyard = board[pos][1] >= 0

            # Collided.
            if ship_halite < 0:
                if not is_dropoff and not is_shipyard:
                    board[pos][0] += ship_halite * -1
                continue

            # Dropoff Halite (shipyard or dropoff).
            if board[pos][2] == index or board[pos][1] == index:
                agent.reward += ship_halite
                ship_halite = 0

            # Collect Halite.
            # TODO - MAX collection in a ship?  99?
            elif board[pos][0] > 0:
                collected = math.ceil(board[pos][0] * config.collect_rate)
                board[pos][0] -= collected
                ship_halite += collected

            # Mark the board with the ship and it's halite.
            board[pos][3] = index
            board[pos][4] = ship_halite

        # New/Moved Ships - collide and mark.
        for pos, ship_halite in new_ships:
            if pos < 0:
                continue
            is_dropoff = board[pos][2] >= 0
            is_shipyard = board[pos][1] >= 0

            # Collided.
            if ship_halite < 0:
                if not is_dropoff and not is_shipyard:
                    board[pos][0] += ship_halite * -1
                continue

            # Mark the board with the ship and it's halite.
            board[pos][3] = index
            board[pos][4] = ship_halite

    # TODO - Halite Regeneration

    return state


def renderer(state, env):
    config = env.configuration
    size = config.size
    board = state[0].observation.board

    colDivider = "|"
    rowDivider = "+" + "+".join(["----"] * size) + "+\n"

    out = rowDivider
    for row in range(size):
        # Ship Row.
        for col in range(size):
            _, _, _, ship, ship_halite = board[col + row * size]
            out += colDivider + (
                f"{min(ship_halite, 99)}S{ship}" if ship > -1 else ""
            ).rjust(4)
        out += colDivider + "\n"
        # Halite, Shipyard, Dropoff Row.
        for col in range(size):
            halite, shipyard, dropoff, _, _ = board[col + row * size]
            out += colDivider
            if shipyard > -1:
                out += f" SY{shipyard}"
            elif dropoff > -1:
                out += f" DO{dropoff}"
            else:
                out += str(min(halite, 9999)).rjust(4)
        out += colDivider + "\n" + rowDivider

    return out


dirpath = path.dirname(__file__)
jsonpath = path.abspath(path.join(dirpath, "nacl.json"))
with open(jsonpath) as f:
    specification = json.load(f)


def get_html_renderer():
    jspath = path.abspath(path.join(dirpath, "nacl.js"))
    with open(jspath) as f:
        return f.read()


nacl = {
    "specification": specification,
    "interpreter": interpreter,
    "renderer": renderer,
    "html_renderer": get_html_renderer,
    "agents": {"random": random_agent},
}

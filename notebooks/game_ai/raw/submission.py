
DIRS = ["NORTH", "SOUTH", "EAST", "WEST"]

def argmax(arr, key=None):
    return arr.index(max(arr, key=key)) if key else arr.index(max(arr))

def get_col_row(size, pos):
    return (pos % size, pos // size)

# This function will not hold up in practice
# E.g. cell getAdjacent(224) includes position 0, which is not adjacent
def get_to_pos(size, pos, direction):
    col, row = get_col_row(size, pos)
    if direction == "NORTH":
        return pos - size if pos >= size else size ** 2 - size + col
    elif direction == "SOUTH":
        return col if pos + size >= size ** 2 else pos + size
    elif direction == "EAST":
        return pos + 1 if col < size - 1 else row * size
    elif direction == "WEST":
        return pos - 1 if col > 0 else (row + 1) * size - 1

def getAdjacent(pos, size):
    return [
        get_to_pos(size, pos, "NORTH"),
        get_to_pos(size, pos, "SOUTH"),
        get_to_pos(size, pos, "EAST"),
        get_to_pos(size, pos, "WEST"),
    ]

def getDirTo(fromPos, toPos, size):
    fromY, fromX = divmod(fromPos, size)
    toY,   toX   = divmod(toPos,   size)
    if fromY < toY: return "SOUTH"
    if fromY > toY: return "NORTH"
    if fromX < toX: return "EAST"
    if fromX > toX: return "WEST"

# Each ship id will be assigned a state (one of COLLECT or DEPOSIT) which decides what it will do on a turn.
states = {}

def agent(obs, config):
    action = {}
    player_halite, shipyards, ships = obs.players[obs.player]
    size = config["size"]

    for uid, shipyard in shipyards.items():
        # Maintain one ship always
        if len(ships) == 0:
            action[uid] = "SPAWN"

    for uid, ship in ships.items():
        # Maintain one shipyard always
        if len(shipyards) == 0:
            action[uid] = "CONVERT"
            continue

        # If a ship was just made
        if uid not in states: states[uid] = "COLLECT"

        pos, halite = ship

        if states[uid] == "COLLECT":
            if halite > 500:
                states[uid] = "DEPOSIT"

            elif obs.halite[pos] < 100:
                best = argmax(getAdjacent(pos, size), key=obs.halite.__getitem__)
                action[uid] = DIRS[best]

        if states[uid] == "DEPOSIT":
            if halite < 200: states[uid] = "COLLECT"

            direction = getDirTo(pos, list(shipyards.values())[0], size)
            if direction: action[uid] = direction
            else: states[uid] = "COLLECT"
    return action

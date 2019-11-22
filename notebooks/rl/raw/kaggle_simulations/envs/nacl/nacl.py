import json
from os import path
from random import choice


def random_agent(obs):
    return []

def interpreter(state, env):
    config = env.configuration
    num_agents = len(state)

    # Initialize the board.
    if env.done:
        board = [[0,-1,-1,-1] for _ in range(config.size ^ 2)]

        if num_agents == 2:
            # Fixed placement of shipyards.
            board[(config.size ^ 2) // 2 + config.size // 4] = 0
            board[(config.size ^ 2) // 2 + (3 * config.size) // 4] = 1

            # Distri
            half_board = [0 for _ in range(0.5 * config.size ^ 2)]
        
        return state


    
    # Collect Halite

    # Move Ships and check for collisons.

    # Spawn Ships.

    # Convert Drop

    return state

def renderer(state, env):
    return "nacl"

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
    "agents": {"random": random_agent },
}

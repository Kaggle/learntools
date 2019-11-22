from kaggle_simulations import make, evaluate, run

env = None


def custom1(obs):
    step = sum(1 for mark in obs.board if mark == obs.mark)
    return [0, 2, 4, 6, 8][step]


def custom2(obs):
    step = sum(1 for mark in obs.board if mark == obs.mark)
    return [1, 3, 5, 7][step]


def beforeEach(state=None):
    global env
    env = make("tictactoe", state=state)


def test_to_json():
    beforeEach()
    assert env.toJSON() == {
        "configuration": {},
        "description": "Classic Tic Tac Toe",
        "max_steps": 10000,
        "name": "tictactoe",
        "specification": {
            "action": {
                "default": 0,
                "description": "Position to place a mark on the " "board.",
                "maximum": 8,
                "minimum": 0,
                "type": "integer",
            },
            "agents": {
                "defaults": {
                    "done": [False, True],
                    "observation": [{"mark": 1}, {"mark": 2}],
                    "reward": 0.5,
                },
                "maximum": 2,
                "minimum": 2,
            },
            "configuration": {},
            "info": {},
            "observation": {
                "board": {
                    "default": [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "description": "Serialized 3x3 " "grid. 0 = Empty, " "1 = X, 2 = O",
                    # "items": {"enum": [0, 1, 2]}, # disabled due to naming conflict
                    "maxItems": 9,
                    "minItems": 9,
                    "type": "array",
                },
                "mark": {"description": "Mark for the agent " "to use", "enum": [1, 2]},
            },
            "reward": {
                "default": 0.5,
                "description": "0 = Lost, 0.5 = Draw, 1 = Won",
                "enum": [0, 0.5, 1],
                "type": "number",
            },
        },
        "version": "1.0.0",
    }


def test_can_reset():
    beforeEach()
    assert env.reset() == [
        {
            "action": 0,
            "done": False,
            "info": {},
            "observation": {"mark": 1, "board": [0, 0, 0, 0, 0, 0, 0, 0, 0]},
            "reward": 0.5,
        },
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"mark": 2, "board": [0, 0, 0, 0, 0, 0, 0, 0, 0]},
            "reward": 0.5,
        },
    ]


def test_can_place_valid_mark():
    beforeEach()

    assert env.step([4, None]) == [
        {
            "action": 4,
            "done": True,
            "info": {},
            "observation": {"mark": 1, "board": [0, 0, 0, 0, 1, 0, 0, 0, 0]},
            "reward": 0.5,
        },
        {
            "action": 0,  # None caused the default action to be applied.
            "done": False,
            "info": {},
            "observation": {"mark": 2, "board": [0, 0, 0, 0, 1, 0, 0, 0, 0]},
            "reward": 0.5,
        },
    ]


def test_can_place_invalid_mark():
    beforeEach()

    env.step([4, None])

    assert env.step([None, 4]) == [
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"mark": 1, "board": [0, 0, 0, 0, 1, 0, 0, 0, 0]},
            "reward": 0.5,
        },
        {
            "action": 4,
            "done": True,
            "info": {},
            "observation": {"mark": 2, "board": [0, 0, 0, 0, 1, 0, 0, 0, 0]},
            "reward": 0,
        },
    ]


def test_can_place_winning_mark():
    obs = {"observation": {"board": [2, 1, 0, 1, 1, 0, 2, 0, 2]}}
    beforeEach([obs, obs])

    assert env.step([7, None]) == [
        {
            "action": 7,
            "done": True,
            "info": {},
            "observation": {"mark": 1, "board": [2, 1, 0, 1, 1, 0, 2, 1, 2]},
            "reward": 1,
        },
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"mark": 2, "board": [2, 1, 0, 1, 1, 0, 2, 1, 2]},
            "reward": 0,
        },
    ]


def test_can_render():
    obs = {"observation": {"board": [0, 1, 0, 2, 1, 2, 0, 0, 2]}}
    beforeEach([obs, obs])
    out = "   | X |   \n---+---+---\n O | X | O \n---+---+---\n   |   | O "
    assert env.render(True) == out


def test_can_step_through_agents():
    beforeEach()
    while not env.done:
        action1 = env.agents.random(env.state[0].observation)
        action2 = env.agents.reaction(env.state[1].observation)
        env.step([action1, action2])
    assert env.state[0].reward + env.state[1].reward == 1


def test_can_run_agents():
    beforeEach()
    state = env.run(["random", "reaction"])[-1]
    assert state[0].reward + state[1].reward == 1


def test_can_run():
    state = run("tictactoe", ["random", "reaction"]).steps[-1]
    assert state[0].reward + state[1].reward == 1


def test_can_evaluate():
    rewards = evaluate("tictactoe", ["random", "reaction"], num_episodes=2)
    assert (rewards[0][0] + rewards[0][1] == 1) and rewards[1][0] + rewards[1][1] == 1


def test_can_run_custom_agents():
    state = env.run([custom1, custom2])[-1]
    assert state == [
        {
            "action": 6,
            "reward": 1,
            "info": {},
            "observation": {"board": [1, 2, 1, 2, 1, 2, 1, 0, 0], "mark": 1},
            "done": True,
        },
        {
            "action": 0,
            "reward": 0,
            "info": {},
            "observation": {"board": [1, 2, 1, 2, 1, 2, 1, 0, 0], "mark": 2},
            "done": True,
        },
    ]


def test_can_run_as_a_gym():
    beforeEach()
    global env

    # Gym will train the second agent.
    env = env.gym([custom1, None])
    observation, reward, done, info = env.reset()

    assert observation == {"board": [1, 0, 0, 0, 0, 0, 0, 0, 0], "mark": 2}
    assert reward == 0.5
    assert done == False
    assert info == {}

    while not done:
        action = custom2(observation)
        observation, reward, done, info = env.step(action)

    assert observation == {"board": [1, 2, 1, 2, 1, 2, 1, 0, 0], "mark": 2}
    assert reward == 0
    assert done == True
    assert info == {}

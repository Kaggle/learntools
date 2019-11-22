from kaggle_simulations import make, evaluate, run

env = None


def beforeEach(state=None, configuration=None):
    global env
    env = make("connectx", state=state, configuration=configuration)


def test_to_json():
    beforeEach()
    assert env.toJSON() == {
        "configuration": {"columns": 7, "inarow": 4, "rows": 6},
        "description": "Classic Connect Four but configurable.",
        "max_steps": 10000,
        "name": "connectx",
        "specification": {
            "action": {
                "default": 0,
                "description": "Column to drop a checker onto " "the board.",
                "minimum": 0,
                "type": "integer",
            },
            "agents": {
                "defaults": {
                    "done": [False, True],
                    "observation": [{"mark": 1}, {"mark": 2}],
                },
                "maximum": 2,
                "minimum": 2,
            },
            "configuration": {
                "columns": {
                    "default": 7,
                    "description": "The number of " "columns on " "the board",
                    "minimum": 1,
                    "type": "integer",
                },
                "inarow": {
                    "default": 4,
                    "description": "The number of "
                    "checkers in a "
                    "row required "
                    "to win.",
                    "minimum": 1,
                    "type": "integer",
                },
                "rows": {
                    "default": 6,
                    "description": "The number of " "rows on the " "board",
                    "minimum": 1,
                    "type": "integer",
                },
            },
            "info": {},
            "observation": {
                "board": {
                    "default": [],
                    "description": "Serialized grid "
                    "(rows x columns). "
                    "0 = Empty, 1 = "
                    "P1, 2 = P2",
                    "type": "array",
                },
                "mark": {
                    "default": 0,
                    "description": "Which checkers are " "the agents.",
                    "enum": [1, 2],
                },
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
            "observation": {"board": [0] * 42, "mark": 1},
            "reward": 0.5,
        },
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"board": [0] * 42, "mark": 2},
            "reward": 0.5,
        },
    ]


def test_can_mark():
    beforeEach(configuration={"rows": 4, "columns": 5, "inarow": 3})
    assert env.step([2, None]) == [
        {
            "action": 2,
            "done": True,
            "info": {},
            "observation": {
                "board": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                "mark": 1,
            },
            "reward": 0.5,
        },
        {
            "action": 0,
            "done": False,
            "info": {},
            "observation": {
                "board": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                "mark": 2,
            },
            "reward": 0.5,
        },
    ]


def test_can_mark_out_of_bounds():
    beforeEach(configuration={"rows": 4, "columns": 5, "inarow": 3})
    assert env.step([10, None]) == [
        {
            "action": 10,
            "done": True,
            "info": {},
            "observation": {
                "board": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "mark": 1,
            },
            "reward": 0,
        },
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {
                "board": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "mark": 2,
            },
            "reward": 0.5,
        },
    ]


def test_can_mark_a_full_column():
    board = [1, 2, 0, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 0, 0]
    beforeEach(
        configuration={"rows": 4, "columns": 5, "inarow": 3},
        state=[{"observation": {"board": board}}, {"observation": {"board": board}}],
    )
    assert env.step([1, None]) == [
        {
            "action": 1,
            "done": True,
            "info": {},
            "observation": {"board": board, "mark": 1},
            "reward": 0,
        },
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"board": board, "mark": 2},
            "reward": 0.5,
        },
    ]


def test_can_win():
    board = [0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 0, 0, 1, 2, 0, 0, 0]
    board_post_move = board[:]
    board_post_move[0] = 1
    beforeEach(
        configuration={"rows": 4, "columns": 5, "inarow": 3},
        state=[{"observation": {"board": board}}, {"observation": {"board": board}}],
    )
    assert env.step([0, None]) == [
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"board": board_post_move, "mark": 1},
            "reward": 1,
        },
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"board": board_post_move, "mark": 2},
            "reward": 0,
        },
    ]


def test_can_tie():
    board = [0, 0, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    board_post_move = board[:]
    board_post_move[0] = 1
    board_post_move[1] = 2
    beforeEach(
        configuration={"rows": 4, "columns": 5, "inarow": 3},
        state=[{"observation": {"board": board}}, {"observation": {"board": board}}],
    )
    env.step([0, None])
    assert env.step([None, 1]) == [
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"board": board_post_move, "mark": 1},
            "reward": 0.5,
        },
        {
            "action": 1,
            "done": True,
            "info": {},
            "observation": {"board": board_post_move, "mark": 2},
            "reward": 0.5,
        },
    ]


def test_can_render():
    board = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 2, 1, 0, 1, 2, 1, 2, 1]
    beforeEach(
        configuration={"rows": 4, "columns": 5, "inarow": 3},
        state=[{"observation": {"board": board}}, {"observation": {"board": board}}],
    )
    assert env.render(True).strip() == """
+---+---+---+---+---+
| 0 | 0 | 0 | 0 | 0 |
+---+---+---+---+---+
| 0 | 0 | 2 | 0 | 0 |
+---+---+---+---+---+
| 0 | 1 | 2 | 1 | 0 |
+---+---+---+---+---+
| 1 | 2 | 1 | 2 | 1 |
+---+---+---+---+---+
""".strip()


def test_can_run_agents():
    def custom1():
        return 1
    def custom2():
        return 2
    beforeEach(
        configuration={"rows": 4, "columns": 5, "inarow": 3},
    )
    board = [0,0,0,0,0,0,1,0,0,0,0,1,2,0,0,0,1,2,0,0]
    assert env.run([custom1, custom2])[-1] == [
        {
            "action": 1,
            "done": True,
            "info": {},
            "observation": {"board": board, "mark": 1},
            "reward": 1,
        },
        {
            "action": 0,
            "done": True,
            "info": {},
            "observation": {"board": board, "mark": 2},
            "reward": 0,
        },
    ]

def test_can_evaluate():
    rewards = evaluate("connectx", ["random", "random"], num_episodes=2)
    assert (rewards[0][0] + rewards[0][1] == 1) and rewards[1][0] + rewards[1][1] == 1


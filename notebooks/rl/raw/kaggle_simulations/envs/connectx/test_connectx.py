from kaggle_simulations import make, evaluate, run

env = None


def beforeEach(state=None, configuration=None):
    global env
    steps = [] if state == None else [state]
    env = make("connectx", steps=steps, configuration=configuration, debug=True)


def test_to_json():
    beforeEach()
    json = env.toJSON()
    assert json["name"] == "connectx"
    assert json["rewards"] == [0.5, 0.5]
    assert json["statuses"] == ["ACTIVE", "INACTIVE"]
    assert json["specification"]["reward"]["type"] == ["number", "null"]


def test_can_reset():
    beforeEach()
    assert env.reset() == [
        {
            "action": 0,
            "status": "ACTIVE",
            "info": {},
            "observation": {"board": [0] * 42, "mark": 1},
            "reward": 0.5,
        },
        {
            "action": 0,
            "status": "INACTIVE",
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
            "status": "INACTIVE",
            "info": {},
            "observation": {
                "board": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                "mark": 1,
            },
            "reward": 0.5,
        },
        {
            "action": 0,
            "status": "ACTIVE",
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
            "status": "INVALID",
            "info": {},
            "observation": {
                "board": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "mark": 1,
            },
            "reward": None,
        },
        {
            "action": 0,
            "status": "DONE",
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
            "status": "INVALID",
            "info": {},
            "observation": {"board": board, "mark": 1},
            "reward": None,
        },
        {
            "action": 0,
            "status": "DONE",
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
            "status": "DONE",
            "info": {},
            "observation": {"board": board_post_move, "mark": 1},
            "reward": 1,
        },
        {
            "action": 0,
            "status": "DONE",
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
            "status": "DONE",
            "info": {},
            "observation": {"board": board_post_move, "mark": 1},
            "reward": 0.5,
        },
        {
            "action": 1,
            "status": "DONE",
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
    assert env.render(mode="ansi").strip() == """
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
            "status": "DONE",
            "info": {},
            "observation": {"board": board, "mark": 1},
            "reward": 1,
        },
        {
            "action": 0,
            "status": "DONE",
            "info": {},
            "observation": {"board": board, "mark": 2},
            "reward": 0,
        },
    ]

def test_can_evaluate():
    rewards = evaluate("connectx", ["random", "random"], num_episodes=2)
    assert (rewards[0][0] + rewards[0][1] == 1) and rewards[1][0] + rewards[1][1] == 1


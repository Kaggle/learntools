# import pytest
# from kaggle_simulations import env, errors


# def interpreter(state):
#     if state.get("done", False):
#         return {"observation": {"num": 0}}
#     return {**state, "info": {"num": state["observation"]["num"] + 1}}


# def renderer():
#     return "foofoo"


# def test_can_load_a_plain_function():
#     e = env(interpreter)
#     assert e.name == ""
#     assert e.description == ""
#     assert e.version == ""
#     newState = e.run({"observation": {"num": 1}})
#     assert newState["info"]["num"] == 2
#     assert newState["observation"]["num"] == 1


# def test_can_load_a_specification():
#     e = env(
#         {
#             "name": "foobar",
#             "version": "beta",
#             "description": "Foo Bar",
#             "interpreters": {"py": interpreter},
#             "renderers": {"py": renderer},
#         }
#     )
#     assert e.name == "foobar"
#     assert e.description == "Foo Bar"
#     assert e.version == "beta"
#     newState = e.run({"observation": {"num": 1}})
#     assert newState["info"]["num"] == 2
#     assert newState["observation"]["num"] == 1
#     assert e.render(newState) == "foofoo"


# def test_can_load_a_folder():
#     e = env("tictactoe")
#     assert e.name == "tictactoe"
#     assert e.description == "Classic Tic Tac Toe"
#     assert e.version == "1.0.0"
#     resetState = e.reset()
#     assert isinstance(resetState, dict)
#     assert isinstance(e.run(resetState), dict)
#     assert isinstance(e.render(resetState), str)


# def test_can_set_a_configuration():
#     def interpreter(state, config):
#         if state.get("done", False):
#             return {"observation": {"num": 0}}
#         return {
#             **state,
#             "info": {"num": state["observation"]["num"] + config.get("num", 0)},
#         }

#     e = env(interpreter, {"num": 5})
#     newState = e.run({"observation": {"num": 1}})
#     assert newState["info"]["num"] == 6

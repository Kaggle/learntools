# from kaggle_simulations import env, sim

# chess_env = None


# def beforeEach():
#     global chess_env
#     chess_env = env("chess")


# def test_can_reset():
#     beforeEach()
#     assert chess_env.reset() == {
#         "agents": [
#             {"action": "", "active": True, "info": {"pieces": "WHITE"}, "reward": 0.5},
#             {"action": "", "active": False, "info": {"pieces": "BLACK"}, "reward": 0.5},
#         ],
#         "info": {},
#         "observation": {
#             "board": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#         },
#         "done": False,
#     }


# def test_can_render():
#     beforeEach()
#     out = """r n b q k b n r
# p p p p p p p p
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# P P P P P P P P
# R N B Q K B N R"""
#     state = {
#         "observation": {
#             "board": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#         }
#     }
#     assert chess_env.render(state) == out


# def test_can_run_agents():
#     chess_sim = sim("chess", ["chess/agents/random.py", "chess/agents/random.py"])
#     rewards = chess_sim.run(10)["rewards"]
#     assert rewards[0] + rewards[1] == 1

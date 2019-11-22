from .connectx.connectx import connectx
from .tictactoe.tictactoe import tictactoe

all_envs = [connectx, tictactoe]
environments = {env["specification"]["name"]: env for env in all_envs}

from .connectx.connectx import connectx
from .nacl.nacl import nacl
from .tictactoe.tictactoe import tictactoe

all_envs = [connectx, nacl, tictactoe]
environments = {env["specification"]["name"]: env for env in all_envs}

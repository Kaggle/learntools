import gym
import json
import traceback
from .envs import environments
from .errors import DeadlineExceeded, FailedPrecondition, Internal, InvalidArgument
from .utils import (
    get,
    has,
    get_player,
    processSchema,
    schemas,
    structify,
    timeout,
    validateSchema,
)


# Follows interface at: https://github.com/openai/gym/blob/master/gym/core.py
class GymEnvironment(gym.Env):
    """
    TODO
    """

    def __init__(self, env, agents):
        self.env = env
        self.action_space = env.action_space
        self.observation_space = env.observation_space

        # Find the empty agent position and validate only one is marked None.
        self.position = None
        for index, agent in enumerate(agents):
            if agent == None:
                if self.position != None:
                    raise InvalidArgument("Only one agent can be marked 'None'")
                self.position = index

        if self.position == None:
            raise InvalidArgument("One agent must be marked 'None'")
        self.agents = agents
        self.reset()

    def step(self, action):
        """
        TODO
        """
        self.env.step(self.env.get_actions(agents=self.agents, none_action=action))
        self.__advance_state()
        return self.state

    def reset(self):
        """
        TODO
        """
        self.env.reset(len(self.agents))
        self.__advance_state()
        return self.state

    def render(self, **kwargs):
        """
        TODO
        """
        return self.env.render(**kwargs)

    def __advance_state(self):
        # Advance the state until the agents turn.
        while not self.env.done and self.env.state[self.position].status == "INACTIVE":
            self.env.step(self.env.get_actions(agents=self.agents))

    @property
    def state(self):
        agent = self.env.state[self.position]
        return agent.observation, agent.reward, agent.status != "ACTIVE", agent.info

    @property
    def done(self):
        return self.env.done

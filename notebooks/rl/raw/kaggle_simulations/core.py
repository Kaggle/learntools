import copy
import gym
import json
import traceback
from .envs import environments
from .errors import DeadlineExceeded, FailedPrecondition, Internal, InvalidArgument
from .utils import get, has, call, get_player, processSchema, schemas, structify, timeout, validateSchema


def evaluate(environment, agents=[], configuration={}, steps=[], num_episodes=1):
    """
    TODO
    """
    e = make(environment, configuration, steps)
    rewards = [[]] * num_episodes
    for i in range(num_episodes):
        last_state = e.run(agents)[-1]
        rewards[i] = [state.reward for state in last_state]
    return rewards


def run(environment, agents=[], configuration={}, steps=[], debug=False):
    """
    TODO
    """
    e = make(environment, configuration, steps, debug=debug)
    e.run(agents)
    agents = [a if has(a, str) else "func" for a in agents]
    return structify({**e.toJSON(), "agents": agents})


def make(environment, configuration={}, steps=[], debug=False):
    """
    TODO
    """
    if has(environment, str) and has(environments, dict, path=[environment]):
        return Environment(**environments[environment], configuration=configuration, steps=steps, debug=debug)
    elif callable(environment):
        return Environment(interpreter=environment, configuration=configuration, steps=steps, debug=debug)
    elif has(environment, path=["interpreter"], isCallable=True):
        return Environment(**environment, configuration=configuration, steps=steps, debug=debug)
    raise InvalidArgument("Unknown Environment Specification")


class Environment(object):
    """
    TODO
    """

    def __init__(
        self,
        specification={},
        configuration={},
        steps=[],
        agents={},
        interpreter=None,
        renderer=None,
        html_renderer=None,
        debug=False,
    ):
        self.debug = debug

        err, specification = self.__process_specification(specification)
        if err:
            raise InvalidArgument("Specification Invalid: " + err)
        self.specification = structify(specification)

        err, configuration = processSchema(
            {"type": "object", "properties": self.specification.configuration},
            {} if configuration == None else configuration,
        )
        if err:
            raise InvalidArgument("Configuration Invalid: " + err)
        self.configuration = structify(configuration)

        if not callable(interpreter):
            raise InvalidArgument("Interpreter is not Callable.")
        self.interpreter = interpreter

        if not callable(renderer):
            raise InvalidArgument("Renderer is not Callable.")
        self.renderer = renderer

        if callable(html_renderer):
            html_renderer = html_renderer()
        self.html_renderer = get(html_renderer, str, "")

        if not all([callable(a) for a in agents.values()]):
            raise InvalidArgument("Default agents must be Callable.")
        self.agents = structify(agents)

        if steps == None or len(steps) == 0:
            self.reset()
        else:
            self.set_state(steps[-1])
            self.steps = steps[0:-1] + self.steps

    def step(self, actions):
        """
        TODO
        """

        if self.done:
            raise FailedPrecondition("Environment done, reset required.")
        if not actions or len(actions) != len(self.state):
            raise InvalidArgument(f"{len(self.state)} actions required.")

        actionState = [0] * len(self.state)
        for index, action in enumerate(actions):
            actionState[index] = {**self.state[index], "action": None}

            if isinstance(action, DeadlineExceeded):
                self.__debug_print(f"Timeout: {str(action)}")
                actionState[index]["status"] = "TIMEOUT"
            elif isinstance(action, BaseException):
                self.__debug_print(f"Error: {str(action)}")
                actionState[index]["status"] = "ERROR"
            else:
                err, data = processSchema(self.state_schema.properties.action, action)
                if err:
                    self.__debug_print(f"Invalid Action: {str(err)}")
                    actionState[index]["status"] = "INVALID"
                    actionState[index]["action"] = action
                else:
                    actionState[index]["action"] = data

        self.state = self.__run_interpreter(actionState)
        self.steps.append(self.state)

        return self.state

    def run(self, agents, state=None):
        """
        TODO
        """

        self.reset(len(agents)) if state == None else self.set_state(state)
        while not self.done:
            self.step(self.get_actions(agents))
        return self.steps

    def reset(self, num_agents=None):
        """
        TODO
        """

        if num_agents == None:
            num_agents = self.specification.agents[0]

        # Get configuration default state.
        self.set_state([{} for _ in range(num_agents)])
        # Reset all agents to status=INACTIVE (copy out values to reset afterwards).
        statuses = [a.status for a in self.state]
        for agent in self.state:
            agent.status = "INACTIVE"
        # Give the interpreter an opportunity to make any initializations.
        self.set_state(self.__run_interpreter(self.state))
        # Replace the starting "status" if still "done".
        if self.done and len(self.state) == len(statuses):
            for i in range(len(self.state)):
                self.state[i].status = statuses[i]
        return self.state

    def set_state(self, state=[]):
        if len(state) not in self.specification.agents:
            raise InvalidArgument(f"{len(state)} is not a valid number of agent(s).")

        self.state = structify([self.__get_state(index, s) for index, s in enumerate(state)])
        self.steps = [self.state];
        return self.state

    def render(self, **kwargs):
        """
        TODO
        """

        mode = get(kwargs, str, "human", path=["mode"])
        if mode == "ansi" or mode == "human":
            args = [self.state, self]
            out = self.renderer(*args[:self.renderer.__code__.co_argcount])
            if mode == "ansi":
                return out
            print(out)
        elif mode == "html" or mode == "ipython":
            autoplay = get(kwargs, bool, self.done, path=["autoplay"])
            window_kaggle = {
                "environment": self.toJSON(),
                "header": get(kwargs, bool, False, path=["header"]),
                "autoplay": autoplay,
                "step": 0 if autoplay else (len(self.steps) - 1),
                "controls": get(kwargs, bool, self.done, path=["controls"]),
                "settings": get(kwargs, bool, False, path=["settings"]),
                "speed": get(kwargs, int, 500, path=["speed"]),
                "animate": get(kwargs, bool, False, path=["animate"]),
            }
            player_html = get_player(window_kaggle, self.html_renderer)
            if mode == "html":
                return player_html
            from IPython.core.display import display, HTML
            player_html = player_html.replace('"', '&quot;')
            width = get(kwargs, int, 300, path=["width"])
            height = get(kwargs, int, 300, path=["height"])
            html = f'<iframe srcdoc="{player_html}" width="{width}" height="{height}" frameborder="0" />'
            display(HTML(html))
        elif mode == "json":
            return json.dumps(self.toJSON(), sort_keys=True)
        else:
            raise InvalidArgument("Available render modes: human, ansi, html, ipython")

    def gym(self, agents=[], init=None, observation=None, reward=None, done=None, info=None):
        return GymEnvironment(self, agents, init, observation, reward, done, info)

    @property
    def name(self):
        return get(self.specification, str, "", ["name"])

    @property
    def version(self):
        return get(self.specification, str, "", ["version"])

    @property
    def description(self):
        return get(self.specification, str, "", ["description"])

    @property
    def max_steps(self):
        return get(self.specification, int, 0, ["max_steps"])

    @property
    def agent_timeout(self):
        return get(self.specification, int, 0, ["agent_timeout"])

    @property
    def done(self):
        return all(s.status != "ACTIVE" for s in self.state)

    def toJSON(self):
        """
        TODO
        """
        spec = self.specification
        return copy.deepcopy(
            {
                "name": spec.name,
                "title": spec.title,
                "description": spec.description,
                "version": spec.version,
                "configuration": self.configuration,
                "max_steps": self.max_steps,
                "specification": {
                    "action": spec.action,
                    "agents": spec.agents,
                    "configuration": spec.configuration,
                    "info": spec.info,
                    "observation": spec.observation,
                    "reward": spec.reward,
                    "reset": spec.reset
                },
                "steps": self.steps,
                "rewards": [state.reward for state in self.steps[-1]],
                "statuses": [state.status for state in self.steps[-1]],
                "schema_version": 1,
            }
        )

    def __get_state(self, position, state):
        key = f"__state_schema_{position}"
        if not hasattr(self, key):
            defaults = self.specification.reset
            props = structify(copy.deepcopy(self.state_schema.properties))

            # Assign different defaults based upon agent position.
            for d in defaults:
                newDefault = None
                if hasattr(props, d):
                    if not has(defaults[d], list):
                        newDefault = defaults[d]
                    elif len(defaults[d]) > position:
                        newDefault = defaults[d][position]
                if newDefault != None:
                    if props[d].type == "object" and has(newDefault, dict):
                        for k in newDefault:
                            if hasattr(props[d].properties, k):
                                props[d].properties[k].default = newDefault[k]
                    elif props[d].type != "object":
                        props[d].default = newDefault
            setattr(self, key, {**self.state_schema, "properties": props})

        err, data = processSchema(getattr(self, key), state)
        if err:
            raise InvalidArgument(
                f"Default state generation failed for #{position}: " + err
            )
        return data

    @property
    def state_schema(self):
        if not hasattr(self, "__state_schema"):
            spec = self.specification
            # schema = structify(schemas["state"])
            self.__state_schema = {
                **schemas["state"],
                "properties": {
                    **schemas.state.properties,
                    "action": spec.action,
                    "reward": spec.reward,
                    "info": {
                        **schemas.state.properties.info,
                        "properties": spec.info,
                    },
                    "observation": {
                        **schemas.state.properties.observation,
                        "properties": spec.observation,
                    },
                },
            }
        return structify(self.__state_schema)

    def get_actions(self, agents=[], none_action=None):
        if len(agents) != len(self.state):
            raise InvalidArgument("Number of agents must match the state length")

        actions = [0] * len(agents)
        for i, agent in enumerate(agents):
            obs = self.state[i].observation
            if self.state[i].status != "ACTIVE":
                actions[i] = None
            elif agent == None:
                actions[i] = none_action
            elif has(agent, str) and has(self.agents, path=[agent], isCallable=True):
                actions[i] = self.__run_agent(self.agents[agent], obs)
            elif not callable(agent):
                actions[i] = agent
            else:
                actions[i] = self.__run_agent(agents[i], obs)
        return actions

    def __run_agent(self, agent, observation):
        args = [observation, structify(self.configuration)]
        args = args[:agent.__code__.co_argcount]
        try:
            return timeout(agent, *args, seconds=self.agent_timeout)
        except Exception as e:
            return e

    def __run_interpreter(self, state):
        try:
            args = [structify(state), self]
            new_state = structify(self.interpreter(*args[:self.interpreter.__code__.co_argcount]))
            for agent in new_state:
                if agent.status not in self.state_schema.properties.status.enum:
                    self.__debug_print(f"Invalid Action: {agent.status}")
                    agent.status = "INVALID"
                if agent.status in ["ERROR", "INVALID", "TIMEOUT"]:
                    agent.reward = None
            return new_state
        except Exception as err:
            raise Internal("Error running environment: " + str(err))

    def __process_specification(self, spec):
        if has(spec, path=["reward"]):
            reward = spec["reward"]
            reward_type = get(reward, str, "number", ["type"])
            if reward_type not in ["integer", "number"]:
                return ("type must be an integer or number", None)
            reward["type"] = [reward_type, "null"]
        return processSchema(schemas.specification, spec)

    def __debug_print(self, message):
        if self.debug:
            print(message)


# Follows interface at: https://github.com/openai/gym/blob/master/gym/core.py
class GymEnvironment(gym.Env):
    """
    TODO
    """

    def __init__(self, env, agents, init=None, observation=None, reward=None, done=None, info=None):
        self.env = env
        self.action_space = None
        self.observation_space = None

        # Override to process state outputs.
        self.overrides = {
            "observation": observation,
            "reward": reward,
            "done": done,
            "info": info
        }

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

        if init:
            init(self)

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

        def get_property(name, default):
            if self.overrides[name] == None:
                return default
            args = [agent, self.env]
            return call(self.overrides, path=[name], args=args, default=self.overrides[name])

        return [
            get_property("observation", agent.observation),
            get_property("reward", agent.reward),
            get_property("done", agent.status != "ACTIVE"),
            get_property("info", agent.info)
        ]

    @property
    def done(self):
        return self.env.done

import copy
import gym
import traceback
from .envs import environments
from .errors import FailedPrecondition, Internal, InvalidArgument
from .utils import get, has, get_player, processSchema, schemas, structify, validateSchema


def evaluate(environment, agents=[], configuration={}, state=None, num_episodes=1):
    e = make(environment, configuration, state)
    rewards = [[]] * num_episodes
    for i in range(num_episodes):
        last_state = e.run(agents, state)[-1]
        rewards[i] = [state.reward for state in last_state]
    return rewards


def run(environment, agents=[], configuration={}, state=None):
    e = make(environment, configuration, state)
    e.run(agents, state)
    agents = [a if has(a, str) else "func" for a in agents]
    return structify({**e.toJSON(), "agents": agents})


def make(environment, configuration={}, state=None):
    if has(environment, str) and has(environments, dict, path=[environment]):
        return Environment(**environments[environment], configuration=configuration, state=state)
    elif callable(environment):
        return Environment(interpreter=environment, configuration=configuration, state=state)
    elif has(environment, path=["interpreter"], isCallable=True):
        return Environment(**environment, configuration=configuration, state=state)
    raise InvalidArgument("Unknown Environment Specification")


class Environment(object):
    def __init__(
        self,
        specification={},
        configuration={},
        state=None,
        interpreter=None,
        renderer=None,
        html_renderer=None,
        agents={},
    ):
        err, specification = processSchema(schemas.specification, specification)
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

        self.reset() if state == None else self.set_state(state)
        

    def step(self, actions):
        if self.done:
            raise FailedPrecondition("Environment done, reset required.")
        if not actions or len(actions) != len(self.state):
            raise InvalidArgument(f"{len(self.state)} actions required.")

        actionState = [0] * len(self.state)
        for index, action in enumerate(actions):
            err, data = processSchema(self.state_schema.properties.action, action)
            if err:
                raise InvalidArgument("Action Invalid: " + err)
            actionState[index] = {**self.state[index], "action": data}

        self.state = self.__run_interpreter(actionState)
        self.steps.append(self.state)

        return self.state

    def run(self, agents, state=None):
        self.reset(len(agents)) if state == None else self.set_state(state)
        while not self.done:
            self.step(self.get_actions(agents))
        return self.steps

    def reset(self, num_agents=None):
        if num_agents == None:
            num_agents = self.specification.agents.minimum
        # Get configuration default state.
        self.set_state([{} for _ in range(num_agents)])
        # Reset all agents to done (copy out values to reset afterwards).
        dones = [a.done for a in self.state]
        for agent in self.state:
            agent.done = True
        # Give the interpreter an opportunity to make any initializations.
        self.set_state(self.__run_interpreter(self.state))
        # Replace the starting "dones" if still "done".
        if self.done and len(self.state) == len(dones):
            for i in range(len(self.state)):
                self.state[i].done = dones[i]
        return self.state

    def set_state(self, state=[]):
        minimum = self.specification.agents.minimum
        maximum = self.specification.agents.maximum

        if len(state) < minimum:
            raise InvalidArgument(f"At least {minimum} agent(s) required.")
        elif maximum and len(state) > maximum:
            raise InvalidArgument(f"At most {maximum} agent(s) required.")

        self.state = structify([self.__get_state(index, s) for index, s in enumerate(state)])
        self.steps = [self.state];
        return self.state

    def render(self, **kwargs):
        mode = get(kwargs, str, "human", path=["mode"])
        if mode == "ansi" or mode == "human":
            args = [self.state, self]
            out = self.renderer(*args[:self.renderer.__code__.co_argcount])
            if mode == "ansi":
                return out
            print(out)
        elif mode == "html" or mode == "ipython":
            autoplay = get(kwargs, bool, True, path=["autoplay"])
            window_kaggle = {
                "environment": {**self.toJSON(), "steps": self.steps},
                "header": get(kwargs, bool, False, path=["header"]),
                "autoplay": autoplay,
                "step": 0 if autoplay else (len(self.steps) - 1),
                "controls": get(kwargs, bool, True, path=["controls"]),
                "speed": get(kwargs, int, 500, path=["speed"])
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
        else:
            raise InvalidArgument("Available render modes: human, ansi, html, ipython")

    def gym(self, agents):
        return GymEnvironment(self, agents)

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
    def done(self):
        return all(s.done for s in self.state)

    @property
    def action_space(self):
        return self.__get_space(self.specification.action)

    @property
    def observation_space(self):
        return {
            k: self.__get_space(v) for k, v in self.specification.observation.items()
        }

    def toJSON(self):
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
                },
                "steps": self.steps,
                "rewards": [state.reward for state in self.steps[-1]],
            }
        )

    def __get_state(self, position, state):
        key = f"__state_schema_{position}"
        if not hasattr(self, key):
            defaults = self.specification.agents.defaults
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

    def get_actions(self, agents=[], done_action=None, none_action=None):
        if len(agents) != len(self.state):
            raise InvalidArgument("Number of agents must match the state length")

        actions = [0] * len(agents)
        for i, agent in enumerate(agents):
            obs = self.state[i].observation
            if self.state[i].done:
                actions[i] = done_action
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
        try:
            args = [observation, structify(self.configuration)]
            return agent(*args[:agent.__code__.co_argcount])
        except Exception as err:
            raise Internal("Error running agent: " + str(err))

    def __run_interpreter(self, state):
        try:
            args = [structify(state), self]
            return structify(self.interpreter(*args[:self.interpreter.__code__.co_argcount]))
        except Exception as err:
            raise Internal("Error running environment: " + str(err))

    def __get_space(self, spec):
        if hasattr(spec, "type") and spec.type == "integer" and spec.minimum == 0:
            return gym.spaces.Discrete(spec.maximum)


# Follows interface at: https://github.com/openai/gym/blob/master/gym/core.py
class GymEnvironment(gym.Env):
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
        self.env.step(self.env.get_actions(agents=self.agents, none_action=action))
        self.__advance_state()
        return self.state

    def reset(self):
        self.env.reset(len(self.agents))
        self.__advance_state()
        return self.state

    def render(self, **kwargs):
        return self.env.render(**kwargs)
            

    def __advance_state(self):
        # Advance the state until the agents turn.
        while not self.env.done and self.env.state[self.position].done:
            self.env.step(self.env.get_actions(agents=self.agents))

    @property
    def state(self):
        agent = self.env.state[self.position]
        return agent.observation, agent.reward, agent.done, agent.info

    @property
    def done(self):
        return self.env.done

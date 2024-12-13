from gymnasium.envs.registration import register

register(
    id="rl_worlds/RandomWalk-v0",
    entry_point="rl_worlds.envs:RandomWalkEnv",
    kwargs={
        "num_states": 5,
        "start_state": 2,
        "use_numeric_state_representation": False,
    },
)

register(
    id="rl_worlds/ThousandStatesRandomWalk-v0",
    entry_point="rl_worlds.envs:ThousandStatesRandomWalkEnv",
)

register(
    id="rl_worlds/GridWorld-v0",
    entry_point="rl_worlds.envs:GridWorldEnv",
    kwargs={
        "grid_size": (7, 10),
        "start_state": (3, 0),
        "goal_states": [(3, 7)],
        "max_steps": 50,
    },
)

register(
    id="rl_worlds/WindyGridWorld-v0",
    entry_point="rl_worlds.envs:WindyGridWorldEnv",
    kwargs={
        "grid_size": (7, 10),
        "start": (3, 0),
        "goal_states": [(3, 7)],
        "max_steps": 50,
    },
)

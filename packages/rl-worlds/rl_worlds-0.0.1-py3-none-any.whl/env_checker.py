from gymnasium.utils.env_checker import check_env
from rl_worlds.envs.grid_world import GridWorldEnv
from rl_worlds.envs.random_walk import RandomWalkEnv
from rl_worlds.envs.windy_grid_world import WindyGridWorldEnv
import gymnasium as gym


#env = gym.make("rl_worlds/RandomWalk-v0")
env = gym.make("rl_worlds/ThousandStatesRandomWalk-v0")
# env = gym.make("rl_worlds/GridWorld-v0")
# env = gym.make("rl_worlds/WindyGridWorld-v0")

check_env(env.unwrapped)


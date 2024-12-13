from typing import List
import gymnasium as gym
from pprint import pprint
import numpy as np
from gymnasium.spaces import Discrete, Box, Tuple


class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(
        self,
        grid_size: tuple = (7, 10),
        start_state: tuple = (3, 0),
        goal_states: List[tuple] = [(3, 7)],
        max_steps: int = 50,
        **kwargs,
    ):
        super(GridWorldEnv, self).__init__()

        # Define the grid world dimensions
        self.grid_size = grid_size
        self.start_state = start_state
        self.terminal_states = goal_states
        self.max_steps = max_steps

        # Define the action space (0: up, 1: right, 2: down, 3: left)
        self.action_space = Discrete(4)

        # Define the observation space (position on the grid)
        self.observation_space = Tuple(
            (
                Box(low=0, high=grid_size[0] - 1, shape=(), dtype=np.int32),
                Box(low=0, high=grid_size[1] - 1, shape=(), dtype=np.int32),
            )
        )

        # Initialize state
        self.state = None
        self.steps_taken = 0

        # Action mappings
        self.action_map = {
            0: np.array([-1, 0]),  # up
            1: np.array([0, 1]),  # right
            2: np.array([1, 0]),  # down
            3: np.array([0, -1]),  # left
        }

        self.action_itos = {0: "up", 1: "right", 2: "down", 3: "left"}
        self.action_stoi = {value: key for key, value in self.action_itos.items()}

        self.force_grid = kwargs.get("force_grid", None)
        self.force_direction = kwargs.get("force_direction", "up").lower()

        if self.force_grid is not None:
            assert (
                self.force_grid.shape == self.grid_size
            ), "Force grid should have the same size as the original grid size"

            assert (
                self.force_direction in self.action_stoi.keys()
            ), f"Force direction should be one of these: {self.action_stoi.keys()}"

    def reset(self, seed=None, options=None):
        """Reset the environment to the starting state."""
        super().reset(seed=seed)

        self.state = self.start_state
        self.steps_taken = 0

        return self.state, {}

    def step(self, action):
        """Execute an action and return next state, reward, terminated, truncated, and info."""
        self.steps_taken += 1

        # Get the change in position based on the action
        delta = self.action_map[action]
        state = np.array(self.state, dtype=np.int32)
        new_state = state + delta

        # Ensure new state is within bounds
        new_state = self._clip_bounds(state=new_state)

        if self.force_grid is not None:
            new_state = self._apply_force(state=new_state)

        # Update state
        self.state = tuple(new_state.astype(np.int32))

        reward = -1.0 if self.state not in self.terminal_states else 0.0

        terminated = self.state in self.terminal_states
        truncated = self.steps_taken >= self.max_steps

        return self.state, reward, terminated, truncated, {}

    def _apply_force(self, state):
        action_i = self.action_stoi[self.force_direction]
        state = state + self.force_grid[tuple(state)] * self.action_map[action_i]

        # Ensure new state is within bounds
        state = self._clip_bounds(state=state)

        return state

    def _clip_bounds(self, state):
        state[0] = np.clip(state[0], 0, self.grid_size[0] - 1)
        state[1] = np.clip(state[1], 0, self.grid_size[1] - 1)

        return state

    def render(self):
        """Render the current state of the environment."""
        grid = np.zeros(self.grid_size, dtype=np.int32).astype("object")
        for t_state in self.terminal_states:
            grid[t_state] = str("G")  # Mark terminal states

        grid[tuple(self.state)] = str("A")  # Mark the agent's current position

        pprint(grid)


# if __name__ == "__main__":
#     # force_grid = np.zeros(shape=(7, 10), dtype="float")
#     # force_grid[:, [3, 4, 5, 8]] = 1.0
#     # force_grid[:, [6, 7]] = 2.0
#     # force_direction = "up"

#     # pprint(force_grid)
#     # # Example usage:
#     # env = GridWorldEnv(force_grid=force_grid, force_direction=force_direction)
#     # obs, _ = env.reset()
#     # env.render()

#     # done = False
#     # while not done:
#     #     action = env.action_space.sample()  # Random action
#     #     obs, reward, terminated, truncated, info = env.step(action)
#     #     done = terminated or truncated
#     #     print(
#     #         f"Action: {env.action_itos[action]}, State: {obs}, Reward: {reward}, Done: {done}"
#     #     )
#     #     env.render()

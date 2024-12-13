import random
from rl_worlds.envs.random_walk import RandomWalkEnv


class ThousandStatesRandomWalkEnv(RandomWalkEnv):
    metadata = {"render_modes": [], "render_fps": 4}

    def __init__(self, **kwargs):
        super().__init__(
            num_states=1000,
            start_state=500,
            use_numeric_state_representation=True,
            **kwargs,
        )

    def step(self, action):
        # Perform the random walk step (ignoring action, random choice between left/right)
        direction = random.choice([-1, 1])  # -1 for left, +1 for right
        self.state_idx += direction * random.randint(1, 100)

        # Check if we've reached the terminal state
        if self.state_idx < 0:
            done = True
            reward = 0  # Left terminal state, no reward
            self.state_idx = -1  # Setting state_idx to left terminal state

        elif self.state_idx >= self.num_non_terminal_states:
            done = True
            reward = 1  # Right terminal state, reward of +1
            self.state_idx = (
                self.num_non_terminal_states
            )  # Setting state_idx to right terminal state

        else:
            done = False
            reward = 0  # All other states, no reward

        observation = self.idx_to_state[self.state_idx]

        return observation, reward, done, False, {}

    def render(self):
        raise Exception("Rendering unavailable due to large state space.")

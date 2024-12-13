import numpy as np

from rl_worlds.envs.grid_world import GridWorldEnv


class WindyGridWorldEnv(GridWorldEnv):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(
        self,
        grid_size=(7, 10),
        start=(3, 0),
        goal_states=[(3, 7)],
        max_steps: int = 50,
        **kwargs,
    ):
        snb_force_grid = np.zeros(shape=(7, 10), dtype="float")
        snb_force_grid[:, [3, 4, 5, 8]] = 1.0
        snb_force_grid[:, [6, 7]] = 2.0

        force_grid = kwargs.get("force_grid", snb_force_grid)
        force_direction = kwargs.get("force_direction", "up").lower()

        super().__init__(
            grid_size=grid_size,
            start_state=start,
            goal_states=goal_states,
            max_steps=max_steps,
            force_grid=force_grid,
            force_direction=force_direction,
        )

if __name__ == "__main__":
    env = WindyGridWorldEnv()
    obs, _ = env.reset()
    env.render()

    done = False
    while not done:
        action = env.action_space.sample()  # Random action
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        print(
            f"Action: {env.action_itos[action]}, State: {obs}, Reward: {reward}, Done: {done}"
        )
        env.render()

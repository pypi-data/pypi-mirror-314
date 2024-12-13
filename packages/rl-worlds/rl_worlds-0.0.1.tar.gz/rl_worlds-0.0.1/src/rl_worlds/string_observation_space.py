import random
from gymnasium.spaces import Space
from typing import List


class StringObservationSpace(Space):
    def __init__(self, non_terminal_states: List, terminal_state: str):
        super().__init__((), str)
        self.non_terminal_states = non_terminal_states
        self.terminal_state = terminal_state
        self.all_states = set(self.non_terminal_states + [self.terminal_state])

    def contains(self, x):
        return x in self.all_states

    def sample(self):
        return random.choice(self.non_terminal_states)
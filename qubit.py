import random  # Not random :(
from utils import *

class Qubit:
    def __init__(self, alpha: complex, beta: complex) -> None:
        self.alpha = alpha
        self.beta = beta
        self.weights: list[complex] = [self.alpha, self.beta]

    def measure(self):
        probs: list[complex] = [abs(self.alpha) ** 2, abs(self.beta) ** 2]
        result = random.choices([0, 1], weights=probs)[0]  # Collapse!
        if result == 0:
            self.alpha, self.beta = 1, 0  # Maintain state
            return '|0⟩'  # Collapsed into 0 state
        else:
            self.alpha, self.beta = 0, 1  # Maintain state
            return '|1⟩'  # Collpased into 1 state

#print(apply_gate("H", Qubit(inv_root2, inv_root2).weights))

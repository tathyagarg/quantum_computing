import random
from utils import *
import math

class Qubit:
    def __init__(self, *weights) -> None:
        self.W: list[complex] = [[w] for w in weights]

        self.digits = int(math.log2(len(self.W)))

    def measure(self):
        probs: list[complex] = [abs(w)**2 for w in self.W]
        result = random.choices(range(len(self.W)), weights=probs)[0]  # Collapse!

        for i in range(len(self.W)):
            if i != result:
                self.W[i] = 0
        self.W[result] = 1
        
    def __repr__(self) -> str:
        result = ''
        for binary in range(2**self.digits):
            result += f'{self.W[binary][0]}|{bin(binary)[2:]:<0{self.digits}}⟩ + '

        return result[:-3]
    
def factor(matrix):
    print(matrix)
    if len(matrix) == 4:
        w, x, y, z = matrix
        w, x, y, z = w[0], x[0], y[0], z[0]
        alpha_a = w + x
        alpha_b = w + y

        beta_a = 1 - alpha_a
        beta_b = 1 - alpha_b

        return Qubit(alpha_a, beta_a), Qubit(alpha_b, beta_b)
    else:
        raise Exception("Unsupported operation.")

a, b, c, d = Qubit(0, 1), Qubit(0, 1), Qubit(1/2, 0, 1/2, 0), Qubit(1, 0)

print(f"{a = }\n{b = }\n")
a, b = factor(apply_gate('CNOT', tensor_product(a, b)))

print(f"{a = }\n{b = }\n{c = }")

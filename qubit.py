import random
from utils import *
import math

class Qubit:
    def __init__(self, *weights) -> None:
        self.W: list[complex] = [[w] for w in weights]

        self.digit_count = int(math.log2(len(self.W)))  # number of digits

    def measure(self):
        probs: list[complex] = [abs(w[0])**2 for w in self.W]
        result = random.choices(range(len(self.W)), weights=probs)[0]  # Collapse!

        for i in range(len(self.W)):
            if i != result:
                self.W[i] = [0]
        self.W[result] = [1]

        return self
        
    def __repr__(self) -> str:
        result = ''
        for binary in range(2**self.digit_count):
            result += f'{self.W[binary][0]}|{bin(binary)[2:]:<0{self.digit_count}}⟩ + '

        return result[:-3]
    
    def __getitem__(self, idx):
        return self.W[idx]
    
    def __len__(self):
        return len(self.W)
    
class DefinedQubit(Qubit):
    def __init__(self, integer, digit_count=0) -> None:
        self.digit_count = digit_count or math.ceil(math.log2(integer))  # `l` from the paper
        weights = [i == integer for i in range(self.digit_count)]

        super().__init__(*weights)
        self.digits = list(map(int, bin(integer)[2:]))

def factor(matrix):
    length = len(matrix)

    if length == 2:
        return Qubit(*unpack(*matrix))
    elif length == 4:
        w, x, y, z = unpack(*matrix)
        alpha_a = w + x
        alpha_b = w + y

        beta_a = 1 - alpha_a
        beta_b = 1 - alpha_b

        return Qubit(alpha_a, beta_a), Qubit(alpha_b, beta_b)
    elif length == 8:
        a, b, c, d, e, f, g, h = unpack(*matrix)

        alpha_a = e / (h + e) if h + e != 0 else (d / (a + d) if a + d != 0 else 0)
        alpha_b = f / (h + f) if h + f != 0 else (c / (a + c) if a + c != 0 else 0)
        alpha_c = g / (h + g) if h + g != 0 else (b / (a + b) if a + b != 0 else 0)

        beta_a = 1 - alpha_a
        beta_b = 1 - alpha_b
        beta_c = 1 - alpha_c

        return Qubit(alpha_a, beta_a), Qubit(alpha_b, beta_b), Qubit(alpha_c, beta_c)
    else:
        raise Exception("Unsupported operation.")

a, b, c, d = Qubit(0, 1), Qubit(0, 1), Qubit(1/2, 0, 1/2, 0), Qubit(0, 1)

print(factor(apply_gate('H', a)).measure())

# print(f"{a = }\n{b = }\n{d = }\n")
# a, b, d = factor(apply_gate('CCNOT', tensor_product(a, b, d)))

# print(f"{a = }\n{b = }\n{d = }")

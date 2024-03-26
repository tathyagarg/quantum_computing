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

class State:
    def __init__(self, qubits: list[Qubit | DefinedQubit] | int) -> None:
        if isinstance(qubits, int):
            self.qubits = [Qubit([(0, 1), (1, 0)][i == '0']) for i in bin(qubits)[2:]]
        else:
            self.qubits = list(qubits)

    def measure(self, bits=None):
        if isinstance(bits, (list, tuple)) or bits is None:
            target = bits or range(len(self.qubits))
            for i in target:
                self.qubits[i] = self.qubits[i].measure()
        else:
            self.qubits[bits] = self.qubits[bits].measure()

        return self
    
    def __repr__(self) -> str:
        return str(self.qubits)


def factor(matrix):
    length = len(matrix)

    if length == 2:
        return Qubit(*unpack(*matrix))
    elif length == 4:
        """
            We know because of the properties of a Qubit,
                |alpha_a|^2 + |beta_a|^2 = 1     --(1)
                |alpha_b|^2 + |beta_b|^2 = 1     --(2)
            
            Our input matrix = [alpha_a*alpha_b, alpha_a*beta_b, beta_a*alpha_b, beta_a*beta_b] = [alpha_a, beta_a] (tensor-product) [alpha_b, beta_b]
            Let w = alpha_a * alpha_b,
                x = alpha_a * beta_b,
                y = bete_a * alpha_b,
                z = bete_a * beta_b (Irrelevant in our calculations)

            Computing |w|^2 + |x|^2, we get |alpha_a|^2 => |alpha_a| = sqrt( |w|^2 + |x|^2 )
            Similarly, we get |alpha_b| = sqrt( |w|^2 + |y|^2 )
            
            From Equation (1),
                |beta_a|^2 = 1 - |alpha_a|^2
                => |beta_a| = sqrt(1 - |alpha_a|^2)
            Similarly from Equation (2),
                |beta_b| = sqrt(1 - |alpha_b|^2)
        """

        w, x, y, z = unpack(*matrix)

        w = abs(w) ** 2
        x = abs(x) ** 2
        y = abs(y) ** 2
        
        alpha_a_sqr = w + x
        alpha_b_sqr = w + y

        beta_a = (1 - alpha_a_sqr) ** 0.5
        beta_b = (1 - alpha_b_sqr) ** 0.5

        return Qubit(alpha_a_sqr ** 0.5, beta_a), Qubit(alpha_b_sqr ** 0.5, beta_b)
    elif length == 8:
        # TODO
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

print(a, b, State(factor(apply_gate('CNOT', tensor_product(a, b)))).measure(), sep='\n')  # TODO, make qubits with multiple digits (isnt this just a basis?)

# print(f"{a = }\n{b = }\n{d = }\n")
# a, b, d = factor(apply_gate('CCNOT', tensor_product(a, b, d)))

# print(f"{a = }\n{b = }\n{d = }")

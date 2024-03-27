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
    def transform(n):
        """
            This function can be defined as
                f(x) = |x|^2
            And helps in calculating probabilities.
        """
        return abs(n) ** 2

    length = len(matrix)

    if length == 2:
        return Qubit(*unpack(*matrix))
    elif length == 4:
        """
            We know because of the properties of a Qubit,
                |alpha_n|^2 + |beta_n|^2 = 1  --(2)
            For any n
            
            Our input matrix = [a1*a2, a1*b2, b1*a2, b1*b2] = [a1, b1] (tensor-product) [a2, b2]
            Let w = a1 * a2,
                x = a1 * b2,
                y = bete_1 * a2,
                z = bete_1 * b2 (Irrelevant in our calculations)

            Computing |w|^2 + |x|^2, we get |a1|^2 => |a1| = sqrt( |w|^2 + |x|^2 )
            Similarly, we get |a2| = sqrt( |w|^2 + |y|^2 )
            
            From Equation (1) with n = 1,
                |b1|^2 = 1 - |a1|^2
                => |b1| = sqrt(1 - |a1|^2)
            Similarly with n = 2,
                |b2| = sqrt(1 - |a2|^2)
        """

        w, x, y, z = list(map(transform, unpack(*matrix)))
        
        a1_sqr = w + x
        a2_sqr = w + y

        b1 = (1 - a1_sqr) ** 0.5
        b2 = (1 - a2_sqr) ** 0.5

        return Qubit(a1_sqr ** 0.5, b1), Qubit(a2_sqr ** 0.5, b2)
    elif length == 8:
        """
            Let a = a1 * a2 * a3, b = a1 * a2 * b3,
                c = a1 * b2 * a3, d = a1 * b2 * b3,
                e = b1 * a2 * a3, f = b1 * a2 * b3,
                g = b1 * b2 * a3, h = b1 * b2 * b3,
            Map f(x) = |x|^2 to each of the variables a, b, c, d, e, f, g, h
            We see that:
                a + b = |a1 * a2 * a3|^2 + |a1 * a2 * b3|^2
                = |a1 * a2|^2 (|a3|^2 + |b3|^2)
                = |a1 * a2|^2
            Similarly,
                c + d = |a1 * b2|^2
                e + f = |b1 * a2|^2
                a + c = |a1 * a3|^2
                e + g = |b1 * a3|^2
            Adding,
                a + b + c + d = |a1|^2
                a + b + e + f = |a2|^2
                a + c + e + g = |a3|^2
            From this,
                |b1| = sqrt( 1 - |a1|^2 ),
                |b2| = sqrt( 1 - |a2|^2 ),
                |b3| = sqet( 1 - |a3|^2 )
        """
        a, b, c, d, e, f, g, h = list(map(transform, unpack(*matrix)))

        alpha_a = (a + b + c + d) ** 0.5
        alpha_b = (a + b + e + f) ** 0.5
        alpha_c = (a + c + e + g) ** 0.5

        beta_a = (1 - (alpha_a ** 2)) ** 0.5
        beta_b = (1 - (alpha_b ** 2)) ** 0.5
        beta_c = (1 - (alpha_c ** 2)) ** 0.5

        return Qubit(alpha_a, beta_a), Qubit(alpha_b, beta_b), Qubit(alpha_c, beta_c)
    else:
        raise Exception("Unsupported operation.")

a, b, c, d = Qubit(0, 1), Qubit(0, 1), Qubit(0, 1), Qubit(0, 1)

print(State(factor(apply_gate('CCNOT', tensor_product(a, b, c)))).measure(), sep='\n')  # TODO, make qubits with multiple digits (isnt this just a basis?)

# print(f"{a = }\n{b = }\n{d = }\n")
# a, b, d = factor(apply_gate('CCNOT', tensor_product(a, b, d)))

# print(f"{a = }\n{b = }\n{d = }")

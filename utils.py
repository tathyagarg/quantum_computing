import math
import numpy as np

root2 = math.sqrt(2)
inv_root2 = 1/root2


def tensor_product(a, b):
    if not isinstance(a, list) or not isinstance(b, list):
        not_lis, lis = (a, b) if isinstance(b, list) else (b, a)
        return [not_lis * i for i in lis]
    
    result = []
    for asub in a:
        result.extend(tensor_product(asub, b))
    
    return result

GATES = {
    'I': [[1, 0], [0, 1]],
    'X': [[0, 1], [1, 0]],
    'Y': [[0, -1j], [1j, 0]],
    'Z': [[1, 0], [0, -1]],
    'CNOT': [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    'S': [[1, 0], [0, 1j]],
    'H': [[inv_root2, inv_root2], [inv_root2, -inv_root2]],
    'SWAP': [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]],
    'CCNOT': [[1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0]]
}

def apply_gate(key, values):
    return np.dot(GATES[key], values)
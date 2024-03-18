import math

root2 = math.sqrt(2)
inv_root2 = 1/root2


def tensor_product(*args):
    if len(args) > 2:
        a, b = args[-2:]
        result = tensor_product(a, b)
        for arg in args[:-2]:
            result = tensor_product(arg, result)

        return result
    
    a, b = args
    a_targ = a if isinstance(a, list) else a.W
    b_targ = b if isinstance(b, list) else b.W

    result = []
    for asub in a_targ:
        asub = asub[0]
        for bsub in b_targ:
            bsub = bsub[0]
            result.append([asub*bsub])

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

def matmul(x: list[list[complex]], y: list[list[complex]]):
    x_height, y_height = len(x), len(y)
    y_width = len(y[0])
    res = [[0 for _ in range(y_width)] for _ in range(x_height)]

    for i in range(x_height):
        for j in range(y_width):
            for k in range(y_height):
                res[i][j] += x[i][k] * y[k][j]

    return res

def apply_gate(key, values):
    return matmul(GATES[key], values)
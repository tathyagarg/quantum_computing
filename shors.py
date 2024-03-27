import random
import math

def shors_algorithm(M):
    a = random.randint(2, M-1)  # a < M
    if euclids_algorithm(a, M) != 1:
        gcd = euclids_algorithm(a, M)
        return gcd, M//gcd
    
    n = random.randint(int(2 * math.log2(M)), int((2 * math.log2(M)) + 1))
    N = 2 ** n

    print(a, n, N)

def euclids_algorithm(a, b):
    """
        Finds gcd(a, b) using Euclid's Algorithm
    """
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a

def mod_finder():
    ...

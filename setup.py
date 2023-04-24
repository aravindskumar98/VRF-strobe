from utils import *
import math
import random
import sympy

def setup(n,t):
    p_dash = get_germain_prime(13) # TODO: change hardcoded value
    q_dash = get_germain_prime(18)
    p = 2*p_dash + 1
    q = 2*q_dash + 1
    N = p*q
    phi = 4*p_dash*q_dash
    # randomly sample a prime s from the range [n+1, min(p_dash, q_dash)-1]
    s = sympy.randprime(n+1, min(p_dash, q_dash)-1)

    try:
        assert(s > n)
        assert(s < min(p_dash, q_dash))
        assert(phi % s != 0)
    except AssertionError:
        print("s is not valid")
        return None
    
    v = sympy.mod_inverse(math.factorial(n)*s, phi//4)
    a_coeff = [sympy.randprime(1, N) for _ in range(t-1)] # TODO: this has to be made a secret?

    return N, phi, s, a_coeff


def gen(n_fact, N):
    seed = random.randint(1, N)
    n_fact_sq = n_fact**2
    x_0 = pow(seed, n_fact_sq, N)
    return x_0
import sympy

def get_germain_prime(bits):
    # Set the range of values to search for a Germain prime
    start = 2**(bits-1)
    end = 2**bits

    # Iterate through the range of values and check if each is a Germain prime
    for n in range(start, end):
        p = 2*n + 1
        if sympy.isprime(p) and sympy.isprime(2*p + 1):
            print("The Germain prime is:", p)
            break
    return p

def get_s(n, p_dash, q_dash, phi):
    # Calculate the value of s
    s = n+1
    for s in range(4*n, min(p_dash, q_dash)):
        if (p_dash > s > n) and (q_dash > s > n) and (phi % s != 0):
            break
    return s


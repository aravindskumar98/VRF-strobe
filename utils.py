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

def lagrange_basis_polynomial(i, x, selected_indices, n_fact = 1):
    out = n_fact # This prevents floating point errors
    for j in selected_indices:
        if j != i:
            out *= (x - j)
            out //=(i - j)
    return out




# Dynamically generated functions will be added here



def count_up_to(n):
    '''Returns a list of prime numbers less than n.
    Raises TypeError for non-integer inputs.'''
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n <= 2:
        return []
    sieve = [True] * n
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]


if __name__ == "__main__":
    pass

if __name__ == "__main__":
    pass

"""
Python implementation of the RSA encryption algorithm.

The RSA algorithm is a public-key encryption algorithm that is based on the
difficulty of factoring large integers.

"""

import time
from math import sqrt

_memorization_prime: dict[int, bool] = {0: True, 1: True, 2: True, 3: True, 5: True, 7: True}
"""The dictionary that stores the prime numbers. 
This is used to speed up the process of finding the prime factors of a number."""


def divisible_by_357(x: int) -> bool:
    """Check if a number is divisible by 3, 5, or 7.

    Args:
        x (int): The number to check if it is divisible by 3, 5, or 7.

    Returns:
        If the number is divisible by 3, 5, or 7.
    """
    return x % 3 != 0 and x % 5 != 0 and x % 7 != 0


def is_prime(number: int) -> bool:
    """Check if a number is prime. Stores result in a dictionary to speed up the process.

    Args:
        number (unsigned long long): The number to check if it is prime.

    Returns:
        A zero of a one, representing a boolean
    """
    if number % 2 == 0:
        return number == 2

    if number in _memorization_prime:
        return _memorization_prime[number]

    if number % 3 == 0 or number % 5 == 0 or number % 7 == 0:
        _memorization_prime[number] = False
        return False

    for i in filter(divisible_by_357, range(11, int(sqrt(number)) + 1, 2)):
        if number % i == 0:
            _memorization_prime[number] = False
            return False

    _memorization_prime[number] = True
    return True


def find_prime_factors(number):
    if number <= 2 or is_prime(number):
        return {number}

    # When the number is a perfect square and the square root is a prime
    # The prime factors are the square root and the square root
    # square_root = sqrt(number)
    # if square_root.is_integer() and is_prime(int(square_root)):
    #     return {int(square_root)}

    fac = set()
    if number % 2 == 0:
        fac.add(2)
        number >>= 1
        while number % 2 == 0:
            number >>= 1

    g = 3
    while number != 1:
        if number % g == 0:
            fac.add(g)
            number //= g
            continue

        g += 2

    return fac


if __name__ == "__main__":
    user_input = 9

    s = time.perf_counter_ns()
    factors = find_prime_factors(user_input)
    e = time.perf_counter_ns()
    sec = (e - s) / 1_000_000_000

    print(f"The factors of {user_input} are {factors}.")
    print(f"The time taken to find the prime factors is {sec} seconds.")


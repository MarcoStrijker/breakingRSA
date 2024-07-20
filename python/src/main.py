"""
Python implementation of the prime factorization algorithm.

This implementation uses memorization to store the prime numbers that have been found.
This is used to speed up the process of finding the prime factors of a number.

The algorithm is as follows:
1. If the number is less than or equal to 2, return the number.
2. If the number is a prime number, return the number.
3. If the number is divisible by 2, add 2 to the factors and divide the number by 2.
4. Find the prime factors of the number by iterating from 3 to the square root of the number.
5. If the number is divisible by the current number, add the number to the factors and divide the number by
   the current number.
6. If the number is not divisible by the current number, increment the current number by 2.
7. Return the factors.

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

    if number <= 2 and number in _memorization_prime:
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
    user_input = 39452342

    s = time.perf_counter_ns()
    factors = find_prime_factors(user_input)
    e = time.perf_counter_ns()
    sec = (e - s) / 1_000_000_000

    print(f"The factors of {user_input} are {factors}.")
    print(f"The time taken to find the prime factors is {sec} seconds.")


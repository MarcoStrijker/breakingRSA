# cython: language_level=3str, boundscheck=False, wraparound=False, nonecheck=False, infer_types=False, profile=False, cdivision=False

"""
Cython implementation of the RSA encryption algorithm.

The RSA algorithm is a public-key encryption algorithm that is based on the
difficulty of factoring large integers.

"""

import time
from math import gcd

from libc.math cimport sqrt

cdef dict _memorization_prime = {}
"""The dictionary that stores the prime numbers.
This is used to speed up the process of finding the prime factors of a number."""


cpdef bint is_prime(unsigned long long number):
    """Check if a number is prime. Stores result in a dictionary to speed up the process.

    Args:
        number (unsigned long long): The number to check if it is prime.

    Returns:
        A zero of a one, representing a boolean
    """

    if number in _memorization_prime:
        return _memorization_prime[number]

    # Perform check after lookup since most evaluations will be
    # for numbers higher than 1
    if number < 2:
        return 0

    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            _memorization_prime[number] = 0
            return 0

    _memorization_prime[number] = 1
    return 1


cdef unsigned long long make_guess(unsigned long long number, unsigned long long guess):
    """Make a guess to determine the factors of a number.

    Args:
        number (unsigned long long): The number for which the factors should be found.
        guess (unsigned long long): The guess for the factors.

    Returns:
        A guess for the factors of the number.

    """
    while gcd(number, guess) != 1:
        guess += 1
    return guess


cdef unsigned long long calculate_exponent(unsigned long long guess):
    """Calculate the exponent for the factors of a number.

    Args:
        guess (unsigned long long): The guess for the factors.

    Returns:
        The exponent for the factors of the number.

    """
    cdef unsigned long long r = 2
    cdef unsigned long long g = guess ** r

    while g <= 1 and r % 2 == 0:
        r += 2
        g = guess ** r

    return r


cdef tuple find_factors(unsigned long long number, unsigned long long guess, unsigned long long exponent):
    """Find the factors for a number. the output is always a prime.

    Args:
        number (unsigned long long): The number for which the factors should be found.
        guess (unsigned long long): The guess for the factors.
        exponent (unsigned long long): The exponent for the factors.

    Returns:
        The factors of the number.

    Raises:
        ZeroDivisionError: If the number is 0.
        OverflowError: If the number is too large.
    """
    cdef unsigned long long nom = pow(guess, exponent // 2, number) + 1
    cdef unsigned long long den = number
    cdef unsigned long long outcome = gcd(nom, den)

    while (outcome == number
           or outcome == 1
           or not is_prime(number // outcome)):
        nom, den = den, nom % den
        outcome = gcd(nom, den)

    return number // outcome, number // (number // outcome)


cpdef shor(unsigned long long number):
    """ Finding the prime factors of a number. For example, the prime factors of 15 are 3 and 5.
    This is for breaking the RSA encryption algorithm.

    Args:
        number (unsigned long long): The number for which the prime factors should be found.

    Returns:
        The prime factors of the number.
    """

    # Only factors can be found for values higher than 2
    # When the number itself is a prime, we just return the number and 1
    if number < 2 or is_prime(number):
        return {number}

    # If the number is even, the prime factors are 2 and the prime factors of the other number
    if number % 2 == 0:
        return {2, *shor(number // 2)}

    # Staring with a guess of 3
    cdef unsigned long long g = 3

    while True:
        g = make_guess(number, g)
        r = calculate_exponent(g)

        # This is in a try-except block because the pow function can raise
        # a ZeroDivisionError or OverflowError. This means that it is not
        # possible to find the prime factors for the given number.
        # And this will restart the process with a new guess.
        try:
            f1, f2 = find_factors(number, g, r)
        except (ZeroDivisionError, OverflowError):
            g += 1
            continue

        # When the second factor is 1, the first factor is the prime factor
        # The guess was not correct, restart loop with another guess
        if f1 == 1:
            g += 1
            continue

        # When the second factor is a prime
        # We can return the two prime factors
        if is_prime(f2):
            return {f1, f2}

        # When the second factor is not a prime
        # Recursively find the prime factors of the other number
        # We return the set of the unique primes
        return {f1, *shor(f2)}


if __name__ == "__main__":
    user_input = int(input("Enter a number: "))
    s = time.perf_counter_ns()
    factors = shor(user_input)
    e = time.perf_counter_ns()
    sec = (e - s) / 1_000_000_000

    print(f"The factors of {user_input} are {factors}.")
    print(f"The time taken to find the prime factors is {sec} seconds.")

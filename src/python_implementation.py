"""
Python implementation of the RSA encryption algorithm.

The RSA algorithm is a public-key encryption algorithm that is based on the
difficulty of factoring large integers.

"""

import time
import math


_memorization_prime = {}
"""The dictionary that stores the prime numbers. 
This is used to speed up the process of finding the prime factors of a number."""


def is_prime(number: int) -> int:
    """Check if a number is prime. Stores result in a dictionary to speed up the process.

    Args:
        number (int): The number to check if it is prime.

    Returns:
        A zero of a one, representing a boolean
    """

    # Lookup if the number is previously marked as prime/not prime
    if number in _memorization_prime:
        return _memorization_prime[number]

    if number < 2:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            _memorization_prime[number] = 0
            return 0

    _memorization_prime[number] = 1
    return 1


def make_guess(number: int, guess: int) -> int:
    """Make a guess to determine the factors of a number.

    Args:
        number (int): The number for which the factors should be found.
        guess (int): The guess for the factors.

    Returns:
        A guess for the factors of the number.

    """
    while math.gcd(number, guess) != 1:
        guess += 1

    return guess


def calculate_exponent(number: int, guess: int) -> int:
    """Calculate the exponent for the factors of a number.

    Args:
        number (int): The number for which the factors should be found.
        guess (int): The guess for the factors.

    Returns:
        The exponent for the factors of the number.

    """
    r = 2
    g = pow(guess, r, 1 if number < 100 else number)
    while g == 1 and r % 2 == 0:
        r += 2
        g = pow(guess, r, number)

    return r


def find_factors(number: int, guess: int, exponent: int) -> int:
    """Find the factors for a number. the output is always a prime.

    Args:
        number (int): The number for which the factors should be found.
        guess (int): The guess for the factors.
        exponent (int): The exponent for the factors.

    Returns:
        The factors of the number.

    Raises:
        ZeroDivisionError: If the number is 0.
        OverflowError: If the number is too large.
    """

    nom = pow(guess, exponent // 2, number) + 1
    den = number

    outcome = math.gcd(nom, den)

    while (outcome == number
           or outcome == 1
           or not is_prime(number // outcome)):
        nom, den = den, nom % den
        outcome = math.gcd(nom, den)

    return number // outcome


def shor(number: int) -> set[int]:
    """ Finding the prime factors of a number. For example, the prime factors of 15 are 3 and 5.
    This is for breaking the RSA encryption algorithm.

    Args:
        number (int): The number for which the prime factors should be found.

    Returns:
        The prime factors of the number.
    """

    # Only factors can be found for values higher than 2
    if number < 2:
        return {number}

    # When the number itself is a prime, we just return the number and 1
    if is_prime(number):
        return {number}

    # If the number is even, the prime factors are 2 and the prime factors of the other number
    if number % 2 == 0:
        result = {2}
        result.update(shor(number // 2))
        return result

    # Staring with a guess of 3
    g = 3

    # Start the loop to find the prime factors
    while True:
        # if g > number:
        #     return {number}

        g = make_guess(number, g)
        r = calculate_exponent(number, g)

        # This is in a try-except block because the pow function can raise
        # a ZeroDivisionError or OverflowError. This means that it is not
        # possible to find the prime factors for the given number.
        # And this will restart the process with a new guess.
        try:
            f = find_factors(number, g, r)
        except (ZeroDivisionError, OverflowError):
            g += 1
            continue

        # When the second factor is zero
        # The guess was not correct, restart loop with another guess
        if f == 1:
            g += 1
            continue

        # When the second factor is a prime
        # We can return the two prime factors
        if is_prime(number // f):
            return {f, number // f}

        # When the second factor is not a prime
        # Recursively find the prime factors of the other number
        # We return the set of the unique primes
        result = {f}
        result.update(shor(number // f))
        return result


if __name__ == "__main__":
    user_input = int(input("Enter a number: "))
    s = time.perf_counter_ns()
    factors = shor(user_input)
    e = time.perf_counter_ns()
    sec = (e - s) / 1_000_000_000

    print(f"The factors of {user_input} are {factors}.")
    print(f"The time taken to find the prime factors is {sec} seconds.")

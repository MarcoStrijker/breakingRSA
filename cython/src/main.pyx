# cython: language_level=3, boundscheck=False, wraparound=False, nonecheck=False

from libc.math cimport sqrt
from math import gcd
import time

cdef dict _memorization_prime = {}

cdef bint is_prime(unsigned long long number):
    if number in _memorization_prime:
        return _memorization_prime[number]

    if number < 2:
        return 0

    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            _memorization_prime[number] = 0
            return 0

    _memorization_prime[number] = 1
    return 1


cdef unsigned long long make_guess(unsigned long long number, unsigned long long guess):
    while gcd(number, guess) != 1:
        guess += 1
    return guess


cdef unsigned long long calculate_exponent(unsigned long long number, unsigned long long guess):
    cdef unsigned long long r = 2
    cdef unsigned long long g = pow(guess, r, 1 if number < 100 else number)

    while g == 1 and r % 2 == 0:
        r += 2
        g = pow(guess, r, number)

    return r


cdef unsigned long long find_factors(unsigned long long number, unsigned long long guess, unsigned long long exponent):
    cdef unsigned long long nom = pow(guess, exponent // 2, number) + 1
    cdef unsigned long long den = number
    cdef unsigned long long outcome = gcd(nom, den)

    while (outcome == number or outcome == 1 or not is_prime(number // outcome)):
        nom, den = den, nom % den
        outcome = gcd(nom, den)

    return number // outcome


cpdef shor(unsigned long long number):
    if number < 2:
        return {number}
    if is_prime(number):
        return {number}
    if number % 2 == 0:
        result = {2, *shor(number // 2)}
    cdef unsigned long long g = 3
    while True:
        g = make_guess(number, g)
        r = calculate_exponent(number, g)
        try:
            f = find_factors(number, g, r)
        except (ZeroDivisionError, OverflowError):
            g += 1
            continue
        if f == 1:
            g += 1
            continue
        if is_prime(number // f):
            return {f, number // f}

        return {f, *shor(number // f)}


if __name__ == "__main__":
    user_input = int(input("Enter a number: "))
    s = time.perf_counter_ns()
    factors = shor(user_input)
    e = time.perf_counter_ns()
    sec = (e - s) / 1_000_000_000
    print(f"The factors of {user_input} are {factors}.")
    print(f"The time taken to find the prime factors is {sec} seconds.")

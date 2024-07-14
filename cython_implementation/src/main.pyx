# cython: language_level=3str, binding=False, boundscheck=False, wraparound=False, initializedcheck=False, nonecheck=False, infer_types=False, profile=False, cdivision=False, type_version_tag=False, unraisable_tracebacks=False
# distutils: language=c++
"""
Cython implementation of the RSA encryption algorithm.

The RSA algorithm is a public-key encryption algorithm that is based on the
difficulty of factoring large integers.

"""

from libc.math cimport sqrt

from libcpp.unordered_map cimport unordered_map


cdef unordered_map[unsigned long long, bint] _memorization_prime
"""The dictionary that stores the prime numbers"""


_memorization_prime[0] = 0
_memorization_prime[1] = 0


cdef bint check(unsigned long long x):
    """Check if a number is divisible by 3, 5, or 7.

    Args:
        x (int): The number to check if it is divisible by 3, 5, or 7.

    Returns:
        If the number is divisible by 3, 5, or 7.
    """
    return x % 3 != 0 and x % 5 != 0 and x % 7 != 0


cpdef bint is_prime(unsigned long long number):
    """Check if a number is prime. Stores result in a dictionary to speed up the process.

    Args:
        number (unsigned long long): The number to check if it is prime.

    Returns:
        A zero of a one, representing a boolean
    """
    cdef int i

    if number % 2 == 0:
        return number == 2

    if _memorization_prime.find(number) != _memorization_prime.end():
        return _memorization_prime[number]

    if number % 3 == 0 or number % 5 == 0 or number % 7 == 0:
        _memorization_prime[number] = False
        return False

    for i in filter(check, range(11, int(sqrt(number)) + 1, 2)):
        if number % i == 0:
            _memorization_prime[number] = 0
            return 0

    _memorization_prime[number] = 1
    return 1


cpdef set find_prime_factors(unsigned long long number):
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

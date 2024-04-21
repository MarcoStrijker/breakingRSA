""" Stub file for the Mypyc implementation of the Shor's algorithm.

Functions:
    is_prime: Check if a number is prime.
    shor: Finding the prime factors of a number.

"""

def is_prime(number: int) -> int:
    """Check if a number is prime. Stores result in a dictionary to speed up the process.

    Args:
        number (unsigned long long): The number to check if it is prime.

    Returns:
        A zero of a one, representing a boolean
    """


def shor(number: int) -> set[int]:
    """ Finding the prime factors of a number. For example, the prime factors of 15 are 3 and 5.
    This is for breaking the RSA encryption algorithm.

    Args:
        number (unsigned long long): The number for which the prime factors should be found.

    Returns:
        The prime factors of the number.
    """

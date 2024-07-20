""" Stub file for the Rust implementation of the Prime factor algorithm."""


from ctypes import c_ulonglong

# Define aliases for the types used in the module
u64 = c_ulonglong


def find_prime_factors(number: u64) -> set[u64]:
    """ Finding the prime factors of a number. For example, the prime factors of 15 are 3 and 5.
    This is for breaking the RSA encryption algorithm.

    Args:
        number (unsigned long long): The number for which the prime factors should be found.

    Returns:
        The prime factors of the number.
    """

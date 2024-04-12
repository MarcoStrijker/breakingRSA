"""This module acts as wrapper for the c code. It handles the conversion of the pointer to
a Python set and the freeing of the memory."""

from ctypes import CDLL, POINTER, Structure, c_uint64, c_uint8


class Set(Structure):
    """ A set of integers. Represents the output of the internal
    c shor function."""
    _fields_ = [
        ("items", POINTER(c_uint64)),
        ("size", c_uint8),
        ("capacity", c_uint8)
    ]


def shor(number: int) -> set[int]:
    """Wrapper function for the C code

    Args:
        number (int): the number fo which the prime factors should be found

    Returns:
        The prime factors (set[int])
    """

    # Solve the prime factors and get the resutls
    ptr = c_lib.shor(number)
    results = set(ptr.contents.items[i] for i in range(ptr.contents.size))

    # free the memory
    c_lib.free_set(ptr)

    return results


# Import DLL
c_lib = CDLL(r".\c_implementation\src\main.dll", mode=1, use_errno=True, use_last_error=True)

# Define return and arg types of DLL
c_lib.shor.restype = POINTER(Set)
c_lib.shor.argtypes = [c_uint64]

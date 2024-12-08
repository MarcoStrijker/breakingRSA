"""Unit tests for the Shor's algorithm implementations.

This module contains unit tests for the Shor's algorithm implementations.
It tests the correctness of the implementations by comparing the results of the
implementations with the predefined results.

"""
import unittest

from python.src.main import shor as python_implementation
from cython_implementation.src.main import shor as cython_implementation
from rust.src.main import shor as rust_implementation
from c_implementation.src.main import find_prime_factors as c_implementation


# Define outcomes for certain inputs
RESULTS = {
    1: {1},
    2: {2},
    3: {3},
    4: {2},
    5: {5},
    6: {2, 3},
    7: {7},
    8: {2},
    9: {3},
    10: {2, 5},
    11: {11},
    12: {2, 3},
    13: {13},
    14: {2, 7},
    15: {3, 5},
    16: {2},
    17: {17},
    18: {2, 3},
    19: {19},
    20: {2, 5},
    21: {3, 7},
    22: {2, 11},
    23: {23},
    24: {2, 3},
    25: {5},
}


# Run the tests
class ShorImplementations(unittest.TestCase):
    """Tests all Shor algorithms of different implementations."""

    def test_python(self):
        for number, factors in RESULTS.items():
            self.assertEqual(python_implementation(number), factors)

    def test_cython(self):
        for number, factors in RESULTS.items():
            self.assertEqual(cython_implementation(number), factors)

    def test_c(self):
        for number, factors in RESULTS.items():
            self.assertEqual(c_implementation(number), factors)


if __name__ == "__main__":
    unittest.main()

""" Speed test for the Shor's algorithm implementations.

This module tests the speed of the Shor's algorithm implementations. It tests the speed of the
implementations by running the implementations for a range of numbers and measuring the time it
takes to run the implementations.

"""

import time

from python.src.main import shor as python_implementation
from cython_implementation.src.main import shor as cython_implementation
from rust.src.main import shor as rust_implementation


# The numbers to test the implementations with
NUMBERS = [
    2 ** n - 1 for n in range(1, 32)
]


def warm_up(*args):
    """Run 357 through all functions to warm up the call overhead.

    Args:
        *args: The functions to run.
    """
    for function in args:
        function(357)


def test_suites(**kwargs):
    """Run all suites once and print the time it took to run each suite.

    Args:
        **kwargs: The functions to test. Keys are names, values are the functions.
    """

    # Run all suites once
    warm_up(*kwargs.values())

    times = {}
    for name, function in kwargs.items():
        print(f"Testing {name} implementation...")
        s = time.perf_counter_ns()

        # Run the function for all numbers
        for n in NUMBERS:
            function(n)

        e = time.perf_counter_ns()
        sec = (e - s) / 1_000_000_000

        # Ensure name always have a length of 10
        name = name.rjust(7)
        times[name] = sec

    # Print the results
    print()
    for name, sec in times.items():
        print(f"{name}: {sec:.9f} seconds.")


if __name__ == "__main__":
    test_suites(
        python=python_implementation,
        cython=cython_implementation,
        rust=rust_implementation,
    )

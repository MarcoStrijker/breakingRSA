import os
import sys
import warnings

import argparse


class StoutCollector:
    """ If setup is called with --verbose, this collector will collect the stdout"""
    def __enter__(self):
        """"Disables the stdout (if verbose is off)"""
        if args.verbose:
            sys.stdout = None
            sys.stderr = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Resets the output"""
        sys.stdout = sys.__stdout__
        sys.stdout = sys.__stderr__


def compile_code(implementation: str, command: str) -> None:
    """Compiles the code

    Args:
        implementation (str): The name of the implementation
        command (str): The command to run

    """
    # Compile the Cython code
    with StoutCollector():
        exit_code = os.system(command)

    if exit_code != 0 and verbose:
        warnings.warn(f"{implementation} failed to compile the code. "
                      "Please check the output for more information.")
    elif exit_code != 0:
        warnings.warn(f"{implementation} failed to compile the code. "
                      "Please run with --verbose to see the output.")


# Define the commands per implementation
commands = {
    "Cython": r"cythonize --3str --no-docstrings -i cython_implementation\src\*.pyx",
    "Rust": r"cd rust && maturin develop --release --strip",
}


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument(
        "--verbose",
        help="Show the internal messages of the compilers",
        action="store_true",
        default=False
    )
    args = argparse.parse_args()

    # Run all commands
    for impl, com in commands.items():
        compile_code(impl, com)


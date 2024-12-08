""" This script compiles the code. It compiles the Cython, Rust and C code, but can be extended to
compile other code as well. The script will raise a warning if the code fails to compile.


The script can be run with the following command:
    python setup.py [--verbose]

The --verbose flag will show the output of the compilers. If the code fails to compile,
the script will raise a warning.

Classes:
    StoutCollector: A context manager to collect the stdout.

Functions:
    compile_code: Compiles the code.
    run: Runs the script and compiles the code.

"""

import os
import sys
import warnings

import argparse

__error = False
__compiled = False


# Define the commands per implementation
COMMANDS = {
    "Cython": rf"cythonize --3str --no-docstrings -i cython_implementation\src\*.pyx",
    "Rust": r"cd rust && maturin develop --release --strip --skip-install --bindings pyo3",
    "C": r'gcc -shared -o2 c_implementation\src\main.pyd -I"C:\Users\xdmar\AppData\Local\Programs\Python\Python313\include" -L"C:\Users\xdmar\AppData\Local\Programs\Python\Python313\libs" c_implementation\src\main.c -lpython313"',
    "Mypyc": r"cd mypyc_implementation\src && mypyc ..\..\python\src\main.py",
}


# Set the PYO3_PYTHON environment variable
# this enables maturin to find Python
os.environ["PYO3_PYTHON"] = sys.executable

# Set the working directory to the root of the project
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def compile_code(implementation: str, command: str) -> None:
    """Compiles the code

    Args:
        implementation (str): The name of the implementation
        command (str): The command to run

    """

    if not args.verbose:
        command += " > NUL 2>&1"

    # Compile the Cython code
    exit_code = os.system(command)

    if exit_code == 0:
        return

    msg = f"{implementation} failed to compile the code."
    msg += "Please check the output for more information." if args.verbose else "Please setup.py run with --verbose"
    warnings.warn(msg)
    global __error
    __error = True


def run(verbose: bool = False) -> None:
    """Runs the script and compiles the code."""
    global __compiled, args

    if __compiled:
        return

    # Set the verbose flag
    args.verbose = verbose

    # Run all commands
    for impl, com in COMMANDS.items():
        compile_code(impl, com)

    if __error:
        raise SystemExit("Failed to compile the code")

    __compiled = True


# Parse the verbose argument
argparse = argparse.ArgumentParser()
argparse.add_argument(
    "--verbose",
    help="Show the internal messages of the compilers",
    action="store_true",
    default=False
)
args = argparse.parse_args()

if __name__ == "__main__":
    run(args.verbose)

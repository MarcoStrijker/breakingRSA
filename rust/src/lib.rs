/// Rust implementation of the prime factorization algorithm.
///
/// This implementation uses memorization to store the prime numbers that have been found.
/// This is used to speed up the process of finding the prime factors of a number.
///
/// The algorithms is being wrapped by a Python module to be used in Python.
///
/// The algorithm is as follows:
/// 1. If the number is less than or equal to 2, return the number.
/// 2. If the number is a prime number, return the number.
/// 3. If the number is divisible by 2, add 2 to the factors and divide the number by 2.
/// 4. Find the prime factors of the number by iterating from 3 to the square root of the number.
/// 5. If the number is divisible by the current number, add the number to the factors and divide the number by
///    the current number.
/// 6. If the number is not divisible by the current number, increment the current number by 2.
/// 7. Return the factors.


use std::collections::HashSet;

use num_integer::Roots;
use memoize::memoize;

use pyo3::prelude::*;


/// Check if a number is prime. Uses memoization.
///
/// # Arguments
/// * `number` - The number to check if it is prime (u64)
///
/// # Returns
/// * `bool` - True if the number is prime, False otherwise
///
#[memoize]
fn is_prime(number: u64) -> bool {
    if number % 2 == 0 || number == 1 {
        // When the number is dividable by two, it is never
        // a prime, except when it is two
        return number == 2
    }

    if number == 3 || number == 5 || number == 7 {
        return true
    }

    if number % 3 == 0 || number % 5 == 0 || number % 7 == 0 {
        return false
    }

    for i in (11..=number.sqrt())
        .step_by(2)
        .filter(|x| x % 3 != 0 || x % 5 != 0 || x % 7 != 0)
    {
        if number % i == 0 {
            return false;
        }
    }

    return true;
}


/// Find the prime factors of a number
/// This function is a bit more optimized than the one in the
/// Python file. It uses memoization to check if a number is prime
/// and it uses a different algorithm to find the prime factors.
/// The algorithm is based on the fact that every number can be
/// represented as a product of prime numbers.
///
/// # Arguments
/// * `number` - The number to find the prime factors for
///
/// # Returns
/// * `HashSet<u64>` - The prime factors of the number
///
/// # Note
/// This function is being wrapped by the `find_prime_factors` function
/// to be used in Python.
///
pub fn _find_prime_factors(mut number: u64) -> HashSet<u64> {
    let mut g: u64 = 3;
    let mut factors: HashSet<u64> = HashSet::<u64>::new();

    // If the number itself is a prime, just return the number
    if number <= 2 || is_prime(number) {
        return HashSet::<u64>::from([number]);
    }

    // If divisible by two, we first will divide the number
    // by two until this is not possible anymore
    // we use bit shifting to divide by two
    // this should be faster than the normal division
    if number % 2 == 0 {
        // 2 only has to be inserted once
        factors.insert(2);

        // keep dividing until number is
        // not fully divisible by two
        number >>= 1;
        while number % 2 == 0 {
            number >>= 1;
        }
    }

    // Start main loop
    while number != 1 {
        // Add factor while
        if number % g == 0 {
            factors.insert(g);
            number /= g;
            continue
        }

        // If number is prime, it should end the loop and add the
        // number as the last factor
        if is_prime(number) {
            factors.insert(number);
            break
        }

        // Increment by two, because g should only
        // primes, this increases the chance
        g += 2;
    }

    return factors
}



/// Wrap the find_prime_factors
///
/// # Arguments
/// * `number` - The number to find the prime factors for
///
/// # Returns
/// * `PyResult<HashSet<u64>>` - The prime factors of the number
#[pyfunction]
fn find_prime_factors(_py: Python, number: u64) -> PyResult<HashSet<u64>> {
    Ok(_find_prime_factors(number))
}


/// Create a Python module with the functions
///
/// # Arguments
/// * `m` - The Python module
///
/// # Returns
/// * `PyResult<()>` - The Python module with the functions
#[pymodule]
#[pyo3(name = "main")]
fn module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_prime_factors, m)?)?;
    Ok(())
}

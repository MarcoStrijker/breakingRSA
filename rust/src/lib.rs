use std::collections::hash_map::HashMap;
use std::collections::HashSet;

use lazy_static::lazy_static;

use pyo3::prelude::*;

extern crate num_integer;

// This is a global variable that will be used to store the memorization of the prime numbers
lazy_static! {
    static ref MEMORIZATION_PRIME: std::sync::Mutex<HashMap<u64, bool>> =
        std::sync::Mutex::new(HashMap::<u64, bool>::new());
}

fn create_hashset_from_single_number(number: u64) -> HashSet<u64> {
    // Create a hashset from a single number
    //
    // # Arguments
    // * `number` - The number to create the hashset from
    //
    // # Returns
    // * `HashSet` - A hashset with the number
    return HashSet::<u64>::from([number]);
}

fn create_hashset_from_numbers(num1: u64, num2: u64) -> HashSet<u64> {
    // Create a hashset from two numbers
    //
    // # Arguments
    // * `num1` - The first number
    // * `num2` - The second number
    //
    // # Returns
    // * `HashSet` - A hashset with the numbers
    return HashSet::<u64>::from([num1, num2]);
}

fn extend_hashset_with_number(mut set: HashSet<u64>, number: u64) -> HashSet<u64> {
    // Extend the first hashset with the second hashset
    //
    // # Arguments
    // * `set` - The first hashset
    // * `number` - The number to extend the first hashset with
    //
    // # Returns
    // * `HashSet` - The first hashset extended with the second hashset
    set.insert(number);
    return set;
}

fn _is_prime(number: u64) -> bool {
    // Check if a number is prime
    //
    // # Arguments
    // * `number` - The number to check if it is prime (u64)
    //
    // # Returns
    // * `bool` - True if the number is prime, False otherwise

    if number < 2 {
        return false;
    }

    // If the number is already in the memorization, return the result
    if let Some(result) = MEMORIZATION_PRIME.lock().unwrap().get(&number) {
        return *result;
    }

    for i in 2..(num_integer::sqrt(number) + 1) {
        if number % i == 0 {
            MEMORIZATION_PRIME.lock().unwrap().insert(number, false);
            return false;
        }
    }

    MEMORIZATION_PRIME.lock().unwrap().insert(number, true);
    return true;
}

fn make_guess(number: u64, mut guess: u64) -> u64 {
    // Make a initial guess
    //
    // # Arguments
    // * `number` - The number to find the prime factors for
    // * `guess` - The initial guess
    //
    // # Returns
    // * `u64` - The initial guess
    loop {
        if num_integer::gcd(number, guess) == 1 {
            return guess;
        }
        guess += 1
    }
}

fn mod_exp(base: u64, exponent: u64, modulus: u64) -> Option<u64> {
    // Calculate the modular exponentiation
    //
    // # Arguments
    // * `base` - The base
    // * `exponent` - The exponent
    // * `modulus` - The modulus
    //
    // # Returns
    // * `Option<u64>` - The result of the modular exponentiation

    // If the modulus is less than or equal to 1, return None
    // This prevents a division by zero
    if modulus <= 1 {
        return None;
    }

    let mut result: u64 = 1;
    let mut base: u64 = base % modulus;
    let mut exponent: u64 = exponent;

    loop {
        if exponent == 0 {
            break;
        }

        if exponent % 2 == 1 {
            result = (result * base) % modulus;
        }

        exponent >>= 1;
        base = (base * base) % modulus;
    }

    return Some(result);
}

fn calculate_exponent(guess: u64) -> u64 {
    let mut r: u64 = 2;

    // Guess to the power of exponent
    let mut g: u64 = guess.pow(r.try_into().unwrap());
    // mod_exp(guess, r, if number < 100 {1} else {number}).unwrap_or_default();

    loop {
        if g > 1 || r % 2 != 0 {
            return r;
        }
        r += 2;
        g = guess.pow(r.try_into().unwrap());
    }
}

fn find_factors(number: u64, guess: u64, exponent: u64) -> Option<u64> {
    // Find the factors of a number
    //
    // # Arguments
    // * `number` - The number to find the factors for
    // * `guess` - The guess
    // * `exponent` - The exponent
    //
    // # Returns
    // * `Option<u64>` - The factors of the number
    let mut nom: u64 = mod_exp(guess, exponent / 2, number).unwrap_or_default() + 1;
    let mut den: u64 = number;
    let mut outcome: u64 = num_integer::gcd(nom, den);

    // Loop until the outcome is not the number or 1 and the outcome is a prime
    loop {
        if outcome != number && outcome != 1 && _is_prime(number / outcome) {
            return Some(number / outcome);
        }
        if den == 0 {
            return None;
        }
        (nom, den) = (den, nom % den);
        outcome = num_integer::gcd(nom, den);
    }
}

pub fn _shor(number: u64) -> HashSet<u64> {
    // Find the prime factors of a number
    //
    // # Arguments
    // * `number` - The number to find the prime factors for
    //
    // # Returns
    // * `HashSet` - The prime factors of the number

    // Only factors can be found for values higher than 2
    // When the number itself is a prime, we just return the number and 1
    if number < 2 || _is_prime(number) {
        return create_hashset_from_single_number(number);
    }

    // If the number is even, one of the prime factors is 2
    // plus the other prime factor of the number divided by 2
    // For this we recursively call the function with the number divided by 2
    if number % 2 == 0 {
        return extend_hashset_with_number(_shor(number / 2), 2);
    }

    // Starting guess process by defining the variables
    // for the guess, the exponent and the factors
    // Staring with a guess of 3
    let mut g: u64 = 3;
    let mut r: u64;
    let mut f: u64;

    loop {
        g = make_guess(number, g);
        r = calculate_exponent(g);
        f = find_factors(number, g, r).unwrap_or_default();

        // When the second factor is zero
        // The guess was not correct, restart loop with
        // current guess + 1
        if f <= 1 {
            g += 1;
            continue;
        }

        // When the second factor is a prime
        // We can return the two prime factors
        if _is_prime(number / f) {
            return create_hashset_from_numbers(f, number / f);
        }

        // When the second factor is not a prime
        // We recursively call the function with the second factor
        return extend_hashset_with_number(_shor(number / f), f);
    }
}

#[pyfunction]
fn shor(_py: Python, number: u64) -> PyResult<HashSet<u64>> {
    // Wrap the _shor function to be used in Python
    //
    // # Arguments
    // * `number` - The number to find the prime factors for
    //
    // # Returns
    // * `PyResult<HashSet<u64>>` - The prime factors of the number
    Ok(_shor(number))
}

#[pyfunction]
fn is_prime(_py: Python, number: u64) -> PyResult<bool> {
    // Wrap the _is_prime function to be used in Python
    //
    // # Arguments
    // * `number` - The number to check if it is prime
    //
    // # Returns
    // * `PyResult<bool>` - True if the number is prime, False otherwise
    Ok(_is_prime(number))
}

#[pymodule]
#[pyo3(name = "main")]
fn module(_py: Python, m: &PyModule) -> PyResult<()> {
    // Create a Python module with the functions
    //
    // # Arguments
    // * `m` - The Python module
    //
    // # Returns
    // * `PyResult<()>` - The Python module with the functions
    m.add_function(wrap_pyfunction!(shor, m)?)?;
    m.add_function(wrap_pyfunction!(is_prime, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn number_is_prime() {
        let number = 13;
        assert_eq!(_is_prime(number), true);
    }

    #[test]
    fn number_is_not_prime() {
        let number = 3233;
        assert_eq!(_is_prime(number), false);
    }

    #[test]
    fn test_make_guess() {
        let number = 15;
        let guess = 3;
        assert_eq!(make_guess(number, guess), 4);
    }

    #[test]
    fn test_pow_mod_new() {
        let base = 4;
        let exponent = 13;
        let modulus = 497;
        assert_eq!(mod_exp(base, exponent, modulus).unwrap(), 445);
    }

    #[test]
    fn test_calculate_exponent() {
        let guess = 4;
        assert_eq!(calculate_exponent(guess), 2);
    }

    #[test]
    fn test_get_single_filled_hashset() {
        let number = 13;
        let mut hashset: HashSet<u64> = HashSet::<u64>::new();
        hashset.insert(number);
        assert_eq!(create_hashset_from_single_number(number), hashset);
    }

    #[test]
    fn test_get_multi_filled_hashset() {
        let a: HashSet<u64> = HashSet::<u64>::from_iter([13]);
        assert_eq!(extend_hashset_with_number(a, 130), [13, 130].into());
    }

    #[test]
    fn test_find_factors() {
        let number = 15;
        let guess = 4;
        let exponent = 2;
        assert_eq!(find_factors(number, guess, exponent).unwrap(), 3);
    }

    #[test]
    fn test_shor() {
        let number = 77;
        let result: HashSet<u64> = [7, 11].into();
        assert_eq!(_shor(number), result);
    }
}

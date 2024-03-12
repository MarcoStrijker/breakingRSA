use std::time::Instant;
use std::collections::hash_map::{HashMap};
use std::collections::HashSet;

extern crate num_integer;


// static mut _memorization_prime: HashMap<u128, bool> = HashMap::<u128, bool>::new();


fn is_prime(number: u128) -> bool {

    // if _memorization_prime.contains_key(&number) {
    //     return *_memorization_prime.get(&number).unwrap();
    // }

    if number < 2 {
        return false
    }

    for i in 2..(num_integer::sqrt(number) + 1) {
        if number % i == 0 {
            // _memorization_prime.insert(number, false);
            return false;
        }
    }

    // _memorization_prime.insert(number, true);
    return true
}


fn make_guess(number: u128, mut guess: u128) -> u128 {
    loop {
        if num_integer::gcd(number, guess) != 1 {
            return guess
        }
        guess += 1
    }
}


fn pow_mod(base: u128, exponent: u128, modulus: u128) -> u128 {
    let mut result = 1;
    let mut power = base % modulus;

    for _ in 0..exponent {
        if exponent & 1 == 1 {
            result = (result * power) % modulus;
        }
        power = (power * power) % modulus;
    }

    return result
}



fn calculate_exponent(number: u128, guess: u128) -> u128 {
    let mut r: u128 = 2;


    let mut g: u128 = pow_mod(guess, r, if number < 100 {1} else {number});

    loop {
        if g == 1 && r % 2 == 0 {
            return r
        }

        r += 2;
        g = pow_mod(guess, r, number)
    }

}


fn find_factors(number: u128, guess: u128, exponent: u128) -> Option<u128> {
    let mut nom: u128 = pow_mod(guess, exponent / 2, number) + 1;
    let mut den: u128 = number;

    let mut outcome: u128 = num_integer::gcd(nom, den);

    loop {
        if outcome != number && outcome != 1 && is_prime(number / outcome) {
            return Some(number / outcome)
        }
        if den == 0 {
            return None
        }
        (nom, den) = (den, nom % den);
        outcome = num_integer::gcd(nom, den);
    }
}


fn get_single_filled_hashset(number: u128) -> HashSet<u128> {
    let mut hashset: HashSet<u128> = HashSet::<u128>::new();
    hashset.insert(number);
    return hashset;
}


fn mesh_two_hashsets(mut a: HashSet<u128>, b: HashSet<u128>) -> HashSet<u128> {
    a.extend(b);
    return a
}

fn shor(number: u128) -> HashSet<u128> {

    // Only factors can be found for values higher than 2
    // When the number itself is a prime, we just return the number and 1
    if number < 2 || is_prime(number) {
        return get_single_filled_hashset(number);
    }

    // If the number is even, the prime factors are 2 and the prime factors of the other number
    if number % 2 == 0 {
        return mesh_two_hashsets(
            get_single_filled_hashset(2),
            shor(number / 2)
        )
    }

    // Staring with a guess of 3
    let mut g: u128 = 3;

    let mut r: u128;
    let mut f: u128;

    loop {
        g = make_guess(number, g);
        r = calculate_exponent(number, g);
        f = find_factors(number, g, r).unwrap_or_default();

        // When the second factor is zero
        // The guess was not correct, restart loop with another guess
        if f <= 1 {
            g += 1;
            continue
        }

        // When the second factor is a prime
        // We can return the two prime factors
        if is_prime(number / f) {
            return mesh_two_hashsets(
                get_single_filled_hashset(f),
                get_single_filled_hashset(number / f)
            )
        }

        return mesh_two_hashsets(
            get_single_filled_hashset(f),
            shor(number / f)
        )
    }
}


fn main() {
    let user_input: u128 = 323333333333;

    let s = Instant::now();
    let set: HashSet<u128> = shor(user_input);
    let e = s.elapsed();
    let sec = e.as_secs() as f64 + e.subsec_nanos() as f64 * 1e-9;

    println!("{:?}", set);
    println!("The time taken to find the prime factors is {} seconds.", sec);
}

use std::collections::HashSet;
use std::time::Instant;

use shors_algorithm::find_prime_factors;

fn main() {

    let user_input: u128 = 41282366920938463463307431768211415;

    let s = Instant::now();
    let set: HashSet<u128> = find_prime_factors(user_input);
    let e = s.elapsed();
    let sec = e.as_secs() as f64 + e.subsec_nanos() as f64 * 1e-9;

    println!("{:?}", set);
    println!(
        "The time taken to find the prime factors is {} seconds.",
        sec
    );
}

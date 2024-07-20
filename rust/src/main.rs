use std::collections::HashSet;
use std::time::Instant;

use find_primes::_find_prime_factors;

fn main() {

    let user_input: u64 = 15;

    let s = Instant::now();
    let set: HashSet<u64> = _find_prime_factors(user_input);
    let e = s.elapsed();
    let sec = e.as_secs() as f64 + e.subsec_nanos() as f64 * 1e-9;

    println!("{:?}", set);
    println!(
        "The time taken to find the prime factors is {} seconds.",
        sec
    );
}

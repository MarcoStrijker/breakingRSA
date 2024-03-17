use std::collections::HashSet;
use std::time::Instant;

use shors_algorithm::_shor;

fn main() {
    let user_input: u64 = 92349678913456;

    let s = Instant::now();
    let set: HashSet<u64> = _shor(user_input);
    let e = s.elapsed();
    let sec = e.as_secs() as f64 + e.subsec_nanos() as f64 * 1e-9;

    println!("{:?}", set);
    println!(
        "The time taken to find the prime factors is {} seconds.",
        sec
    );
}

// Python implementation of the RSA encryption algorithm.
//
// The RSA algorithm is a public-key encryption algorithm that is based on the
// difficulty of factoring large integers.

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define u64 unsigned long long
#define u8 unsigned char
#define i8 char

typedef struct {
  u64* keys;
  i8* items;
  u8 size;
  u64 capacity;
} Dict;

Dict* create_dict() {
  // Create a dictionary.
  //
  // Args:
  //     capacity (unsigned long long): The capacity of the dictionary.
  //
  // Returns:
  //     Dict: The created dictionary.
  Dict* dict = malloc(sizeof(Dict));
  dict->keys = malloc(1000000 * sizeof(u64));
  dict->items = malloc(1000000 * sizeof(i8));
  dict->size = 0;
  dict->capacity = 1000000;

  return dict;
}

void add_to_dict(Dict* dict, u64 key, i8 item) {
  // Add an item to a dictionary.
  //
  // Args:
  //     dict (Dict): The dictionary to which the item should be added.
  //     key (unsigned long long): The key to add to the dictionary.
  //     item (unsigned char): The item to add to the dictionary.
  //
  // Returns:
  //     Dict: The dictionary with the added item.

  // Extend the dictionary if it is full with 1000 elements.
  if (dict->size == dict->capacity) {
    dict->capacity += 1000;
    dict->keys = realloc(dict->keys, dict->capacity * sizeof(u64));
    dict->items = realloc(dict->items, dict->capacity * sizeof(i8));
  }

  // Add the item to the dictionary.
  dict->keys[dict->size] = key;
  dict->items[dict->size] = item;
  dict->size += 1;
}

i8 get_from_dict(Dict* dict, u64 key) {
  // Get an item from a dictionary.
  //
  // Args:
  //     dict (Dict): The dictionary from which the item should be retrieved.
  //     key (unsigned long long): The key from which the item should be
  //     retrieved.
  //
  // Returns:
  //     unsigned char: The item from the dictionary.
  for (u64 i = 0; i < dict->size; i++) {
    if (dict->keys[i] == key) {
      return dict->items[i];
    }
  }

  return -1;
}

// Create set like structure
typedef struct {
  u64* items;
  u8 size;
  u8 capacity;
} Set;

Set* create_set(u64 capacity) {
  // Create a set.
  //
  // Args:
  //     capacity (unsigned long long): The capacity of the set.
  //
  // Returns:
  //     Set: The created set.
  Set* set = malloc(sizeof(Set));
  set->items = malloc(capacity * sizeof(u64));
  set->size = 0;
  set->capacity = capacity;

  return set;
}

void free_set(Set* set) {
  // Free the memory of a set.
  //
  // Args:
  //     set (Set): The set for which the memory should be freed.
  free(set->items);
  free(set);
}

void add_to_set(Set* set, u64 item) {
  // Add an item to a set.
  //
  // Args:
  //     set (Set): The set to which the item should be added.
  //     item (unsigned long long): The item to add to the set.

  // Extend the set if it is full.
  if (set->size == set->capacity) {
    set->capacity += 1;
    set->items = realloc(set->items, set->capacity * sizeof(u64));
  }

  // Check if the item is already in the set, if so, early return.
  for (u8 i = 0; i < set->size; i++) {
    if (set->items[i] == item) {
      return;
    }
  }

  // Add the item to the set.
  set->items[set->size] = item;
  set->size += 1;
}

Set* add_u64_to_set(Set* set, u64 item) {
  // Add an item to a set.
  //
  // Args:
  //     set (Set): The set to which the item should be added.
  //     item (unsigned long long): The item to add to the set.
  //
  // Returns:
  //     Set: The set with the added item.
  add_to_set(set, item);
  return set;
}

Set* initialize_set_with_single_item(u64 item) {
  // Initialize a set with a single item.
  //
  // Args:
  //     item (unsigned long long): The item to add to the set.
  //
  // Returns:
  //     Set: The initialized set.
  Set* set = create_set(1);
  add_to_set(set, item);

  return set;
}

Set* initialize_set_with_items(u64* items) {
  // Initialize a set with items.
  //
  // Args:
  //     items (unsigned long long): The items to add to the set.
  //     size (unsigned char): The size of the set.
  //
  // Returns:
  //     Set: The initialized set.
  Set* set = create_set(2);
  for (u8 i = 0; i < 2; i++) {
    add_to_set(set, items[i]);
  }

  return set;
}

Dict* memorization_prime;

i8 is_prime(u64 number) {
  // Check if a number is prime.
  //
  // Args:
  //     number (unsigned long long): The number to check.
  //
  // Returns:
  //     unsigned long long: 1 if the number is prime, 0 otherwise.

  i8 mem = get_from_dict(memorization_prime, number);

  // If mem is negative one, it means the number is not in the dictionary
  if (mem != -1) {
    return mem;
  }

  for (u64 i = 2; i <= sqrt(number); i++) {
    if (number % i == 0) {
      add_to_dict(memorization_prime, number, 0);
      return 0;
    }
  }

  add_to_dict(memorization_prime, number, 1);
  return 1;
}

u64 gcd(u64 a, u64 b) {
  // Calculate the greatest common divisor of two numbers.
  //
  // Args:
  //     a (unsigned long long): The first number.
  //     b (unsigned long long): The second number.
  //
  // Returns:
  //     unsigned long long: The greatest common divisor of the two numbers.

  while (b != 0) {
    a %= b;
    a ^= b;
    b ^= a;
    a ^= b;
  }

  return a;
}

u64 mod_exp(u64 base, u64 exponent, u64 modulus) {
  // Calculate the modular exponentiation of a number.
  //
  // Args:
  //     base (unsigned long long): The base.
  //     exponent (unsigned long long): The exponent.
  //     modulus (unsigned long long): The modulus.
  //
  // Returns:
  //     unsigned long long: The modular exponentiation of the number.
  if (modulus <= 1) {
    return 0;
  }

  u64 result = 1;

  while (exponent > 0) {
    if (exponent % 2 == 1) {
      result = (result * base) % modulus;
    }

    exponent = exponent >> 1;
    base = (base * base) % modulus;
  }

  return result;
}

u64 make_guess(u64 number, u64 guess) {
  // Make a guess to determine the factors of a number.
  //
  // Args:
  //     number (int): The number for which the factors should be found.
  //     guess (int): The guess for the factors.
  //
  // Returns:
  //     A guess for the factors of the number.
  while (gcd(number, guess) != 1) {
    guess += 1;
  }

  return guess;
}

u64 calculate_exponent(u64 guess) {
  // Calculate the exponent for the factors of a number.
  //
  // Args:
  //     guess (int): The guess for the factors of the number.
  //
  // Returns:
  //     The exponent for the factors of the number.
  u64 r = 2;
  u64 g = pow(guess, r);

  while (g <= 1 && r % 2 == 0) {
    r += 2;
    g = pow(guess, r);
  }

  return r;
}

u64* find_factors(u64 number, u64 guess, u64 exponent) {
  // Find the factors of a number. The output is always a prime.
  //
  // Args:
  //     number (int): The number for which the factors should be found.
  //     guess (int): The guess for the factors.
  //     exponent (int): The exponent for the factors.
  //

  u64 temp;
  // Free memory for array of the size of two u64
  u64* factors = malloc(2 * sizeof(u64));

  u64 nom = mod_exp(guess, exponent >> 1, number) + 1;
  u64 den = number;
  u64 outcome = gcd(nom, den);

  if (outcome == number || outcome == 1) {
    factors[0] = 0;
    return factors;
  }

  while (!is_prime(number / outcome)) {
    // Early exit if the denominator is 0
    // This prevents a division by zero error
    if (den == 0) {
      factors[0] = 0;
      return factors;
    }
    temp = den;
    den = nom % den;
    nom = temp;
    outcome = gcd(nom, den);
  }

  factors[0] = number / outcome;
  factors[1] = number / factors[0];

  return factors;
}

Set* shor(u64 number) {
  // Finding the prime factors of a number. For example, the prime factors of 15
  // are 3 and 5. This is for breaking the RSA encryption algorithm.

  // Args:
  //     number (usigned long long): The number for which the prime factors
  //     should be found.

  // Returns:
  //     The prime factors of the number.

  // Only factors can be found for values higher than 2
  // When the number itself is a prime, we just return the number and 1
  if (memorization_prime == NULL) {
    memorization_prime = create_dict();
    add_to_dict(memorization_prime, 0, 0);
    add_to_dict(memorization_prime, 1, 0);
  }

  if (number < 2 || is_prime(number)) {
    return initialize_set_with_single_item(number);
  }
  // If the number is even, the prime factors are 2 and the prime factors of the
  // other number
  if (number % 2 == 0) {
    return add_u64_to_set(shor(number >> 1), 2);
  }

  // Staring with a guess of 3
  u64* factors;
  u64 g = 3;
  u64 r = calculate_exponent(g);

  // Start the loop to find the prime factors
  while (1) {
    g = make_guess(number, g);
    r = calculate_exponent(g);

    factors = find_factors(number, g, r);

    if (factors[0] <= 1) {
      free(factors);
      g += 1;
      continue;
    }

    if (is_prime(factors[1])) {
      return initialize_set_with_items(factors);
    }

    return add_u64_to_set(shor(factors[1]), factors[0]);
  }
}


int main() {
  memorization_prime = create_dict();
  add_to_dict(memorization_prime, 0, 0);
  add_to_dict(memorization_prime, 1, 0);

  // Add way user can input number at runtime
  // The user can input a number for which the prime factors should be found.
  // This will be used as input for the shor function.
  // printf("Please enter a number: \n");

  const u64 number = 92349678913456;

  // scanf("%d", &number);
  time_t start = clock();
  Set* a = shor(number);

  time_t end = clock();

  printf("The prime factors of %llu are: \n", number);
  for (u8 i = 0; i < a->size; i++) {
    printf("%llu\n ", a->items[i]);
  }
  printf("\n Time taken: %f\n", (double)(end - start) / CLOCKS_PER_SEC);
  return 0;
}

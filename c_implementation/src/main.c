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

  if (number % 2 == 0 | number % 3 == 0 || number % 5 == 0 || number % 7 == 0) {
    return 0;
  }

  for (u64 i = 11; i <= sqrt(number); i+=2) {
    if (i % 3 == 0 || i % 5 == 0 || i % 7 == 0) {
      continue;
    }

    if (number % i == 0) {
      add_to_dict(memorization_prime, number, 0);
      return 0;
    }
  }

  add_to_dict(memorization_prime, number, 1);
  return 1;
}

Set* find_prime_factors(u64 number) {
  // Find the prime factors of a number.
  //
  // Args:
  //     number (unsigned long long): The number for which the prime factors
  //     should be found.
  //
  // Returns:
  //     Set: The prime factors of the number.

  // We need to create the memorization_prime dictionary if it does not exist
  if (memorization_prime == NULL) {
    memorization_prime = create_dict();
    add_to_dict(memorization_prime, 0, 0);
    add_to_dict(memorization_prime, 1, 0);
    add_to_dict(memorization_prime, 2, 1);
    add_to_dict(memorization_prime, 3, 1);
    add_to_dict(memorization_prime, 5, 1);
    add_to_dict(memorization_prime, 7, 1);
  }

  if (number < 2 || is_prime(number)) {
    return initialize_set_with_single_item(number);
  }

  Set* factors = create_set(5);

  if (number % 2 == 0) {
    factors = add_u64_to_set(factors, 2);

    number >>= 1;
    while (number % 2 == 0) {
      number >>= 1;
    }
  }

  for (u64 g = 3; number != 1; g += 2) {
    if (number % g == 0) {
      factors = add_u64_to_set(factors, g);
      number /= g;
      continue;
    } 
  
    if (is_prime(number)) {
      factors = add_u64_to_set(factors, number);
      break;
    }
  }

  return factors;
}

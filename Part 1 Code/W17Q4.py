from itertools import permutations
from hashlib import sha1

hashed_gesture = "91077079768edba10ac0c93b7108bc639d778d67"

pattern_elements = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


def check_hash(pattern: str) -> str:
    return sha1(pattern.encode("utf-8")).hexdigest()


def guess_pattern() -> int:
    perm_list = list(permutations(pattern_elements, len(pattern_elements)))
    perm_list_len = len(perm_list)
    for k in range(perm_list_len):
        word = "".join(perm_list[k])
        if hashed_gesture == check_hash(word):
            print("Done: ", word)
            return 0
    print("No match found")
    return 1


def main():
    return guess_pattern()


if __name__ == '__main__':
    exit(main())

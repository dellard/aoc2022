#!/usr/bin/env python3

import sys

# brute-force has a certain elegance

def find_no_repeats_prefix(text, prefix_len):

    for i in range(len(text) - prefix_len):
        characters = set(text[i:i + prefix_len])
        if len(characters) == prefix_len:
            return i + prefix_len

    # oops?
    return -1


line = sys.stdin.readline().strip()
print('part 1: %d' % find_no_repeats_prefix(line, 4))
print('part 2: %d' % find_no_repeats_prefix(line, 14))

#!/usr/bin/env python3

"""
Advent of Code 2022, day 6
"""

import sys

def find_no_repeats_prefix(text, prefix_len):
    """
    Use brute-force approach to finding the
    first sequence of prefix_len that contains
    no repeated characters
    """

    for i in range(len(text) - prefix_len):
        characters = set(text[i:i + prefix_len])
        if len(characters) == prefix_len:
            return i + prefix_len

    # oops?
    return -1


def main():
    line = sys.stdin.readline().strip()
    print('part 1: %d' % find_no_repeats_prefix(line, 4))
    print('part 2: %d' % find_no_repeats_prefix(line, 14))


if __name__ == '__main__':
    main()

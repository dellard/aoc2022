#!/usr/bin/env python3

"""
Advent of Code 2022, day 3
"""

import sys


def find_overlap(compartment0, compartment1):

    items0 = set(compartment0)
    items1 = set(compartment1)

    return list(items0 & items1)


def find_priority(char):

    if ord(r'a') <= char <= ord(r'z'):
        return 1 + char - ord(r'a')
    else:
        return 27 + char - ord(r'A')


def find_badge_prio(lines):
    common = find_overlap(find_overlap(lines[0], lines[1]), lines[2])
    return find_priority(ord(common[0]))


def main():
    total_priority0 = 0
    total_priority1 = 0

    curr_lines = []

    for line in sys.stdin:
        line = line.strip()

        curr_lines.append(line)

        halflen = int(len(line) / 2)

        half0 = line[:halflen]
        half1 = line[halflen:]

        overlap = find_overlap(half0, half1)

        total_priority0 += find_priority(ord(list(overlap)[0]))

        # each time we've read three un-badged lines,
        # it's time to figure out their badge and then
        # reset and start again
        #
        if len(curr_lines) == 3:
            total_priority1 += find_badge_prio(curr_lines)
            curr_lines = []

    print('part 1: %d' % total_priority0)
    print('part 2: %d' % total_priority1)


if __name__ == '__main__':
    main()

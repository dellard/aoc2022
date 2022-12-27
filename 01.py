#!/usr/bin/env python3

"""
Advent of Code 2022, day 1
"""

import sys


def main():
    """
    Advent of Code 2022, day 1
    """

    totals = []

    current_sum = 0

    for line in sys.stdin:

        line = line.strip()
        if not line:
            totals.append(current_sum)
            current_sum = 0
        else:
            current_sum += int(line)

    # deal with the last group, which ends at the end
    # of the input, not a blank line
    #
    if current_sum > 0:
        totals.append(current_sum)

    totals = sorted(totals)
    print('part 1: %d' % totals[-1])
    print('part 2: %d' % sum(totals[-3:]))


if __name__ == '__main__':
    main()

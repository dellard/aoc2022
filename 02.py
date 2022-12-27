#!/usr/bin/env python3

"""
Advent of Code 2022, day 2
"""

import sys


def main():
    """
    Advent of Code 2022, day 2
    """

    # for part 1
    score1 = 0
    outcomes1 = {
            'A X' : 1 + 3,
            'B X' : 1 + 0,
            'C X' : 1 + 6,
            'A Y' : 2 + 6,
            'B Y' : 2 + 3,
            'C Y' : 2 + 0,
            'A Z' : 3 + 0,
            'B Z' : 3 + 6,
            'C Z' : 3 + 3,
    }

    # for part 2
    score2 = 0
    outcomes2 = {
            'A X' : 3 + 0,
            'B X' : 1 + 0,
            'C X' : 2 + 0,
            'A Y' : 1 + 3,
            'B Y' : 2 + 3,
            'C Y' : 3 + 3,
            'A Z' : 2 + 6,
            'B Z' : 3 + 6,
            'C Z' : 1 + 6,
    }

    for line in sys.stdin:
        line = line.strip()

        score1 += outcomes1[line]
        score2 += outcomes2[line]

    print('part 1: %d' % score1)
    print('part 2: %d' % score2)


if __name__ == '__main__':
    main()

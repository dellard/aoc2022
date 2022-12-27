#!/usr/bin/env python3

"""
Advent of Code 2022, day 4
"""

import sys


def is_within(point0, point1):

    return (point0[0] >= point1[0] and point0[0] <= point1[1] and
            point0[1] >= point1[0] and point0[1] <= point1[1])


def does_overlap(point0, point1):

    # Feelin' lazy
    #
    if point0[0] >= point1[0] and point0[0] <= point1[1]:
        result = True
    elif point0[1] >= point1[0] and point0[1] <= point1[1]:
        result = True
    elif point1[0] >= point0[0] and point1[0] <= point0[1]:
        result = True
    elif point1[1] >= point0[0] and point1[1] <= point0[1]:
        result = True
    else:
        result = False

    return result


def main():
    count0 = 0
    count1 = 0

    for line in sys.stdin:

        # This method of parsing the input is more
        # cautious than necessary for AoC
        #
        r0_s, r1_s = line.strip().split(',')

        r00_s, r01_s = r0_s.split('-')
        r10_s, r11_s = r1_s.split('-')

        point0 = int(r00_s), int(r01_s)
        point1 = int(r10_s), int(r11_s)

        if is_within(point0, point1) or is_within(point1, point0):
            count0 += 1

        if does_overlap(point0, point1):
            count1 += 1

    print('part 1: %d' % count0)
    print('part 2: %d' % count1)


if __name__ == '__main__':
    main()


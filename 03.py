#!/usr/bin/env python3

import sys

def find_overlap(compartment0, compartment1):

    s0 = set([c for c in compartment0])
    s1 = set([c for c in compartment1])

    return list(s0 & s1)


def find_priority(char):

    if char >= ord(r'a') and char <= ord(r'z'):
        return 1 + char - ord(r'a')
    elif char >= ord(r'A') and char <= ord(r'Z'):
        return 27 + char - ord(r'A')
    else:
        print('oops 2 [%s]' % char)
        sys.exit(1)


def find_badge_prio(lines):
    common = find_overlap(find_overlap(lines[0], lines[1]), lines[2])

    if len(common) != 1:
        print('ooops 4')
        sys.exit(1)

    return find_priority(ord(common[0]))


total_priority0 = 0
total_priority1 = 0

curr_lines = list()

for line in sys.stdin:
    line = line.strip()

    curr_lines.append(line)

    halflen = int(len(line) / 2)

    if halflen * 2 != len(line):
        print('ooops 1')
        sys.exit(1)

    h0 = line[:halflen]
    h1 = line[halflen:]

    overlap = find_overlap(h0, h1)
    if len(overlap) != 1:
        print('oops 3')
        sys.exit(1)

    total_priority0 += find_priority(ord(list(overlap)[0]))

    # each time we've read three un-badged lines,
    # it's time to figure out their badge and then
    # reset and start again
    #
    if len(curr_lines) == 3:
        total_priority1 += find_badge_prio(curr_lines)
        curr_lines = list()

print('case 0: total priority %d' % total_priority0)
print('case 1: total priority %d' % total_priority1)


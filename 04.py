#!/usr/bin/env python3

import sys

def is_within(p0, p1):

    return (p0[0] >= p1[0] and p0[0] <= p1[1] and
            p0[1] >= p1[0] and p0[1] <= p1[1])


def does_overlap(p0, p1):

    # Feelin' lazy
    #
    if p0[0] >= p1[0] and p0[0] <= p1[1]:
        result = True
    elif p0[1] >= p1[0] and p0[1] <= p1[1]:
        result = True
    elif p1[0] >= p0[0] and p1[0] <= p0[1]:
        result = True
    elif p1[1] >= p0[0] and p1[1] <= p0[1]:
        result = True
    else:
        result = False

    # print('%s  %s / %s' % (result, p0, p1))
    return result


count0 = 0
count1 = 0

for line in sys.stdin:
    r0_s, r1_s = line.strip().split(',')

    r00_s, r01_s = r0_s.split('-')
    r10_s, r11_s = r1_s.split('-')

    p0 = int(r00_s), int(r01_s)
    p1 = int(r10_s), int(r11_s)

    if is_within(p0, p1) or is_within(p1, p0):
        count0 += 1

    if does_overlap(p0, p1):
        count1 += 1

print('test0: total %d' % count0)
print('test1: total %d' % count1)


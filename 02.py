#!/usr/bin/env python3

import sys

OUTCOMES1 = {
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

OUTCOMES2 = {
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

SCORE1 = 0
SCORE2 = 0

for line in sys.stdin:
    line = line.strip()

    if line not in OUTCOMES1:
        print('oops1 %s' % line)
    if line not in OUTCOMES2:
        print('oops2 %s' % line)


    SCORE1 += OUTCOMES1[line]
    SCORE2 += OUTCOMES2[line]

print('task 1: total score %d' % SCORE1)
print('task 2: total score %d' % SCORE2)




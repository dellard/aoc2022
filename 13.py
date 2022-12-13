#!/usr/bin/env python3

import sys


def reader():

    lines = [l.strip() for l in sys.stdin.readlines()]

    # Here's where the security hole is...
    # But the first rule of AoC is that you don't need
    # to check the input...
    pairs = [(eval(lines[3 * i]), eval(lines[3 * i + 1]))
             for i in range(1 + len(lines) // 3)]

    # print(pairs)

    return pairs


RIGHT = 1
WRONG = 0
CONTINUE = 2

def check_pair(left, right):

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 'RIGHT'
        elif left == right:
            return 'CONTINUE'
        else:
            return 'WRONG'

    elif isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            res = check_pair(left[i], right[i])
            if res in ['RIGHT', 'WRONG']:
                return res

        if len(left) < len(right):
            return 'RIGHT'
        elif len(left) > len(right):
            return 'WRONG'
        else:
            return 'CONTINUE'

    elif isinstance(left, int):
        return check_pair([left], right)
    elif isinstance(right, int):
        return check_pair(left, [right])
    else:
        print('oops')


def compute_sum(pairs):

    sum = 0
    for i in range(len(pairs)):
        if check_pair(pairs[i][0], pairs[i][1]) == 'RIGHT':
            sum += (i + 1)

    return sum


def main():
    pairs = reader()

    #for left, right in pairs:
    #    print('GOT %s %s -> %s' %
    #          (str(left), str(right), check_pair(left, right)))

    print('part 1: %d' % compute_sum(pairs))


if __name__ == '__main__':
    main()

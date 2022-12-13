#!/usr/bin/env python3

"""
Advent of Code 2022, day 13
"""

import sys


def reader():

    lines = [l.strip() for l in sys.stdin.readlines()]

    # Here's where the gaping security hole is...
    # You should NEVER use eval on unchecked input.
    #
    # But the first rule of AoC is that the input is
    # always properly formed, unless specified otherwise,
    # so just do the simple thing
    #
    pairs = [(eval(lines[3 * i]), eval(lines[3 * i + 1]))
             for i in range(1 + len(lines) // 3)]

    return pairs


# Whether the order of two pairs is right, wrong, or
# they're "equivalent".  These values are chosen so
# we can use them later when sorting the messages
# (in part 2)

RIGHT = -1
WRONG = 1
CONTINUE = 0


def check_pair(left, right):

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return RIGHT
        elif left == right:
            return CONTINUE
        else:
            return WRONG

    elif isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            res = check_pair(left[i], right[i])
            if res in [RIGHT, WRONG]:
                return res

        if len(left) < len(right):
            return RIGHT
        elif len(left) > len(right):
            return WRONG
        else:
            # Not sure if this is exactly right, but
            # fortunately it never seems to come up
            # in the test or eval data that a pair
            # of messages end in this state.  If that
            # ever becomes a problem, wrap this
            # function in a helper that tests the
            # total comparison, and if it's CONTINUE,
            # return RIGHT, because if two messages
            # are identical, then they're in the
            # right order, I would think, but the
            # spec doesn't say AFAIK.
            #
            return CONTINUE

    elif isinstance(left, int):
        return check_pair([left], right)
    elif isinstance(right, int):
        return check_pair(left, [right])
    else:
        # crash and burn.  This shouldn't happen.
        print('oops')


def compute_sum(pairs):

    good_count = 0
    for i in range(len(pairs)):
        if check_pair(pairs[i][0], pairs[i][1]) == RIGHT:
            good_count += (i + 1)

    return good_count

# cmp_to_key is copied verbatim from the python3 docs.
#
# Python3 sort is fundamentally broken, so workaround
# to compare anything complicated.
# It's either that, or make a class for the messages, and
# that's a nah.
#
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def find_divisions(pairs):

    # This flattening shouldn't be done in this function,
    # but hey, it's AoC
    #
    all_msgs = []
    for left, right in pairs:
        all_msgs.append(left)
        all_msgs.append(right)

    # Add the divider packets
    #
    divider0 = [[2]]
    divider1 = [[6]]

    all_msgs.append(divider0)
    all_msgs.append(divider1)

    # deal with Python3's silly sort
    def cmp_msgs(msg1, msg2):
        return check_pair(msg1, msg2)
    python3_bodge = cmp_to_key(cmp_msgs)

    all_msgs.sort(key=python3_bodge)

    # indices are 1-based, not 0-based
    d0_ind = 1 + all_msgs.index(divider0)
    d1_ind = 1 + all_msgs.index(divider1)

    return d0_ind * d1_ind


def main():
    pairs = reader()

    print('part 1: %d' % compute_sum(pairs))
    print('part 2: %d' % find_divisions(pairs))


if __name__ == '__main__':
    main()

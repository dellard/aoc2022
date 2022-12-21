#!/usr/bin/env python3

import copy
import re
import sys

# maybe we'll need this?
# sys.setrecursionlimit(100000)


def reader():

    monkeys = {}

    for line in sys.stdin:
        tokens = line.strip().split()
        tokens[0] = re.sub(':', '', tokens[0])

        if len(tokens) == 2:
            monkeys[tokens[0]] = int(tokens[1])
        else:
            monkeys[tokens[0]] = tuple(tokens[1:4])

    return monkeys


def monkey_eval(monkeys, root_name):

    root = monkeys[root_name]

    if isinstance(root, int):
        return root

    left_name, operator, right_name = monkeys[root_name]
    left_val = monkey_eval(monkeys, left_name)
    right_val = monkey_eval(monkeys, right_name)

    if operator == '+':
        val = left_val + right_val
    elif operator == '-':
        val = left_val - right_val
    elif operator == '*':
        val = left_val * right_val
    elif operator == '/':
        val = left_val // right_val
    else:
        print('OOPS op %s %s %s' % (left_name, operator, right_name))

    return val

def part2(monkeys, root_name):

    # We're going to be destructive, so always mount
    # a scratch monkey
    #
    monkeys = copy.deepcopy(monkeys)

    # assumption: the root node isn't the human.
    # Then we would be godlike and could name
    # any value.
    #
    root = monkeys[root_name]

    # Replace the 'human' node with 'HUMAN', and then
    # try to eval the left and right, using the modified
    # evaluator that recognizes the 'HUMAN' value.
    # One of these will evaluate to a human, and the
    # other will evaluate to 'HUMAN'.
    #
    # Important note: while the evaluation is going on,
    # the monkeys are being rewritten to simplify the
    # resulting expression by substituting every subtree
    # that can be replaced with a constant value with
    # that constant value.  So if we had an "monkey-tree"
    # that looked like ((2 + 2) * ((3 * 4) + HUMAN))
    # the subexpressions 2 + 2 and 3 * 4 would be
    # replaced with their values, leaving just
    # (4 * (12 + HUMAN))
    #
    monkeys['humn'] = 'HUMAN'
    left_val = monkey_eval2(monkeys, root[0])
    right_val = monkey_eval2(monkeys, root[2])

    if left_val == 'HUMAN':
        value, unknown = right_val, root[0]
    else:
        value, unknown = left_val, root[2]

    candidate = solver(monkeys, unknown, value)

    # Now we have a candidate value.
    #
    # HOWEVER, the solution is not necessarily unique,
    # because of rounding in integer division.  The
    # problem description says that you need to supply
    # "the" answer, but what do we do when there is
    # more than one?  Could we return any of them?
    # Or just the smallest?
    #
    # Let's check the candidate by plugging it back
    # into the monkey tree and seeing what value it
    # evaluates to.
    #
    monkeys['humn'] = candidate
    check = monkey_eval(monkeys, unknown)
    if check == value:
        return candidate
    else:
        print('UH-OH.  Not a unique solution?')
        return -1


def expr_to_str(monkeys, root_name):
    """
    To help visualize the expression
    """

    root = monkeys[root_name]
    if isinstance(root, str):
        return root
    elif isinstance(root, int):
        return '%d' % root
    else:
        return '(%s %s %s)' % (
                expr_to_str(monkeys, root[0]),
                root[1],
                expr_to_str(monkeys, root[2]))


def solver(monkeys, root_name, value):

    root = monkeys[root_name]
    if isinstance(root, str):
        return value
    elif isinstance(root, int):
        print('UNEXPECTED')
        return root

    # At this point, the tree is a single chain,
    # so we either go left or right, but never both

    left = monkeys[root[0]]
    operator = root[1]
    right = monkeys[root[2]]

    if operator == '+':
        if isinstance(left, int):
            value -= left
            return solver(monkeys, root[2], value)
        else:
            value -= right
            return solver(monkeys, root[0], value)
    elif operator == '-':
        if isinstance(left, int):
            value = -(value - left)
            return solver(monkeys, root[2], value)
        else:
            value += right
            return solver(monkeys, root[0], value)
    elif operator == '*':
        if isinstance(left, int):
            value //= left
            return solver(monkeys, root[2], value)
        else:
            value //= right
            return solver(monkeys, root[0], value)
    elif operator == '/':
        if isinstance(right, int):
            value *= right
            return solver(monkeys, root[0], value)
        else:
            print('WARNING: this could lead to problems?')
            value = left / value
            return solver(monkeys, root[2], value)
    else:
        print('OOPS op %s' % operator)
        return value


def monkey_eval2(monkeys, root_name):

    # Like monkey_eval, but simplifies the monkey tree
    # as it goes, turning constant sub-trees into ints.
    #
    # Returns 'HUMAN' for any tree containing a variable
    # (the human-supplied input)

    root = monkeys[root_name]

    if isinstance(root, str):
        return 'HUMAN'
    elif isinstance(root, int):
        return root

    left_name, operator, right_name = monkeys[root_name]
    left_val = monkey_eval2(monkeys, left_name)
    right_val = monkey_eval2(monkeys, right_name)

    if left_val == 'HUMAN' or right_val == 'HUMAN':
        return 'HUMAN'

    if operator == '+':
        val = left_val + right_val
    elif operator == '-':
        val = left_val - right_val
    elif operator == '*':
        val = left_val * right_val
    elif operator == '/':
        val = left_val // right_val
    else:
        print('OOPS op %s %s %s' % (left_name, operator, right_name))

    monkeys[root_name] = val
    return val


def main():

    monkeys = reader()

    # Note: we could just use monkey_eval2 instead of
    # monkey_eval, as long as we make sure to make a
    # copy of the tree first.  We don't really *need*
    # to have two functions that are so similar.
    #
    # (or whether monkey_eval2 is destructive could also
    # be a parameter, or it could construct a new tree
    # of its own, or...)

    print('part 1: %d' % monkey_eval(monkeys, 'root'))
    print('part 2: %d' % part2(monkeys, 'root'))


if __name__ == '__main__':
    main()

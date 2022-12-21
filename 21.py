#!/usr/bin/env python3

import re
import sys

# maybe we'll need this?
# sys.setrecursionlimit(100000)


def reader():

    monkeys = {}
    deps = {}
    constants = []
    operators = []

    for line in sys.stdin:

        tokens = line.strip().split()
        tokens[0] = re.sub(':', '', tokens[0])

        if len(tokens) == 2:
            monkeys[tokens[0]] = int(tokens[1])
        else:
            monkeys[tokens[0]] = tuple(tokens[1:4])

    return monkeys


def monkey_eval(monkeys, root_name):

    # fill in any known constants

    root = monkeys[root_name]

    if isinstance(root, int):
        return root

    left_name, operator, right_name = monkeys[root_name]
    left_val = monkey_eval(monkeys, left_name)
    right_val = monkey_eval(monkeys, right_name)

    if operator == '+':
        return left_val + right_val
    elif operator == '-':
        return left_val - right_val
    elif operator == '*':
        return left_val * right_val
    elif operator == '/':
        return left_val // right_val
    else:
        print('OOPS op %s %s %s' % (left_name, operator, right_name))


def main():

    monkeys = reader()
    # print(monkeys)

    print('part 1: %d' % monkey_eval(monkeys, 'root'))

if __name__ == '__main__':
    main()

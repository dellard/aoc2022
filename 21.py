#!/usr/bin/env python3

import copy
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

    # We're going to be destructive
    #
    monkeys = copy.deepcopy(monkeys)

    monkeys['humn'] = 'HUMAN'

    root = monkeys[root_name]

    left_val = monkey_eval2(monkeys, root[0])
    right_val = monkey_eval2(monkeys, root[2])

    if left_val == 'HUMAN':
        value = right_val
        unknown = root[0]
    else:
        value = left_val
        unknown = root[2]

    print('left ', left_val, ' right ', right_val)

    #for i in range(299, 305, 1):
    #    monkeys['humn'] = i
    #    print('eval at %d is %d' % (i, monkey_eval(monkeys, unknown)))

    monkeys['humn'] = 'HUMAN'
    #print('expr ', expr_to_str(monkeys, unknown))

    #for i in range(0, 10000, 1000):
    #    monkeys['humn'] = i
    #    print('eval at %d is %d' % (i, monkey_eval(monkeys, root[0])))

    candidate = solver(monkeys, unknown, value)

    monkeys['humn'] = candidate
    print('eval at %d is %d' % (candidate, monkey_eval(monkeys, unknown)))
    print('value is %d' % value)



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

    print('value ', value)

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
        elif isinstance(right, int):
            value -= right
            return solver(monkeys, root[0], value)
    elif operator == '-':
        if isinstance(left, int):
            value = -(value - left)
            return solver(monkeys, root[2], value)
        elif isinstance(right, int):
            value = value + right
            return solver(monkeys, root[0], value)
    elif operator == '*':
        if isinstance(left, int):
            value = value // left
            return solver(monkeys, root[2], value)
        elif isinstance(right, int):
            value = value // right
            return solver(monkeys, root[0], value)
    elif operator == '/':
        if isinstance(right, int):
            value = value * right
            return solver(monkeys, root[0], value)
        elif isinstance(left, int):
            print('WHAT?')
            value = left / value
            return solver(monkeys, root[2], value)
    else:
        print('OOPS op %s %s %s' % (left_name, operator, right_name))
        return value



def monkey_eval2(monkeys, root_name):

    # fill in any known constants

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
    # print(monkeys)

    print('part 1: %d' % monkey_eval(monkeys, 'root'))

    part2(monkeys, 'root')
    # print('part 2: %d' % monkey_eval2(monkeys, 'root'))

if __name__ == '__main__':
    main()

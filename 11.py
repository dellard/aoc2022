#!/usr/bin/env python3

import re
import sys


class Monkey():

    def __init__(
            self, name, worries, operator, operand,
            test, action_t, action_f):

        self.name = name
        self.worries = worries[:]
        self.operator = operator
        self.operand = operand
        self.test = test
        self.action_t = action_t
        self.action_f = action_f

        self.inspections = 0

    def new_worry(self, old_worry):

        if self.operand[0] == 'const':
            operand = self.operand[1]
        else:
            operand = old_worry

        if self.operator == '*':
            return old_worry * operand
        else:
            return old_worry + operand

    def do_turn(self, monkeys):

        to_inspect = len(self.worries)

        while self.worries:
            worry = self.worries.pop(0)
            new_worry = self.new_worry(worry)
            bored_worry = int(new_worry / 3)

            if (bored_worry % self.test) == 0:
                print('is div so %d' % self.action_t)
                dest = self.action_t
            else:
                print('is NOT so %d' % self.action_f)
                dest = self.action_f

            print('worry %d -> %d %d [%d] tossed to %d' %
                  (worry, new_worry, bored_worry, self.test, dest))

            monkeys[dest].worries.append(bored_worry)

        self.inspections += to_inspect

    def print_worries(self):
        print('Monkey %d: %s' %
              (self.name, ', '.join([str(x) for x in self.worries])))

    def __repr__(self):

        # FIXME: complete this
        return '%s %s, (%s, %s), %d' % (
                self.name, self.worries, self.operator, self.operand,
                self.test)



def reader():

    monkeys = []
    monkey_num = 0

    lines = [line.strip() for line in sys.stdin.readlines()]

    while lines:
        tokens = lines[:6]

        # terrifyingly little sanity checking
        name = int(re.findall(r'\d+', tokens[0])[0])

        worries = [int(worry) for worry in re.findall(r'\d+', tokens[1])]

        operation_toks = tokens[2].split()
        if operation_toks[:4] != ['Operation:', 'new', '=', 'old']:
            print('oops 0')

        # TODO: split this by whether the operand is 'old' or an int
        #
        operator = operation_toks[4]
        if operator not in ['*', '+']:
            print('oops operator %s' % operator)
            sys.exit(1)

        if operation_toks[5] == 'old':
            op_mode = 'old'
            op_val = 0
        else:
            op_mode = 'const'
            op_val = int(operation_toks[5])

        operand = op_mode, op_val

        test_toks = tokens[3].split()
        if test_toks[:3] != ['Test:', 'divisible', 'by']:
            print('oops 1')
        test = int(test_toks[3])

        action_t = int(re.findall(r'\d+', tokens[4])[0])
        action_f = int(re.findall(r'\d+', tokens[5])[0])

        # We assume that we never monkeys never throw
        # things to themselves
        #
        if name in [action_t, action_f]:
            print('GOTTA DEAL with loops')
            sys.exit(1)

        # We assume that monkeys are named sequentially,
        # starting at 0 (the name of each monkey is the
        # index at which it appears in the definition file)
        #
        if name != monkey_num:
            print('GOTTA DEAL with ooo names')
            sys.exit(1)

        lines = lines[7:]
        monkey_num += 1

        monkeys.append(
                Monkey(name, worries, operator, operand,
                       test, action_t, action_f))

    return monkeys


def do_round(monkeys):

    for monkey in monkeys:
        monkey.do_turn(monkeys)

    for monkey in monkeys:
        print(monkey)


def main():

    monkeys = reader()

    for monkey in monkeys:
        print(monkey)
        monkey.print_worries()

    for i in range(20):
        do_round(monkeys)

    print('== == == ==')
    inspections = sorted([m.inspections for m in monkeys])
    business = inspections[-1] * inspections[-2]
    print('part 1: %d' % business)



if __name__ == '__main__':
    main()


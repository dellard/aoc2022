#!/usr/bin/env python3

import copy
import re
import sys


class Monkey():

    def __init__(
            self, name, worries, operator, operand,
            modulus, action_t, action_f):

        self.name = name
        self.worries = worries[:]
        self.operator = operator
        self.operand = operand
        self.modulus = modulus
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

    def do_turn(self, monkeys, worry_factor=3, ring_modulus=0):

        to_inspect = len(self.worries)

        while self.worries:
            worry = self.worries.pop(0)
            new_worry = self.new_worry(worry)
            bored_worry = new_worry // worry_factor

            # See comment in main() to understand this confusing step
            #
            if ring_modulus:
                bored_worry %= ring_modulus

            if (bored_worry % self.modulus) == 0:
                #print('is div so %d' % self.action_t)
                dest = self.action_t
            else:
                #print('is NOT so %d' % self.action_f)
                dest = self.action_f

            #print('worry %d -> %d %d [%d] tossed to %d' %
            #      (worry, new_worry, bored_worry, self.modulus, dest))

            monkeys[dest].worries.append(bored_worry)

        self.inspections += to_inspect

    def print_worries(self):
        print('Monkey %d: %s' %
              (self.name, ', '.join([str(x) for x in self.worries])))

    def __repr__(self):

        # FIXME: complete this
        return '%s %s, (%s, %s), %d' % (
                self.name, self.worries, self.operator, self.operand,
                self.modulus)


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

        mod_toks = tokens[3].split()
        if mod_toks[:3] != ['Test:', 'divisible', 'by']:
            print('oops 1')
        modulus = int(mod_toks[3])

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
                       modulus, action_t, action_f))

    return monkeys


def do_round(monkeys, worry_factor=3, ring_modulus=0):

    for monkey in monkeys:
        monkey.do_turn(
                monkeys, worry_factor=worry_factor, ring_modulus=ring_modulus)

def do_trial(orig_monkeys, n_rounds, worry_factor=3, ring_modulus=0):

    # Always mount a scratch monkey!
    #
    # The rounds are destructive, so we need to start with
    # a fresh copy for every trial
    #
    monkeys = copy.deepcopy(orig_monkeys)

    for _ in range(n_rounds):
        do_round(monkeys, worry_factor=worry_factor, ring_modulus=ring_modulus)

    inspections = [m.inspections for m in monkeys]
    inspections = sorted(inspections)
    business = inspections[-1] * inspections[-2]
    return business


def main():

    # The monkeys get modified by the rounds, so
    # we make copies of the original monkeys before
    # we do any rounds
    #
    base_monkeys = reader()

    # For part 2, the quantity of worry becomes absolutely
    # ridiculously large, because it's always increasing (in
    # some steps, by a lot) and there are 10000 rounds, and
    # even after a few tens of rounds the numbers start to get
    # big enough that Python starts to have issues (i.e.
    # trying to do integer division with floats starts to fail).
    #
    # But here's the insight: we don't actually care about the
    # *magnitude* of the worry -- we only care whether the
    # operations give the right answer when we do the tests
    # to decide which monkey to throw the next item to.  The
    # test is always a modulo operation, so if we do all the
    # worry arithmetic in a ring Z_r where r is divisible
    # by all of the modulo divisors, we'll get the correct
    # answer.
    #
    # I find r using the lazy way of just computing the product
    # of the modulo divisor that each monkey uses.  If I was
    # being elegant, or there were a lot of monkeys, etc,
    # then I could find the LCM instead of the product, but
    # for this puzzle input it doesn't make much difference
    # to amount of work the computer has to do (and no
    # difference at all to the final answer, in any case).
    #
    # If there is a really enormous number of monkeys then
    # I'd have to use the CRT to keep the numbers small
    # enough to use, but at that point I'd just give up
    # and abandon the gold star for today.

    ring_modulus = 1
    for monkey in base_monkeys:
        ring_modulus *= monkey.modulus

    print('part 1: %d' % do_trial(base_monkeys, 20))
    print('part 2: %d' % do_trial(
            base_monkeys, 10000, worry_factor=1, ring_modulus=ring_modulus))

    # A test that the ring works...
    # monkeys1a = copy.deepcopy(base_monkeys)
    # for i in range(20):
    #     do_round(monkeys1a, ring_modulus=ring_modulus)
    #
    # print('== == == ==')
    # inspections = [m.inspections for m in monkeys1a]
    # print('inspections %s' % inspections)
    # inspections = sorted(inspections)
    # business = inspections[-1] * inspections[-2]
    # print('part 1a: %d' % business)

    # Another test:
    # monkeys2a = copy.deepcopy(base_monkeys)
    #for i in range(20):
    #    do_round(monkeys2a, worry_factor=1, ring_modulus=ring_modulus)
    #
    # print('== == == ==')
    # inspections = [m.inspections for m in monkeys2a]
    # print('inspections %s' % inspections)
    # inspections = sorted(inspections)
    # business = inspections[-1] * inspections[-2]
    # print('part 2a: %d' % business)


if __name__ == '__main__':
    main()


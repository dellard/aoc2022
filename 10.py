#!/usr/bin/env python3

import sys


def reader():

    program = []

    for line in sys.stdin:
        line = line.strip()

        if line == 'noop':
            program.append(('noop', 0))
        else:
            opcode, val_s = line.strip().split()
            val = int(val_s)
            program.append((opcode, val))

    return program


def part1(program, base, period):

    cycle = 1
    reg_x = 1
    total = 0

    for opcode, val in program:

        if opcode == 'noop':
            next_reg_x = reg_x
            needed_cycles = 1
        elif opcode == 'addx':
            next_reg_x = reg_x + val
            needed_cycles = 2

        for _ in range(needed_cycles):
            offset = (cycle - base) % period
            if offset == 0:
                total += cycle * reg_x
            cycle += 1

        reg_x = next_reg_x

    return total


def main():
    prog = reader()

    print('part 1 %d' % part1(prog, 20, 40))


if __name__ == '__main__':
    main()

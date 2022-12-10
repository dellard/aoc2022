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


def part2(program, crt_width):

    cycle = 1
    sprite = 1

    row_buf = []

    for opcode, val in program:

        if opcode == 'noop':
            next_sprite = sprite
            needed_cycles = 1
        elif opcode == 'addx':
            next_sprite = sprite + val
            needed_cycles = 2

        for _ in range(needed_cycles):
            # just bodging something together
            col = (cycle - 1) % crt_width
            if col in [sprite - 1, sprite, sprite + 1]:
                row_buf.append('#')
            else:
                row_buf.append(' ')

            # flyback
            if col == crt_width - 1:
                row_buf.append('\n')

            cycle += 1

        sprite = next_sprite

    # We might end up with an "extra" newline on the end,
    # but all that matters for this part is that it's legible
    #
    return ''.join(row_buf)


def main():
    prog = reader()

    print('part 1 %d' % part1(prog, 20, 40))
    print('part 2\n%s' % part2(prog, 40))


if __name__ == '__main__':
    main()

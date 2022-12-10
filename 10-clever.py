#!/usr/bin/env python3

"""
When I started on part 1, I realized that the problem
would be bit simpler if I rewrote the original program
in terms of a more primitive machine with one instruction,
which I'll call "addq".  The addq instruction always
adds its operand to the current register x, and always
takes exactly one cycle.  So

    addx X

becomes 

    addq 0
    addq X

and

    noop

becomes

    addq 0

Since there's only one instruction, we can elide it
entirely and have the program just be the list of
operations.

I didn't implement this initially, because I anticipated
that part 2 would someone depend on the fact that addx
and noop took different numbers of cycles -- but part 2
did not, and also becomes simpler when rewritten in terms
of addq.
"""

import sys


def reader():

    program = []

    for line in sys.stdin:
        line = line.strip()

        if line == 'noop':
            program.append(0)
        else:
            program.append(0)
            opcode, val_s = line.strip().split()
            val = int(val_s)
            program.append(val)

    return program


def part1(program, base, period):

    reg_x = 1
    total = 0

    for prog_counter in range(len(program)):
        next_reg_x = reg_x + program[prog_counter]
        cycle = prog_counter + 1
        offset = (cycle - base) % period

        if offset == 0:
            total += cycle * reg_x

        reg_x = next_reg_x

    return total


def part2(program, crt_width):

    sprite = 1
    row_buf = []

    for prog_counter in range(len(program)):
        next_sprite = sprite + program[prog_counter]
        cycle = prog_counter + 1
        col = (cycle - 1) % crt_width

        # Still a bodge
        if col in [sprite - 1, sprite, sprite + 1]:
            row_buf.append('#')
        else:
            row_buf.append(' ')

        # flyback
        if col == crt_width - 1:
            row_buf.append('\n')

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

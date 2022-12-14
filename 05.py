#!/usr/bin/env python3

import copy
import sys


def reader():

    stacks = None

    # assumption 1
    # important note: in the input, all of first
    # rows (which contain the initial stacks) have
    # all of the columns, even if the columns are
    # empty.  This means that we can tell how many
    # columns there are just by looking at the first
    # row, instead of trying to figure it out as
    # we go.
    #
    # assumption 2
    # Also, the input for the first problem has
    # every item labeled with a single letter,
    # so we can take advantage of the items
    # have a fixed, one-character width,
    # although this seems like the sort of
    # assumption that could totally backfire
    # in the second puzzle.
    #
    # assumption 3
    # There are a fixed number of columns, which
    # could also totally backfire.

    # Read the initial stacks:
    #
    for line in sys.stdin:
        # remove the newline, in a lazy manner
        # Note that we don't want to just do an rstrip
        # because we might need that trailing whitespace
        # (to figure out how many columns there are
        #
        line = line[:-1]

        # If it's the first line, figure out how many
        # stacks there are going to be by looking at the
        # length of the line
        #
        if not stacks:
            n_cols = (len(line) + 1) // 4
            stacks = [[] for i in range(n_cols)]

        # when we're done seeing stacks, break
        # out of this loop
        #
        if not line.strip().startswith('['):
            break

        for i in range(n_cols):

            # assumption 2
            col_width = 4
            item = line[1 + (i * col_width)]

            if item != ' ':
                stacks[i].append(item)

    """
    for i in range(n_cols):
        print(stacks[i])
    """

    commands = []

    for line in sys.stdin:
        tokens = line.strip().split()
        if not tokens:
            continue

        # the laziness is palpable here
        # could have just used a regexp to find all the
        # ints
        #
        cmd = [int(tokens[x]) for x in [1, 3, 5]]
        commands.append(cmd)

    return stacks, commands


def do_command9000(stacks, command):
    return do_command(stacks, command, rev=True)


def do_command9001(stacks, command):
    return do_command(stacks, command, rev=False)


def do_command(stacks, command, rev=True):

    cnt, src_1, dst_1 = command

    # the stack names are 1-based, but our
    # representation is zero-based
    #
    src = src_1 - 1
    dst = dst_1 - 1

    top = stacks[src][:cnt]
    if rev:
        top.reverse()
    stacks[src] = stacks[src][cnt:]
    stacks[dst] = top + stacks[dst]

    return stacks


def main():

    stacks, commands = reader()

    stacks0 = copy.copy(stacks)
    stacks1 = copy.copy(stacks)

    for command in commands:
        stacks0 = do_command9000(stacks0, command)

    print('part 1:', ''.join(stack[0] for stack in stacks0))

    for command in commands:
        stacks1 = do_command9001(stacks1, command)

    print('part 2:', ''.join(stack[0] for stack in stacks1))


if __name__ == '__main__':
    main()

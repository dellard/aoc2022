#!/usr/bin/env python3

"""
Advent of Code 2022 -- day 9

See https://adventofcode.com/2022/day/9
"""

import sys


def reader():
    """
    Read the input moves from stdin

    Each line has two columns: a character that
    represents the direction (R, L, U, or D for
    right, left, up, and down) followed by a
    positive integer representing the count of steps
    to take in that direction.  Return a list of
    direction, count pairs.

    Absolutely no error checking whatsoever is done.
    GIGO.
    """

    moves = []

    for line in sys.stdin:
        (direction, steps_s) = line.strip().split()
        steps = int(steps_s)

        moves.append((direction, steps))

    return moves


def move_one(head, tail, direction):
    """
    Move the head one step in the given direction,
    update the tail position if necessary, and return
    the updated positions of the head and tail

    Note that this is only used in the solution for
    the first part, because it assumes that there's
    only a head and tail, and no intermediate knots
    """

    new_head = move_head(head, direction)
    new_tail = move_tail(new_head, tail)

    return new_head, new_tail


def move_head(head, direction):
    """
    Return the result of moving the head one step
    in the given direction
    """

    if direction == 'R':
        inc = (1, 0)
    elif direction == 'L':
        inc = (-1, 0)
    elif direction == 'U':
        inc = (0, 1)
    elif direction == 'D':
        inc = (0, -1)

    new_head = head[0] + inc[0], head[1] + inc[1]

    return new_head


def move_tail(head, tail):
    """
    Given a new position for the head, and the current
    position of the tail, update the tail to move closer
    to the head and return the new position of the tail

    Note that if the tail is already "near" to the
    head, then no move is necessary and the tail remains
    where it is.

    Note that no error checking is done to ensure that
    the head and tail are in valid positions relative to
    each other.
    """

    diff = head[0] - tail[0], head[1] - tail[1]
    near = abs(diff[0]), abs(diff[1])

    if near in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        return tail

    if diff[0] and diff[1]:
        # if both elements of diff are non-zero, then
        # it's a diagonal move
        diag = 1 if diff[0] > 0 else -1, 1 if diff[1] > 0 else -1

        new_tail = tail[0] + diag[0], tail[1] + diag[1]
    else:
        # at this point, it must be a vertical or
        # horizontal move

        if diff[0] > 0:
            inc = (1, 0)
        elif diff[0] < 0:
            inc = (-1, 0)
        elif diff[1] > 0:
            inc = (0, 1)
        else:
            inc = (0, -1)

        new_tail = tail[0] + inc[0], tail[1] + inc[1]

    return new_tail


def make_move1(head, tail, move, visited):
    """
    Make a move for part 1

    For part 1, there is only a head and tail
    """

    direction, steps = move

    # print('direction %s steps %d' % (direction, steps))

    visited.add(tail)

    for _ in range(steps):
        head, tail = move_one(head, tail, direction)
        visited.add(tail)

    return head, tail


def make_move2(knots, move, visited):
    """
    Make a move for part 2

    For part 2, there may be any number of knots

    Note: this code assumes that there is at least
    one knot, which is treated as a head.
    """

    direction, steps = move

    # not necessary, for the current conditions where
    # the knots all start together, but doesn't hurt
    # anything
    #
    visited.add(knots[-1])

    for _ in range(steps):

        new_head = move_head(knots[0], direction)
        new_knots = [new_head]

        for i in range(1, len(knots), 1):
            new_knot = move_tail(new_knots[-1], knots[i])
            new_knots.append(new_knot)

        knots = new_knots

        visited.add(knots[-1])

    return knots


def part1(moves, start):
    """
    Solution for part 1 -- move the head according
    to the list of moves, and return the number of
    unique positions occupied by the tail as it
    drags behind the head

    Both the head and tail begin at the start position
    """

    visited = set()

    head = start
    tail = start

    for move in moves:
        head, tail = make_move1(head, tail, move, visited)

    return len(visited)


def part2(moves, start, n_knots):
    """
    Solution for part 2 -- move the head according
    to the list of moves, and then drag the following
    knots behind it, and return the number of unique
    positions occupied by the tail (the last knot)

    All the knots (including the head and tail) begin
    at the start position
    """

    visited = set()

    knots = [start] * n_knots

    for move in moves:
        knots = make_move2(knots, move, visited)

    return len(visited)


def main():
    """
    Execute the different parts; print the results
    """

    moves = reader()

    print('part 1: %d' % part1(moves, (0, 0)))

    # redo part1 using the generalized method for n knots
    # print('part 1 redone: %d' % part2(moves, (0, 0), 2))

    print('part 2: %d' % part2(moves, (0, 0), 10))


if __name__ == '__main__':
    main()

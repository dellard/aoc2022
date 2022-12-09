#!/usr/bin/env python3

import sys

def reader():

    moves = list()

    for line in sys.stdin:
        (direction, steps_s) = line.strip().split()
        steps = int(steps_s)

        moves.append((direction, steps))

    return moves


def move_one(head, tail, direction):

    new_head = move_head(head, direction)
    new_tail = move_tail(new_head, tail)

    return new_head, new_tail


def move_head(head, direction):

    if direction == 'U':
        inc = (0, 1)
    elif direction == 'D':
        inc = (0, -1)
    elif direction == 'L':
        inc = (-1, 0)
    elif direction == 'R':
        inc = (1, 0)
    else:
        print('Ooops 1')

    new_head = head[0] + inc[0], head[1] + inc[1]

    return new_head

def move_tail(head, tail):

    diff = head[0] - tail[0], head[1] - tail[1]
    near = abs(diff[0]), abs(diff[1])

    if head == tail:
        #print('overlap')
        new_tail = tail
    elif near in [(0, 1), (1, 0), (1, 1)]:
        #print('close enough')
        new_tail = tail
    else:
        if diff[0] * diff[1]:
            # it's a diagonal move
            diag = 1 if diff[0] > 0 else -1, 1 if diff[1] > 0 else -1
            #print('diagonal %s' % str(diag))
            new_tail = tail[0] + diag[0], tail[1] + diag[1]
        else:
            #print('straight')

            if diff[0] > 0:
                inc = (1, 0)
            elif diff[0] < 0:
                inc = (-1, 0)
            elif diff[1] > 0:
                inc = (0, 1)
            else:
                inc = (0, -1)

            # print('inc = %s' % str(inc))
            new_tail = tail[0] + inc[0], tail[1] + inc[1]
            # it's a straight move

    #print('%s, %s -> %s %s' % (head, tail, new_head, new_tail))

    return new_tail


def make_move1(head, tail, move, visited):

    direction, steps = move

    #print('direction %s steps %d' % (direction, steps))

    visited.add(tail)

    for _ in range(steps):
        head, tail = move_one(head, tail, direction)
        visited.add(tail)

    return head, tail


def make_move2(knots, move, visited):

    direction, steps = move

    #print('direction %s steps %d' % (direction, steps))

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

    visited = set()

    head = start
    tail = start

    for move in moves:
        head, tail = make_move1(head, tail, move, visited)

    return len(visited)


def part2(moves, start, n_knots):

    visited = set()

    knots = [start] * n_knots

    for move in moves:
        knots = make_move2(knots, move, visited)

    return len(visited)


def main():

    moves = reader()

    print('part 1: %d' % part1(moves, (0, 0)))
    print('part 2: %d' % part2(moves, (0, 0), 10))

    # redo part1 using the generalized method for n knots
    print('part 1 redone: %d' % part2(moves, (0, 0), 2))


if __name__ == '__main__':
    main()

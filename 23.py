#!/usr/bin/env python3

"""
Advent of Code 2022, day 23
"""

import sys


def reader():

    elves = set()

    rownum = 0
    for line in sys.stdin:
        row = line.strip()
        for colnum in range(len(row)):
            if row[colnum] == '#':
                elves.add((colnum, rownum))

        rownum += 1

    return elves


def find_extent(positions):
    """
    Find the extents of the current elf "rectangle"
    and the area (occupied or unoccupied) of this rectangle
    """

    if not positions:
        # This should never happen
        #
        return 0, (0, 0), (0, 0)

    x_min = min(x_pos for x_pos, y_pos in positions)
    y_min = min(y_pos for x_pos, y_pos in positions)
    x_max = max(x_pos for x_pos, y_pos in positions)
    y_max = max(y_pos for x_pos, y_pos in positions)

    area = (1 + x_max - x_min) * (1 + y_max - y_min)
    return area, (x_min, y_min), (x_max, y_max)


# You have entered a region of dense copy/pasting.

def move_n(pos):
    return pos[0], pos[1] - 1


def move_e(pos):
    return pos[0] + 1, pos[1]


def move_s(pos):
    return pos[0], pos[1] + 1


def move_w(pos):
    return pos[0] - 1, pos[1]


def move_ne(pos):
    return move_n(move_e(pos))


def move_nw(pos):
    return move_n(move_w(pos))


def move_se(pos):
    return move_s(move_e(pos))


def move_sw(pos):
    return move_s(move_w(pos))


def occ(elves, pos):
    return pos in elves


def unocc(elves, pos):
    return pos not in elves


def check_n(elves, pos):
    if all([
            unocc(elves, move_ne(pos)),
            unocc(elves, move_n(pos)),
            unocc(elves, move_nw(pos))]):
        return move_n(pos)
    else:
        return None


def check_s(elves, pos):
    if all([
            unocc(elves, move_se(pos)),
            unocc(elves, move_s(pos)),
            unocc(elves, move_sw(pos))]):
        return move_s(pos)
    else:
        return None


def check_e(elves, pos):
    if all([
            unocc(elves, move_ne(pos)),
            unocc(elves, move_e(pos)),
            unocc(elves, move_se(pos))]):
        return move_e(pos)
    else:
        return None


def check_w(elves, pos):
    if all([
            unocc(elves, move_nw(pos)),
            unocc(elves, move_w(pos)),
            unocc(elves, move_sw(pos))]):
        return move_w(pos)
    else:
        return None


def neighbor_count(elves, pos):

    p_x, p_y = pos

    cnt = 0
    for e_x in range(p_x - 1, p_x + 2, 1):
        for e_y in range(p_y - 1, p_y + 2, 1):
            if e_x == p_x and e_y == p_y:
                continue
            if (e_x, e_y) in elves:
                cnt += 1

    return cnt


def round_step1(elves, round_number):

    move_order = [check_n, check_s, check_w, check_e]

    # pure laziness
    n_directions = len(move_order)
    base = round_number % n_directions
    move_order += move_order

    move_order = move_order[base:base + n_directions]

    # spots is a pair of positions: where each elf is,
    # and where it wants to go
    # cnts is the number of elves who want to go to
    # each position (for positions any elves actually
    # want to go to)
    #
    proposed_spots = set()
    proposed_cnts = {}

    for pos in elves:
        if neighbor_count(elves, pos) == 0:
            # No neighbors?  Happily stay where you are.
            new_pos = pos
        else:
            # Try moving in each direction until you find
            # one that works, or give up in despair
            #
            for move in move_order:
                new_pos = move(elves, pos)
                if new_pos:
                    break

        if not new_pos:
            new_pos = pos

        proposed_spots.add((pos, new_pos))
        if new_pos not in proposed_cnts:
            proposed_cnts[new_pos] = 0
        proposed_cnts[new_pos] += 1

    new_positions = set()

    for curr_pos, proposed_pos in proposed_spots:
        if proposed_cnts[proposed_pos] == 1:
            new_positions.add(proposed_pos)
        else:
            new_positions.add(curr_pos)

    return new_positions


def print_elves(elves):
    """
    For debugging: print the positions of the elves
    """

    _, min_pos, max_pos = find_extent(elves)

    min_x, min_y = min_pos
    max_x, max_y = max_pos

    buf = []
    for e_y in range(min_y, max_y + 1, 1):
        for e_x in range(min_x, max_x + 1, 1):
            if (e_x, e_y) in elves:
                buf.append('#')
            else:
                buf.append('.')

        buf.append('\n')

    print(''.join(buf))


def part1(elves):

    for rnd in range(10):
        elves = round_step1(elves, rnd)

    area, _, _ = find_extent(elves)
    return area - len(elves)


def part2(elves):

    rnd = 0
    while True:
        new_elves = round_step1(elves, rnd)
        if elves == new_elves:
            break

        elves = new_elves
        rnd += 1

    return 1 + rnd


def main():

    elves = reader()

    #print_elves(elves)
    #print('============')

    print('part 1: %d' % part1(elves))
    print('part 2: %d' % part2(elves))




if __name__ == '__main__':
    main()

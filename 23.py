#!/usr/bin/env python3

import sys


def reader():

    rows = []
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

    unset = True
    for x_pos, y_pos in positions:
        if unset:
            unset = False
            x_min, y_min = x_pos, y_pos
            x_max, y_max = x_pos, y_pos
            continue

        if x_min > x_pos:
            x_min = x_pos
        if x_max < x_pos:
            x_max = x_pos
        if y_min > y_pos:
            y_min = y_pos
        if y_max < y_pos:
            y_max = y_pos

    area = (1 + x_max - x_min) * (1 + y_max - y_min)
    return area, (x_min, y_min), (x_max, y_max)


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
    for x in range(p_x - 1, p_x + 2, 1):
        for y in range(p_y - 1, p_y + 2, 1):
            if x == y:
                continue
            if (x, y) in elves:
                cnt += 1

    return cnt


def round_step1(elves, round_number):

    move_order = [
            check_n, check_s, check_w, check_e
        ]
    test_order = [0, 1, 2, 3]

    # pure laziness
    n_directions = len(move_order)
    base = round_number % n_directions
    move_order += move_order
    test_order += test_order

    move_order = move_order[base:base + n_directions]
    test_order = test_order[base:base + n_directions]
    print('TEST ORDER ', test_order)
    # print('moves %d %d %s' % (base, round_number, move_order))

    proposed_spots = set()
    proposed_cnts = {}

    for pos in elves:
        if neighbor_count(elves, pos) == 0:
            new_pos = pos
        else:
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

    _, min_pos, max_pos = find_extent(elves)

    min_x, min_y = min_pos
    max_x, max_y = max_pos

    buf = []
    for y in range(min_y, max_y + 1, 1):
        for x in range(min_x, max_x + 1, 1):
            if (x, y) in elves:
                buf.append('#')
            else:
                buf.append('.')

        buf.append('\n')

    print(''.join(buf))


def main():

    elves = reader()

    print_elves(elves)
    print('============')

    elves = round_step1(elves, 0)
    print_elves(elves)
    print('============')
    elves = round_step1(elves, 1)
    print_elves(elves)
    print('============')

    area, min_p, max_p = find_extent(elves)
    print('min_p ', min_p)
    print('max_p ', max_p)
    print('occupied ', len(elves))
    print('part 1: %d' % (area - len(elves)))



if __name__ == '__main__':
    main()

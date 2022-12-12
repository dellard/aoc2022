#!/usr/bin/env python3

import re
import sys

HUGE = 1000 * 1000
BORDER = 0

# I'm being lazy
sys.setrecursionlimit(100000)

def reader():

    grid = []

    row = 0

    for line in sys.stdin:
        row += 1
        line = line.strip()
        if 'S' in line:
            start_pos = (row, line.find('S') + 1)
            line = re.sub('S', 'a', line)
        if 'E' in line:
            end_pos = (row, line.find('E') + 1)
            line = re.sub('E', 'z', line)

            # print('end %s' % str(end_pos))

        line = [BORDER] + [ord(c) for c in line] + [BORDER]

        grid.append(line)

    grid.insert(0, [BORDER] * len(line))
    grid.append([BORDER] * len(line))

    return grid, start_pos, end_pos


def get_grid_val(grid, pos):
    return grid[pos[0]][pos[1]]


def set_grid_val(grid, pos, val):
    grid[pos[0]][pos[1]] = val


def find_path(grid, start_pos, end_positions):

    rows = len(grid)
    cols = len(grid[0])

    visited = []
    for row in range(len(grid)):
        visited.append([HUGE] * len(grid[0]))

    # print(grid)

    shortest = find_path_worker(grid, visited, start_pos, end_positions, 0)

    # print(end_pos)
    # print_visited(visited)

    return shortest


def print_visited(visited):

    for row in visited:
        buf = ''
        for col in row:
            if col == HUGE:
                buf += '   '
            else:
                buf += '%.2d ' % col

        print(buf)


def find_path_worker(
        grid, visited, curr_pos, end_positions, path_len):

    # print('trying %s len %d' % (str(curr_pos), path_len))

    if get_grid_val(grid, curr_pos) == BORDER:
        return HUGE

    if curr_pos in end_positions:
        set_grid_val(visited, curr_pos, path_len)
        return 0

    if path_len >= get_grid_val(visited, curr_pos):
        return HUGE

    set_grid_val(visited, curr_pos, path_len)

    curr_alt = get_grid_val(grid, curr_pos)

    row, col = curr_pos
    left = row, col - 1
    right = row, col + 1
    up = row - 1, col
    down = row + 1, col

    potential_lengths = []

    for new_pos in [left, right, up, down]:
        if get_grid_val(grid, new_pos) - curr_alt <= 1:
            potential_lengths.append(
                    find_path_worker(
                        grid, visited, new_pos, end_positions, path_len + 1))

    # print('potentials %s' % str(potential_lengths))
    shortest_len = 1 + min(potential_lengths)

    return shortest_len


def find_all_as(grid):

    all_as = set()

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pos = (row, col)
            if get_grid_val(grid, pos) == ord('a'):
                all_as.add(pos)

    return all_as


def main():

    grid, start, end = reader()

    shortest = find_path(grid, start, set([end]))
    print('part 1: %d' % shortest)

    # being super lazy here; instead of generalizing the
    # searching function, I'm just going to flip the grid
    # over and then search from the ending backwards
    #
    flipped_grid = []
    for row in grid:
        flipped_grid.append([-v for v in row])

    all_as = find_all_as(grid)
    shortest = find_path(flipped_grid, end, all_as)
    print('part 2: %d' % shortest)


main()

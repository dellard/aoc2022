#!/usr/bin/env python3

import re
import sys

# An impossibly long path... at least for the
# input of this puzzle

HUGE = 10000 * 10000

# The BORDER sentinel value must be zero, because
# later we use the negation of the altitudes and
# having BORDER = 0 means that BORDER = -BORDER,
# which gives us one less thing to worry about
#
BORDER = 0

# I'm being lazy.  It would be more efficient to use
# a queue instead of the stack, but whatever.
#
sys.setrecursionlimit(100000)


def reader():
    """
    Read the input; return the altitude grid and
    the start and end positions

    I put a border of BORDER sentinel values around
    the grid, so I don't have to check whether I've
    fallen off the sides.  This means that the grid
    doesn't have to be rectangular, and simplifies
    some things, but might be overkill for this
    task.
    """

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

        line = [BORDER] + [ord(c) for c in line] + [BORDER]

        grid.append(line)

    grid.insert(0, [BORDER] * len(line))
    grid.append([BORDER] * len(line))

    return grid, start_pos, end_pos


def get_grid_val(grid, pos):
    """
    Get the value of a grid at the given position

    No bounds checking is done.

    Reduces the number of times I have to type [ and ],
    which matters to me, but really this is just a
    minimal accessor function
    """

    return grid[pos[0]][pos[1]]


def set_grid_val(grid, pos, val):
    """
    Set the value of a grid at the given position
    to the given value

    No bounds checking is done.

    Reduces the number of times I have to type [ and ],
    which matters to me, but really this is just a
    minimal accessor function
    """

    grid[pos[0]][pos[1]] = val


def find_path(grid, start_pos, end_positions):
    """
    Return the length of the shortest path from
    the start position to any position in the set
    of end positions, where the possible steps
    from each position are as defined by the problem
    description
    """

    # Make a grid of how many steps it might take to
    # reach # each position; assume that every position
    # is HUGEly far away
    #
    visited = []
    for _ in range(len(grid)):
        visited.append([HUGE] * len(grid[0]))

    shortest = find_path_worker(grid, visited, start_pos, end_positions, 0)

    return shortest


def find_path_worker(
        grid, visited, curr_pos, end_positions, path_len):
    """
    Resursively search for the shortest path from the current
    position to any of the end positions and return it

    Destructively fills in the visited grid with path lengths
    that we learn as we go
    """

    # Base case: any path through the border is HUGE
    #
    if get_grid_val(grid, curr_pos) == BORDER:
        return HUGE

    # Base case: we already found another way to
    # reach the current position via a path of
    # lesser or equal length; no point in continuing
    #
    if path_len >= get_grid_val(visited, curr_pos):
        return HUGE

    set_grid_val(visited, curr_pos, path_len)

    # Base case: we reached an end position; yay
    #
    if curr_pos in end_positions:
        return 0

    curr_alt = get_grid_val(grid, curr_pos)
    row, col = curr_pos

    left = row, col - 1
    right = row, col + 1
    up = row - 1, col
    down = row + 1, col

    candidates = []

    for next_pos in [left, right, up, down]:
        if get_grid_val(grid, next_pos) - curr_alt <= 1:
            candidates.append(
                    find_path_worker(
                        grid, visited, next_pos, end_positions, path_len + 1))

    return 1 + min(candidates)


def print_visited(visited):
    """
    For debugging
    """

    for row in visited:
        buf = ''
        for col in row:
            if col == HUGE:
                buf += '   '
            else:
                buf += '%.2d ' % col

        print(buf)


def find_all_as(grid):
    """
    Find all the grid positions that contain an 'a'

    Lazily written function for a special purpose;
    could be generalized
    """

    all_as = set()

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pos = (row, col)
            if get_grid_val(grid, pos) == ord('a'):
                all_as.add(pos)

    return all_as


def main():
    """
    Do the puzzle for day 12
    """

    grid, start, end = reader()

    shortest = find_path(grid, start, set([end]))
    print('part 1: %d' % shortest)

    # being super lazy here; instead of generalizing the
    # searching function, I'm just going to invert the
    # altitude grid and then search from the end position
    # backwards to all the possible start positions
    #
    flipped_grid = []
    for row in grid:
        flipped_grid.append([-v for v in row])

    shortest = find_path(flipped_grid, end, find_all_as(grid))
    print('part 2: %d' % shortest)


if __name__ == '__main__':
    main()

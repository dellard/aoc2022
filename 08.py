#!/usr/bin/env python3

"""
Advent of Code 2022, day 8
"""


import sys


def reader():

    rows = []
    for line in sys.stdin:
        # assume that the input is properly formed

        rows.append([int(x) for x in line.strip()])

    # no sanity checks to make sure that the
    # grid is rectangular, or sane in any
    # other manner

    return rows


def find_visible_linear(grid, start, step):

    seen = set()

    start_col, start_row = start
    step_col, step_row = step

    # we're assuming the grid is square

    n_rows = len(grid)
    highest_seen = -1

    for i in range(n_rows):
        row = start_row + (i * step_row)
        col = start_col + (i * step_col)

        elem = grid[row][col]
        if elem > highest_seen:
            highest_seen = elem
            seen.add((row, col))

    return seen


def find_n_scenic(grid, row, col):

    n_rows = len(grid)
    my_height = grid[row][col]

    # so much repetition...

    visible_down = 0
    for i in range(row + 1, n_rows, 1):
        visible_down += 1
        if my_height <= grid[i][col]:
            break

    visible_up = 0
    for i in range(row - 1, -1, -1):
        visible_up += 1
        if my_height <= grid[i][col]:
            break

    visible_right = 0
    for i in range(col + 1, n_rows, 1):
        visible_right += 1
        if my_height <= grid[row][i]:
            break

    visible_left = 0
    for i in range(col - 1, -1, -1):
        visible_left += 1
        if my_height <= grid[row][i]:
            break

    score = visible_up * visible_down * visible_right * visible_left

    return score


def find_max_scenic(grid):

    max_scenic = 0
    n_rows = len(grid)

    for row in range(n_rows):
        for col in range(n_rows):
            scenic = find_n_scenic(grid, row, col)
            if scenic > max_scenic:
                max_scenic = scenic

    return max_scenic


def count_visible(grid):

    # again, we're assuming that the grid is
    # well-formed and square, or else kaboom

    seen = set()

    n_rows = len(grid)
    for i in range(n_rows):
        seen |= find_visible_linear(grid, (i, 0), (0, 1))
        seen |= find_visible_linear(grid, (i, n_rows - 1), (0, -1))

        seen |= find_visible_linear(grid, (0, i), (1, 0))
        seen |= find_visible_linear(grid, (n_rows - 1, i), (-1, 0))

    return len(seen)


def main():
    grid = reader()

    print('part 1: %d' % count_visible(grid))
    print('part 2: %d' % find_max_scenic(grid))


if __name__ == '__main__':
    main()

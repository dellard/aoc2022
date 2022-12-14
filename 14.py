#!/usr/bin/env python3

import sys

class Cave:

    MIN_X, MAX_X = -1, -1
    MIN_Y, MAX_Y = 0, -1

def reader():

    all_paths = []

    for line in sys.stdin:

        points = line.strip().split('->')
        path = []
        for point in points:
            x_s, y_s = point.split(',')
            x, y = int(x_s), int(y_s)
            path.append((x, y))

            if Cave.MIN_X == -1 or x < Cave.MIN_X:
                Cave.MIN_X = x
            if Cave.MAX_X == -1 or x > Cave.MAX_X:
                Cave.MAX_X = x

            if Cave.MAX_Y == -1 or y > Cave.MAX_Y:
                Cave.MAX_Y = y

        all_paths.append(path)

    # add a space on each side, for sand to flow out
    Cave.MIN_X -= 1
    Cave.MAX_X += 1

    if Cave.MIN_X < 0:
        print('OOPS')
        sys.exit(1)

    grid = []
    for _ in range(Cave.MAX_Y + 1):
        grid.append(['.'] * (1 + Cave.MAX_X - Cave.MIN_X))

    #print('(%d, %d) (%d, %d)' % (Cave.MIN_X, Cave.MIN_Y, Cave.MAX_X, Cave.MAX_Y))

    for path in all_paths:
        curr_x, curr_y = path[0]
        #print('start (%d, %d)' % (curr_x, curr_y))

        for next_x, next_y in path[1:]:
            #print('next (%d, %d)' % (next_x, next_y))
            if curr_x == next_x:
                for y in range(
                        min(next_y, curr_y), 1 + max(next_y, curr_y), 1):
                    set_grid(grid, curr_x, y, '#')
                    #print('filling (%d, %d)' % (curr_x, y))
            else:
                for x in range(
                        min(next_x, curr_x), 1 + max(next_x, curr_x), 1):
                    set_grid(grid, x, curr_y, '#')
                    #print('filling (%d, %d)' % (x, curr_y))

            curr_x, curr_y = next_x, next_y

    return all_paths, grid


def print_grid(grid):

    for r in grid:
        print(''.join(r))


def set_grid(grid, x, y, val):

    grid[y - Cave.MIN_Y][x - Cave.MIN_X] = val


def get_grid(grid, x, y):
    return grid[y - Cave.MIN_Y][x - Cave.MIN_X]


def fill_grid(grid, hole_x, hole_y):

    curr_x, curr_y = hole_x, hole_y

    while True:
        if curr_y == Cave.MAX_Y:
            # We have reached the bottom
            return 'FULL'

        if get_grid(grid, curr_x, curr_y + 1) == '.':
            curr_y += 1
        elif get_grid(grid, curr_x - 1, curr_y + 1) == '.':
            curr_y += 1
            curr_x -= 1
        elif get_grid(grid, curr_x + 1, curr_y + 1) == '.':
            curr_y += 1
            curr_x += 1
        else:
            set_grid(grid, curr_x, curr_y, 'o')
            break

    return 'UNFULL'


def main():

    paths, grid  = reader()
    print('(%d, %d) (%d, %d)' % (Cave.MIN_X, Cave.MIN_Y, Cave.MAX_X, Cave.MAX_Y))

    #print_grid(grid)

    counter = 0
    while fill_grid(grid, 500, 0) != 'FULL':
        counter += 1

    print('part 1: %d' % counter)


main()

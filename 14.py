#!/usr/bin/env python3

import copy
import sys

class Cave:

    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        self.grid = []
        for _ in range(max_y + 1):
            self.grid.append(['.'] * (1 + max_x - min_x))

        self.print_grid()

    def print_grid(self):
        for r in self.grid:
            print(''.join(r))

    def set_grid(self, x, y, val):

        # print('set %d, %d' % (x, y))
        # print('min %d, %d' % (self.min_x, self.min_y))
        # print('rep %d, %d' % (x - self.min_x, y - self.min_y))
        self.grid[y - self.min_y][x - self.min_x] = val

    def get_grid(self, x, y):
        return self.grid[y - self.min_y][x - self.min_x]


def reader():

    all_paths = []

    min_x, max_x = -1, -1
    min_y, max_y = 0, -1

    for line in sys.stdin:

        points = line.strip().split('->')
        path = []
        for point in points:
            x_s, y_s = point.split(',')
            x, y = int(x_s), int(y_s)
            path.append((x, y))

            if min_x == -1 or x < min_x:
                min_x = x
            if max_x == -1 or x > max_x:
                max_x = x

            if max_y == -1 or y > max_y:
                max_y = y

        all_paths.append(path)

    # add a space on each side, for sand to flow out
    min_x -= 1
    max_x += 1

    if min_x < 0:
        print('OOPS')
        sys.exit(1)

    cave = Cave(min_x, max_x, min_y, max_y)

    #print('(%d, %d) (%d, %d)' % (Cave.MIN_X, Cave.MIN_Y, Cave.MAX_X, Cave.MAX_Y))

    for path in all_paths:
        curr_x, curr_y = path[0]
        #print('start (%d, %d)' % (curr_x, curr_y))

        for next_x, next_y in path[1:]:
            #print('next (%d, %d)' % (next_x, next_y))
            if curr_x == next_x:
                for y in range(
                        min(next_y, curr_y), 1 + max(next_y, curr_y), 1):
                    cave.set_grid(curr_x, y, '#')
                    #print('filling (%d, %d)' % (curr_x, y))
            else:
                for x in range(
                        min(next_x, curr_x), 1 + max(next_x, curr_x), 1):
                    cave.set_grid(x, curr_y, '#')
                    #print('filling (%d, %d)' % (x, curr_y))

            curr_x, curr_y = next_x, next_y

    #return all_paths, grid
    return cave


def fill_grid(cave, hole_x, hole_y, stop_at_bottom=True):

    curr_x, curr_y = hole_x, hole_y

    while True:
        if curr_y == cave.max_y:
            # We have reached the bottom
            return 'FULL'

        if cave.get_grid(curr_x, curr_y + 1) == '.':
            curr_y += 1
        elif cave.get_grid(curr_x - 1, curr_y + 1) == '.':
            curr_y += 1
            curr_x -= 1
        elif cave.get_grid(curr_x + 1, curr_y + 1) == '.':
            curr_y += 1
            curr_x += 1
        else:
            cave.set_grid(curr_x, curr_y, 'o')
            break

    # We're jammed at the starting hole
    if (curr_x, curr_y) == (hole_x, hole_y):
        return 'FULL'
    else:
        return 'UNFULL'


def part1(cave, stop_at_bottom=True):

    counter = 0
    while fill_grid(cave, 500, 0, stop_at_bottom) != 'FULL':
        # cave.print_grid()
        counter += 1

    return counter


def part2(cave, hole_x=500):
    """
    We need to fatten out the grid

    The fullest that the grid can get is a triangle
    from the hole to the base, where the extent along
    the base is equal to the height in each direction,
    plus one.
    """

    deeper_cave = copy.deepcopy(cave)

    new_min_x = min(cave.min_x, hole_x - (cave.max_y + 3))
    new_max_x = max(cave.max_x, hole_x + (cave.max_y + 3))

    if new_min_x < cave.min_x:
        prefix_len = cave.min_x - new_min_x
    else:
        prefix_len = 0

    if new_max_x > cave.max_x:
        suffix_len = new_max_x - cave.max_x
    else:
        suffix_len = 0

    for i in range(len(deeper_cave.grid)):
        pref = ['.'] * prefix_len
        suff = ['.'] * suffix_len
        deeper_cave.grid[i] = pref + deeper_cave.grid[i] + suff

    deeper_cave.grid.append(['.'] * (1 + new_max_x - new_min_x))
    deeper_cave.grid.append(['#'] * (1 + new_max_x - new_min_x))

    deeper_cave.min_x = new_min_x
    deeper_cave.max_x = new_max_x
    deeper_cave.max_y = cave.max_y + 2

    # deeper_cave.print_grid()

    cnt = part1(deeper_cave, stop_at_bottom=False)
    # deeper_cave.print_grid()

    # the last bit of sand returns FULL, but it still counts
    #
    # NOTE: this assumes that the hole isn't filled at the
    # start; that would be embarassing
    #
    return 1 + cnt


def main():

    cave  = reader()
    # print('(%d, %d) (%d, %d)' % (Cave.MIN_X, Cave.MIN_Y, Cave.MAX_X, Cave.MAX_Y))

    #print_grid(grid)

    print('part 1: %d' % part1(copy.deepcopy(cave)))
    print('part 2: %d' % part2(copy.deepcopy(cave)))


main()

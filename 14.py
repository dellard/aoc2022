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

    def print_grid(self):
        for r in self.grid:
            print(''.join(r))

    def set_grid(self, x, y, val):
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

    # TODO: Should be a method in Cave
    #
    for path in all_paths:
        curr_x, curr_y = path[0]

        for next_x, next_y in path[1:]:
            if curr_x == next_x:
                for y in range(
                        min(next_y, curr_y), 1 + max(next_y, curr_y), 1):
                    cave.set_grid(curr_x, y, '#')
            else:
                for x in range(
                        min(next_x, curr_x), 1 + max(next_x, curr_x), 1):
                    cave.set_grid(x, curr_y, '#')

            curr_x, curr_y = next_x, next_y

    return cave


def fill_grid(cave, hole_x, hole_y):

    curr_x, curr_y = hole_x, hole_y

    # Are we jammed at the hole itself?
    #
    if cave.get_grid(hole_x, hole_y) != '.':
        return 0

    while True:
        if curr_y == cave.max_y:
            # We have reached the bottom; the sand will
            # not remain in the cave
            #
            return 0

        # Try down, then left+down, the right+down
        #
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
            return 1


def part1(cave, hole_x=500):

    # Destructive; need to make a copy
    #
    cave = copy.deepcopy(cave)

    counter = 0
    while fill_grid(cave, hole_x, 0):
        # cave.print_grid()
        counter += 1

    return counter


def part2(cave, hole_x=500):
    """
    We need to expand the grid; bash together a new
    cave with fatter dimensions, using a sequence of
    shameful shortcuts

    The new cave is 2 rows deeper than the original,
    and the "fullest" that the grid can get is a triangle
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

    # Cringe
    for i in range(len(deeper_cave.grid)):
        pref = ['.'] * prefix_len
        suff = ['.'] * suffix_len
        deeper_cave.grid[i] = pref + deeper_cave.grid[i] + suff

    deeper_cave.grid.append(['.'] * (1 + new_max_x - new_min_x))
    deeper_cave.grid.append(['#'] * (1 + new_max_x - new_min_x))

    deeper_cave.min_x = new_min_x
    deeper_cave.max_x = new_max_x
    deeper_cave.max_y = cave.max_y + 2

    cnt = part1(deeper_cave)

    return cnt


def main():

    cave = reader()

    print('part 1: %d' % part1(cave))
    print('part 2: %d' % part2(cave))


main()

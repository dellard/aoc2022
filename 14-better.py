#!/usr/bin/env python3

import copy
import sys


class Cave:

    EMPTY = '.'
    SAND = 'o'
    ROCK = '#'

    def __init__(self, min_x, max_x, min_y, max_y, hole_x=500, filling=False):

        if min_y != 0:
            print('I assumed y would always be 0')
            sys.exit(1)

        if filling:
            # The new cave is 2 rows deeper than the original,
            # and the "fullest" that the grid can get is a triangle
            # from the hole to the base, where the extent along
            # the base (the x direction) in each direction away
            # from the hole is equal to the height plus one.

            max_y += 2
            min_x = min(min_x, hole_x - (max_y + 1))
            max_x = max(max_x, hole_x + (max_y + 1))

        if min_x < 0:
            print('I assumed x would always be at least 0')
            sys.exit(1)

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        self.grid = []
        for _ in range(max_y + 1):
            self.grid.append([Cave.EMPTY] * (1 + max_x - min_x))

        if filling:
            self.add_rock_segment(min_x, max_y, max_x, max_y)

    def add_rock_segment(self, x0, y0, x1, y1):

        if x0 == x1:
            for y in range(min(y0, y1), 1 + max(y0, y1), 1):
                self.set_grid(x0, y, Cave.ROCK)
        else:
            for x in range(min(x0, x1), 1 + max(x0, x1), 1):
                self.set_grid(x, y0, Cave.ROCK)

    def print_grid(self):
        for r in self.grid:
            print(''.join(r))

    def set_grid(self, x, y, val):
        self.grid[y - self.min_y][x - self.min_x] = val

    def get_grid(self, x, y):
        return self.grid[y - self.min_y][x - self.min_x]

    def add_sand(self, hole_x, hole_y):
        # TODO: make into a method in Cave?

        curr_x, curr_y = hole_x, hole_y

        # Are we jammed at the hole itself?
        #
        if self.get_grid(hole_x, hole_y) != Cave.EMPTY:
            return 0

        while True:
            if curr_y == self.max_y:
                # We have reached the bottom; the sand will
                # not remain in the cave
                #
                return 0

            # Try down, then left+down, the right+down
            #
            if self.get_grid(curr_x, curr_y + 1) == Cave.EMPTY:
                curr_y += 1
            elif self.get_grid(curr_x - 1, curr_y + 1) == Cave.EMPTY:
                curr_y += 1
                curr_x -= 1
            elif self.get_grid(curr_x + 1, curr_y + 1) == Cave.EMPTY:
                curr_y += 1
                curr_x += 1
            else:
                self.set_grid(curr_x, curr_y, Cave.SAND)
                return 1


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

    # add a space on each side, for sand to flow out if there
    # aren't any other gaps at the base
    # 
    # This isn't always necessary unless there's a rock along the
    # floor, and might even be wrong in some cases, I think, but
    # I'm not certain and it worked for the cases I tried...
    #
    min_x -= 1
    max_x += 1

    if min_x < 0:
        print('OOPS')
        sys.exit(1)

    return all_paths, min_x, max_x, min_y, max_y


def create_cave(
        all_paths, min_x, max_x, min_y, max_y,
        hole_x=500, filling=False):

    cave = Cave(min_x, max_x, min_y, max_y, hole_x=hole_x, filling=filling)

    for path in all_paths:
        curr_x, curr_y = path[0]

        for next_x, next_y in path[1:]:
            cave.add_rock_segment(curr_x, curr_y, next_x, next_y)
            curr_x, curr_y = next_x, next_y

    return cave


def fill_cave_until_full(cave, hole_x=500):

    # Destructive!
    #
    # This isn't necessary for this task, but it's defensive programming
    #
    cave = copy.deepcopy(cave)

    counter = 0
    while cave.add_sand(hole_x, 0):
        counter += 1

    return counter


def main():

    all_paths, min_x, max_x, min_y, max_y = reader()

    cave1 = create_cave(all_paths, min_x, max_x, min_y, max_y, hole_x=500)
    cave2 = create_cave(
            all_paths, min_x, max_x, min_y, max_y,
            hole_x=500, filling=True)

    print('part 1: %d' % fill_cave_until_full(cave1))
    print('part 2: %d' % fill_cave_until_full(cave2))


main()

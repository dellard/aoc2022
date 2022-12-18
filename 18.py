#!/usr/bin/env python3

"""
Advent of Code 2022, day 18
"""

import re
import sys


def reader():

    points = []
    for line in sys.stdin:
        point = tuple([int(x) for x in re.findall(r'\d+', line)])

        points.append(point)

    return points


def total_unconnected(points):

    point_set = set(points)
    if len(point_set) != len(points):
        print('OOPS -- duplicate points')

    # if none of the cubes touch, then this
    # is the most exposed sides we can get
    #
    total_possible = len(points) * 6

    # print('most possible: ', total_possible)

    covered = 0
    for point in points:
        n_x = (point[0] + 1, point[1], point[2])
        if n_x in point_set:
            covered += 2

    for point in points:
        n_y = (point[0], point[1] + 1, point[2])
        if n_y in point_set:
            covered += 2

    for point in points:
        n_z = (point[0], point[1], point[2] + 1)
        if n_z in point_set:
            covered += 2

    return total_possible - covered


def find_voids(points):

    # Find the extents of the points.  We use
    # this to construct a rectangular volume
    # containing a filler shape which contains
    # everything in the volume *except* the points

    x_ord = sorted(points, key=lambda p: p[0])
    x_min, x_max = x_ord[0][0], x_ord[-1][0]

    y_ord = sorted(points, key=lambda p: p[1])
    y_min, y_max = y_ord[0][1], y_ord[-1][1]

    z_ord = sorted(points, key=lambda p: p[2])
    z_min, z_max = z_ord[0][2], z_ord[-1][2]

    point_set = set(points)

    # construct the filler
    #
    filler = set()
    for x in range(x_min - 1, x_max + 3, 1):
        for y in range(y_min - 1, y_max + 3, 1):
            for z in range(z_min - 1, z_max + 3, 1):
                if (x, y, z) not in point_set:
                    filler.add((x, y, z))

    """
    Now for the fun part:

    partition filler by removing every cube that
    is reachable from the outside of the enclosing
    volume.  This will leave just the voids, if
    there are any.

    1. make a to-do list of all of the "surface" cubes
        that are on the perimeter of the filler, and
        add each cube in the to-do list to the visited
        set

    2. While the to-do list isn't empty, pop the first
        cube off the to-do list, and then:

        a. add all of the adjacent cubes that aren't
            in the visited list and are within the filler
            shape, to the to-do list and the visited set

    3. Remove every cube in the visited set from the
        filler set

    4. What remains of the filler should be any voids.
        Find their surface areas, and subtract from them
        from the surface area of the original volume
    """

    # Step 1
    todo = []
    visited = set()

    for point in filler:
        x, y, z = point
        if ((x == x_min - 1 or x == x_max + 2)
                or (y == y_min - 1 or y == y_max + 2)
                or (z == z_min - 1 or z == z_max + 2)):
            todo.append(point)
            visited.add(point)

    # Step 2

    def explore(point):
        if point in filler and point not in visited:
            visited.add(point)
            todo.append(point)

    while todo:
        (x, y, z) = todo.pop(0)
        explore((x + 1, y, z))
        explore((x - 1, y, z))
        explore((x, y + 1, z))
        explore((x, y - 1, z))
        explore((x, y, z + 1))
        explore((x, y, z - 1))

    # Step 3

    for point in visited:
        filler.remove(point)

    void_surface = total_unconnected(list(filler))
    return void_surface


def main():

    points = reader()

    total_un = total_unconnected(points)
    print('part 1: ', total_un)

    void_surface = find_voids(points)
    print('part 2: ', total_un - void_surface)

if __name__ == '__main__':
    main()

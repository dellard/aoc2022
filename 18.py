#!/usr/bin/env python3

import re
import sys


def reader():

    points = []
    for line in sys.stdin:
        point = tuple([int(x) for x in re.findall(r'\d+', line)])

        points.append(point)

    return points


def scratch(points):

    f = set(points)
    if len(f) != len(points):
        print('OOPS -- duplicate points')

    # if none of the cubes touch, then this
    # is the most exposed sides we can get
    #
    total_possible = len(points) * 6

    print('most possible: ', total_possible)

    x_ord = sorted(points, key=lambda p: p[0])
    x_min = x_ord[0][0]
    x_max = x_ord[-1][0]

    y_ord = sorted(points, key=lambda p: p[1])
    y_min = y_ord[0][1]
    y_max = y_ord[-1][1]

    z_ord = sorted(points, key=lambda p: p[2])
    z_min = z_ord[0][2]
    z_max = z_ord[-1][2]

    print(x_ord)
    print(x_min, x_max)

    print(y_ord)
    print(y_min, y_max)

    print(z_ord)
    print(z_min, z_max)

    p_set = set(points)

    covered = 0
    for point in points:
        n_x = (point[0] + 1, point[1], point[2])
        if n_x in points:
            covered += 2

    for point in points:
        n_y = (point[0], point[1] + 1, point[2])
        if n_y in points:
            covered += 2

    for point in points:
        n_z = (point[0], point[1], point[2] + 1)
        if n_z in points:
            covered += 2

    return total_possible - covered



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


def main():

    points = reader()

    #total_un = total_unconnected([(1, 1, 1), (2, 1, 1)])
    #print(total_un)

    total_un = total_unconnected(points)
    print('part 1: ', total_un)


if __name__ == '__main__':
    main()

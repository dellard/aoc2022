#!/usr/bin/env python3

import re
import sys


def reader():

    rows = []
    for line in sys.stdin:

        tokens = [int(x) for x in re.findall(r'-*\d+', line)]
        extent = abs(tokens[0] - tokens[2]) + abs(tokens[1] - tokens[3])
        rows.append([(tokens[0], tokens[1]), (tokens[2], tokens[3]), extent])

    return rows


def find_range(sb_pairs):

    min_x, min_y = sb_pairs[0][0][0], sb_pairs[0][0][1]
    max_x, max_y = sb_pairs[0][0][0], sb_pairs[0][0][1]

    for sensor, beacon, extent in sb_pairs:
        # print('%s %s' % (str(sensor), str(min_x)))
        min_x = min(min_x, sensor[0] - extent, beacon[0])
        max_x = max(max_x, sensor[0] + extent, beacon[0])

        min_y = min(min_y, sensor[1] - extent, beacon[1])
        max_y = max(max_y, sensor[1] + extent, beacon[1])

    return (min_x, min_y), (max_x, max_y)


def find_row_cov(sb_pairs, min_pos, max_pos, row_n, inc_beacons=False):

    if row_n < min_pos[1] or row_n > max_pos[1]:
        # We're outside the box
        return []

    row = {}

    for sensor, beacon, extent in sb_pairs:
        projection = extent - abs(sensor[1] - row_n)
        if projection > 0:
            start_x = max(sensor[0] - projection, min_pos[0])
            end_x = min(1 + sensor[0] + projection, 1 + max_pos[0])

            for i in range(start_x, end_x, 1):
                if min_pos[0] <= i <= max_pos[0]:
                    row[i] = '#'

    # Now replace any actual beacons
    #
    # Not an effcient way to do this, alas
    #
    for sensor, beacon, extent in sb_pairs:
        if beacon[1] == row_n:
            row[beacon[0]] = 'B'

    offsets = []
    for ind, val in row.items():
        if inc_beacons or val == '#':
            offsets.append(ind)

    return offsets


def find_annulus(center_x, center_y, radius):

    if radius == 0:
        return [(center_x, center_y)]

    annulus = set()

    for i in range(radius):
        annulus.add((center_x + i, center_y - (radius - i)))
        annulus.add((center_x + radius - i, center_y + i))
        annulus.add((center_x - i, center_y + (radius - i)))
        annulus.add((center_x - (radius - i), center_y - i))

    return annulus


def distance(pos1, pos2):

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def find_uncovered(sb_info, min_x, min_y, max_x, max_y):

    annuli = []
    for center, _, ext in sb_info:
        annuli.append(find_annulus(center[0], center[1], ext + 1))

    candidates = set()
    for i in range(len(annuli) - 1):
        for j in range(i + 1, len(annuli), 1):
            candidates |= annuli[i] & annuli[j]

    for pos in candidates:
        if min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y:
            missed = True
            for center, _, ext in sb_info:
                if distance(center, pos) <= ext:
                    missed = False
                    break

            if missed:
                return pos

    return None


def main():

    sb_info = reader()

    min_pos, max_pos = find_range(sb_info)
    covered = find_row_cov(sb_info, min_pos, max_pos, 2000000)

    print('part 1: %d' % len(covered))

    uncovered = find_uncovered(sb_info, 0, 0, 4000000, 4000000)
    if uncovered:
        print('part 2: %d' % (uncovered[0] * 4000000 + uncovered[1]))
    else:
        print('part 2: DISASTER')


if __name__ == '__main__':
    main()

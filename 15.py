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

    new_rows = []
    for sensor, beacon, _ in sb_pairs:
        print('%s %s' % (str(sensor), str(min_x)))
        min_x = min(min_x, sensor[0], beacon[0])
        max_x = max(max_x, sensor[0], beacon[0])

        min_y = min(min_y, sensor[1], beacon[1])
        max_y = max(max_y, sensor[1], beacon[1])

    return (min_x, min_y), (max_x, max_y)


def find_row_cov(sb_pairs, min_pos, max_pos, row_n):

    min_x, max_x = min_pos[0], max_pos[0]
    row_len = 1 + max_x - min_x

    # lazy, may regret later...
    row = {}
    #for i in range(min_x, max_x + 1, 1):
    #    row[i] = '.'

    for sensor, beacon, extent in sb_pairs:
        projection = extent - abs(sensor[1] - row_n)
        if projection > 0:
            print('ADD ', sensor, beacon, extent)
            for i in range(sensor[0] - projection, 1 + sensor[0] + projection, 1):
                row[i] = '#'

            # print('R ' + ''.join([row[i] for i in range(min_x, max_x + 1, 1)]))

    # Now add the beacons back in
    for sensor, beacon, extent in sb_pairs:
        if beacon[1] == row_n:
            row[beacon[0]] = 'B'

    count = 0
    for ind, val in row.items():
        if val == '#':
            count += 1
        else:
            print('nah at %d' % ind)

    return count


def main():

    rows = reader()

    for row in rows:
        print(row)

    min_pos, max_pos = find_range(rows)

    print(find_row_cov(rows, min_pos, max_pos, 2000000))
    # print(min_pos, max_pos)


if __name__ == '__main__':
    main()



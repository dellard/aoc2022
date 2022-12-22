#!/usr/bin/env python3

import re
import sys


def reader():

    # Note that we always put an extra blank row
    # at the beginning, and an extra space at the
    # start of each row, so that we can use zero-based
    # coordinates (which Python likes) instead of
    # 1-based coordinates (which the puzzle uses)

    tiles = [' ']
    commands_next = False

    for line in sys.stdin:
        row = line.rstrip()

        if not row:
            # the next row is the commands
            commands_next = True
            continue

        if commands_next:
            magnitudes = [int(mag) for mag in re.findall('\d+', row)]
            directions = re.findall('[RL]', row)
            print(magnitudes)
            print(directions)

            break
        else:
            tiles.append(' ' + row + ' ')

    # fill in the top row, and add a bottom row
    # to make figuring out how to wrap easier
    # (hopefully)
    #
    maxlen = max([len(row) for row in tiles])
    tiles.append(' ' * maxlen)
    tiles[0] = ' ' * maxlen

    # find the start.  Note again that we are 1-based
    start = (tiles[1].index('.'), 0)

    return tiles, list(zip(magnitudes, directions)), start


def main():

    tiles, commands, start = reader()

    print(tiles)
    print(commands)
    print(start)

    # At this point, we could make a map of ALL of the
    # possible moves, i.e. (x, y, d) -> (x, y) means that
    # if you're in position (x, y) facing direction d
    # then your next position is (x, y), which would make
    # everything else easier, but I don't know if that's
    # necessary.
    # Something to consider.


if __name__ == '__main__':
    main()

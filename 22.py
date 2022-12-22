#!/usr/bin/env python3

import re
import sys


class Tiles:

    def __init__(self, rows, start):

        self.rows = rows
        self.start = start
        self.max_x = max([len(r) for r in rows])
        self.max_y = len(rows)

    def next_x(self, x, step):
        return (x + step) % self.max_x

    def next_y(self, y, step):
        return (y + step) % self.max_y

    def next_p(self, curr, delta):
        return (self.next_x(curr[0], delta[0]),
                self.next_y(curr[1], delta[1]))

    def turn(self, delta, direction):
        # So much typing

        # To make things easier at the end
        #
        if direction == 'S':
            return delta

        if delta == (1, 0):
            if direction == 'L':
                return (0, -1)
            else:
                return (0, 1)

        elif delta == (-1, 0):
            if direction == 'L':
                return (0, 1)
            else:
                return (0, -1)

        elif delta == (0, -1):
            if direction == 'L':
                return (-1, 0)
            else:
                return (1, 0)

        elif delta == (0, 1):
            if direction == 'L':
                return (1, 0)
            else:
                return (-1, 0)


def reader():

    # Note that we always put an extra blank row
    # at the beginning, and an extra space at the
    # start of each row, so that we can use zero-based
    # coordinates (which Python likes) instead of
    # 1-based coordinates (which the puzzle uses)

    rows = [' ']
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
            #print(magnitudes)
            #print(directions)

            break
        else:
            row = [str(c) for c in row]
            rows.append([' '] + row + [' '])

    # fill in the top row, and add a bottom row
    # to make figuring out how to wrap easier
    # (hopefully)
    #
    maxlen = max([len(row) for row in rows])
    rows.append([' '] * maxlen)
    rows[0] = [' '] * maxlen

    # pad all the rows to make the grid a full
    # rectangle.  This is the lazy way to make
    # later things easier.
    #
    max_row_len = max([len(r) for r in rows])
    rows = [r + [' '] * (max_row_len - len(r)) for r in rows]

    # find the start.  Note again that we are 1-based
    for i in range(len(rows[1])):
        if rows[1][i] == '.':
            start = (i, 1)
            break

    # what if we didn't find it?

    return rows, list(zip(magnitudes, directions + ['S'])), start


def move(tiles, pos, delta):

    p_x, p_y = pos

    print('pos ', pos)

    if tiles.rows[p_y][p_x] not in '.o<>^v':
        print('WHOOPS!  off the grid (%d, %d)' % (p_x, p_y))
        return pos

    next_x, next_y = tiles.next_p(pos, delta)
    if tiles.rows[next_y][next_x] in '.o<>^v':
        return next_x, next_y
    elif tiles.rows[next_y][next_x] == '#':
        return pos

    # I sure hope this loop isn't infinite.
    #
    while tiles.rows[next_y][next_x] == ' ':
        next_x, next_y = tiles.next_p((next_x, next_y), delta)

    if tiles.rows[next_y][next_x] == '#':
        return pos
    else:
        return (next_x, next_y)


def print_tiles(tiles):

    row = tiles.rows
    for row in tiles.rows:
        print('|', ''.join(row), '|')


def find_facing(delta):

    if delta == (1, 0):
        return 0, '>'
    elif delta == (0, 1):
        return 1, 'v'
    elif delta == (-1, 0):
        return 2, '<'
    elif delta == (0, -1):
        return 3, '^'


def navigate(tiles, commands):

    delta = (1, 0)
    curr = tiles.start

    tiles.rows[curr[1]][curr[0]] = 'o'
    print_tiles(tiles)

    for (count, turn) in commands:
        print('====')
        print('curr ', curr, ' delta ', delta)

        _, sym = find_facing(delta)
        tiles.rows[curr[1]][curr[0]] = sym

        for i in range(count):
            new = move(tiles, curr, delta)
            if tiles.rows[new[1]][new[0]] not in '.o<>^v':
                print('OOPS bad loc ', new)
                sys.exit(1)

            if new == curr:
                break
            curr = new

            tiles.rows[curr[1]][curr[0]] = sym

        delta = tiles.turn(delta, turn)
        print_tiles(tiles)

    facing, _ = find_facing(delta)
    return curr, facing


def main():

    rows, commands, start = reader()

    """
    for row in rows:
        print('|', row, '|')
    """

    tiles = Tiles(rows, start)
    # print_tiles(tiles)

    # At this point, we could make a map of ALL of the
    # possible moves, i.e. (x, y, d) -> (x, y) means that
    # if you're in position (x, y) facing direction d
    # then your next position is (x, y), which would make
    # everything else easier, but I don't know if that's
    # necessary.
    # Something to consider.

    print(start)
    print(commands)

    pos, facing = navigate(tiles, commands)
    print('part 1: ', pos[1] * 1000 + pos[0] * 4 + facing)



if __name__ == '__main__':
    main()

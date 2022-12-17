#!/usr/bin/env python3


import sys


class Chimney:

    ROCK_SHAPES = [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
            [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 0), (1, 0), (0, 1), (1, 1)]
        ]

    def __init__(self, puffs, width=7):

        self.height = 8 # does this matter?
        self.width = width
        self.puffs = puffs
        self.puff_ind = 0

        self.initial_x = 2
        self.initial_y = 3

        self.rocks = self.ROCK_SHAPES
        self.rock_ind = 0

        self.rock_grid = []
        for y in range(self.height):
            self.rock_grid.append(['.'] * self.width)

        self.curr_top = len(self.rock_grid)

    def draw(self):

        print('----')
        for y in range(self.curr_top - 1, -1, -1):
            print('y = ', y, ' ', ''.join(self.rock_grid[y]))
        print('++++')
        print(self.rock_grid)

    def apply_puff(self, rock, pos, puff):

        px, py = pos

        if puff == '<':
            dx = -1
        else:
            dx = 1

        rock_now = [(x + px + dx, y + py) for x, y in rock]
        print('rock_now ', rock_now)

        if min([p[0] for p in rock_now]) < 0:
            return pos
        elif max([p[0] for p in rock_now]) >= self.width:
            return pos

        for x, y in rock_now:
            print('looking at %d, %d' % (x, y))
            if self.rock_grid[y][x] != '.':
                return pos

        return px + dx, py

    def fall_one(self, rock, pos):

        px, py = pos

        rock_now = [(x + px, y + py - 1) for x, y in rock]

        if min([p[1] for p in rock_now]) < 0:
            return pos

        for x, y in rock_now:
            if self.rock_grid[y][x] != '.':
                return pos

        return px, py - 1

    def place(self, rock, pos, symbol='#'):

        px, py = pos

        print('rock ', rock)
        rock_now = [(x + px, y + py) for x, y in rock]
        print('rock_now ', rock_now)

        for x, y in rock_now:
            self.rock_grid[y][x] = symbol

    def drop(self):

        rock = self.ROCK_SHAPES[self.rock_ind]
        print('rock =', rock)

        self.rock_ind = (self.rock_ind + 1) % len(self.ROCK_SHAPES)

        rock_pos = (self.initial_x, self.initial_y)

        while True:
            self.draw()

            puff = self.puffs[self.puff_ind]
            self.puff_ind = (self.puff_ind + 1) % len(self.puffs)

            puff_pos = self.apply_puff(rock, rock_pos, puff)
            if puff_pos == rock_pos:
                print('could not move %s' % puff)
            down_pos = self.fall_one(rock, puff_pos)

            if down_pos == puff_pos:
                print('at rest')
                self.place(rock, puff_pos)
                break

            print('moving down')
            rock_pos = down_pos


def reader():

    puffs = sys.stdin.readline().strip()

    print(puffs)

    chimney = Chimney(puffs)

    return chimney


def main():

    chimney = reader()

    chimney.draw()
    chimney.drop()
    chimney.draw()


if __name__ == '__main__':
    main()

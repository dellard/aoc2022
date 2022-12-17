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

        self.height = 20 # does this matter?
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
            print(''.join(self.rock_grid[y]))
        print('++++')
        # print(self.rock_grid)

    def apply_puff(self, rock, pos, puff):

        px, py = pos

        if puff == '<':
            dx = -1
        else:
            dx = 1

        rock_now = [(x + px + dx, y + py) for x, y in rock]
        # print('rock_now ', rock_now)

        if min([p[0] for p in rock_now]) < 0:
            return pos
        elif max([p[0] for p in rock_now]) >= self.width:
            return pos

        for x, y in rock_now:
            # print('looking at %d, %d' % (x, y))
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

        # print('rock ', rock)
        rock_now = [(x + px, y + py) for x, y in rock]
        # print('rock_now ', rock_now)

        for x, y in rock_now:
            self.rock_grid[y][x] = symbol

    def find_max_height(self):

        for i in range(len(self.rock_grid) - 1, -1, -1):
            if '#' in self.rock_grid[i]:
                return i + 1

        return 0

    def drop(self):

        rock = self.ROCK_SHAPES[self.rock_ind]
        # print('rock =', rock)

        self.rock_ind = (self.rock_ind + 1) % len(self.ROCK_SHAPES)

        rock_pos = (self.initial_x, self.initial_y)

        while True:
            # self.draw()

            puff = self.puffs[self.puff_ind]
            self.puff_ind = (self.puff_ind + 1) % len(self.puffs)

            puff_pos = self.apply_puff(rock, rock_pos, puff)
            if puff_pos == rock_pos:
                #print('could not move %s' % puff)
                pass
            down_pos = self.fall_one(rock, puff_pos)

            if down_pos == puff_pos:
                # print('at rest')
                self.place(rock, puff_pos)
                break

            # print('moving down')
            rock_pos = down_pos

        new_height = self.find_max_height()
        # print('max height ', self.find_max_height())

        self.initial_y = new_height + 3

        if self.height < self.initial_y + 5:
            for _ in range(10):
                self.rock_grid.append(['.'] * self.width)

            self.height = len(self.rock_grid)


def reader():

    puffs = sys.stdin.readline().strip()

    return puffs


def part1(puffs, cnt=2022):

    chimney = Chimney(puffs)

    for i in range(cnt):
        chimney.drop()
        if chimney.puff_ind == 0:
            print('here %d' % i)
        # chimney.draw()

    print('part 1: %d' % chimney.find_max_height())


def part2(puffs, cnt=2022):

    prelim_iters, iters_per_loop, height_per_loop = recon(puffs)


    # how many rocks it takes to get into the loop
    #
    # if cnt is less than prelim_iters, oops
    #

    # for the test
    #prelim_iters = 57
    #iters_per_loop = 35
    #height_per_loop = 53

    # for the eval
    #prelim_iters = 3429
    #iters_per_loop = 1715
    #height_per_loop = 2616

    # create a chimney and drop the first
    # prelim_iters rocks into it, to get
    # things set up
    #
    chimney = Chimney(puffs)
    for i in range(prelim_iters):
        chimney.drop()

    curr_height = chimney.find_max_height()

    elided_loops = (cnt - prelim_iters) // iters_per_loop

    remaining_rocks = (cnt - prelim_iters) % iters_per_loop

    # Drop the leftover rocks, and find the resulting height
    for i in range(remaining_rocks):
        chimney.drop()

    curr_height = chimney.find_max_height()

    total_height = curr_height + (elided_loops * height_per_loop)

    print('part 2: %d' % total_height)


def recon(puffs, n_iters=20000):
    """
    find the periodicity of the behavior of the
    falling rocks
    """

    # n_iters is the maximum number of iterations
    # we'll use to test for a loop.  We want this
    # to be as small as possible, so everything
    # runs faster, but we could also make this
    # dynamic, with a little work.  For the puzzle
    # input, 20,000 is (quite a bit) more than
    # adequate.

    chimney = Chimney(puffs)

    # What we're going to do is consider the top
    # of the stack when the offset into the puffs
    # is small: starting at 1, and going to 20.
    # Since there's a small limit to how many puffs
    # a rock can encounter before settling, we know
    # that eventually this will happen.
    #
    # We start at 1, instead of 0, in order to avoid
    # an edge case (the very first rock, might not
    # be part of a loop).
    #
    # It would be more efficient to check all the
    # offsets in one pass, but this is Good Enough
    # because the loops (for the puzzle input)
    # are reasonably easy to find.
    #
    for offset in range(1, 20, 1):

        # Start the chimney from scratch each time
        #
        chimney = Chimney(puffs)

        state = []
        prev_i = 0
        prev_h = 0

        prev_state = []
        prev_span_i = 0
        prev_span_h = 0

        for i in range(n_iters):
            chimney.drop()

            if chimney.puff_ind == offset:
                height = chimney.find_max_height()

                state.append((chimney.puff_ind, chimney.rock_ind))
                span_i = i - prev_i
                span_h = height - prev_h

                # See whether everything looks like it looked
                # the last time we were at this offset, and if
                # so, then return the number of rocks we had
                # to drop to get into the loop (i - span_i),
                # the number of rocks in the loop (span_i),
                # and the height each loop adds to the pile
                # (span_h)
                #
                # Note that we don't realize that we're in
                # the loop until we have completed it, so
                # that's why we use (i - span_i) instead of
                # just using i.  We could also use i, but
                # (i - span_i) reduces the number of rocks
                # we needlessly drop later.
                #
                # NOTE: it's possible my heuristic is too
                # weak: I don't actually check the pile
                # to see if the top span_h rows are the
                # same as the previous.  That would be easy
                # to add, but I've got other things to do
                # with my weekend.
                #
                if prev_span_h == span_h and prev_span_i == span_i:
                    if state == prev_state:
                        #print('Got 1 at %d span %d spanh %d' %
                        #      (i, span_i, span_h))
                        return i - span_i, span_i, span_h

                        #print('Got 1 at %d span %d spanh %d - %s' %
                        #      (i, span_i, span_h,
                        #       ', '.join([str(o) for o in state])))

                prev_state = state
                prev_i = i
                prev_h = height

                prev_span_i = span_i
                prev_span_h = span_h
                prev_state = state

    print('OOPS: try making n_iters larger!')
    sys.exit(1)


def main():

    puffs = reader()

    part1(puffs, cnt=2022)
    part2(puffs, cnt=1000000000000)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3


import re
import sys


def reader():

    rows = []
    for line in sys.stdin:
        line = line.strip()

        rows.append(line)

    # find the entrance and exit
    entr_x = rows[0].index('.') - 1
    exit_x = rows[-1].index('.') - 1

    # Don't count the borders?
    rows.pop(0)
    rows.pop()

    rows = [re.sub('#', '', row) for row in rows]

    # Assume that the valley is rectangular
    n_rows = len(rows)
    n_cols = len(rows[0])

    # find all the blizzards
    #
    blizzards = set()

    for p_y in range(n_rows):
        for p_x in range(n_cols):
            if rows[p_y][p_x] in '><^v':
                blizzards.add(
                        Blizzard(p_x, p_y, rows[p_y][p_x], n_rows, n_cols))

    return Valley(blizzards, n_rows, n_cols, (entr_x, -1)), entr_x, exit_x


class Valley:

    def __init__(self, blizzards, n_rows, n_cols, entrance):

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.entrance = entrance

        print('n_rows %d n_cols %d' % (n_rows, n_cols))

        # Make lists, for each row and each column,
        # of just the blizzards that move along that
        # row or column.  This will make it a lot
        # easier to check a given position, because
        # only the blizzards that move through that
        # position need to be considered.  No need
        # to reconstruct the entire valley at each
        # step along the way.
        #
        row_blizzards = [[]] * n_rows
        col_blizzards = [[]] * n_cols
        print(row_blizzards)
        print(col_blizzards)

        for bliz in blizzards:
            if bliz.direction in '<>':
                print(bliz.pos)
                row_blizzards[bliz.pos[1]].append(bliz)
            else:
                print(bliz.pos)
                col_blizzards[bliz.pos[0]].append(bliz)

        self.row_blizzards = row_blizzards
        self.col_blizzards = col_blizzards

        # That was the old way of managing the blizzards.
        # We need a faster way.

    def pos_ok(self, pos, minute):

        if pos == self.entrance:
            return True

        p_x, p_y = pos

        if p_x < 0 or p_x >= self.n_cols or p_y < 0 or p_y >= self.n_rows:
            return False

        for bliz in self.row_blizzards[p_y]:
            if bliz.where_n(minute) == pos:
                return False

        for bliz in self.col_blizzards[p_x]:
            if bliz.where_n(minute) == pos:
                return False

        return True


class Blizzard:

    def __init__(self, p_x, p_y, direction, n_rows, n_cols):

        self.pos = p_x, p_y
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.direction = direction

        if direction == '^':
            self.delta = (0, -1)
        elif direction == 'v':
            self.delta = (0, 1)
        elif direction == '<':
            self.delta = (-1, 0)
        elif direction == '>':
            self.delta = (1, 0)
        else:
            print('OOPS')

    def move_one(self):
        # Not sure if this is useful

        self.pos = ((self.pos[0] + self.delta[0]) % self.n_cols,
                    (self.pos[1] + self.delta[1]) % self.n_rows)

    def where_n(self, n_mins):
        """
        Where will this storm be n_mins after the start?
        """

        return ((self.pos[0] + (n_mins * self.delta[0])) % self.n_cols,
                (self.pos[1] + (n_mins * self.delta[1])) % self.n_rows)


def print_valley(bliz, minute, n_rows, n_cols, p_x, p_y):
    pass


def part1_search(valley, start_pos, end_pos, start_minute=0):

    # Note: although the instructions don't seem to mention
    # it, there are never any vertical blizzards on the entrance
    # and exit columns.  So you could just wait in the entrance
    # forever, although that doesn't seem helpful.
    #
    # Our real goal is to reach the position above the exit safely.
    # From there it's just one more minute to the exit.

    queue = []
    seen = set()

    queue.append((start_pos, start_minute))

    while queue:
        pos, minute = queue.pop(0)

        p_x, p_y = pos

        # Oops; we shouldn't be here at all
        if not valley.pos_ok(pos, minute):
            print('oops')
            continue

        # no fair tunneling along the border
        #
        if p_y == -1 and p_x != start_pos[0]:
            continue
        if p_y == valley.n_rows and p_x != start_pos[0]:
            continue

        #print('trying pos %s minute %d' % (pos, minute))
        #print('queue length %d' % len(queue))

        if pos == end_pos:
            # hooray.  We're out.
            return minute + 1

        if p_x > 0 and valley.pos_ok((p_x - 1, p_y), minute + 1):
            cand = ((p_x - 1, p_y), minute + 1)
            if cand not in seen:
                seen.add(cand)
                queue.append(cand)

        if p_x + 1 < valley.n_cols and valley.pos_ok((p_x + 1, p_y), minute + 1):
            cand = ((p_x + 1, p_y), minute + 1)
            if cand not in seen:
                seen.add(cand)
                queue.append(cand)

        if p_y > 0 and valley.pos_ok((p_x, p_y - 1), minute + 1):
            cand = ((p_x, p_y - 1), minute + 1)
            if cand not in seen:
                seen.add(cand)
                queue.append(cand)

        if p_y + 1 < valley.n_rows and valley.pos_ok((p_x, p_y + 1), minute + 1):
            cand = ((p_x, p_y + 1), minute + 1)
            if cand not in seen:
                seen.add(cand)
                queue.append(cand)

        # Hang out here and wait for things to blow over.
        if valley.pos_ok((p_x, p_y), minute + 1):
            cand = ((p_x, p_y), minute + 1)
            if cand not in seen:
                seen.add(cand)
                queue.append(cand)

        #print('---- ----')

    print('SEARCH FAILED!')


def main():

    valley, entr_x, exit_x = reader()
    minutes0 = part1_search(
            valley, (entr_x, -1), (exit_x, valley.n_rows - 1),
            start_minute=0))
    print('part 1: ', minutes0)

    valley.entrance = (exit_x, valley.n_rows)
    minutes1 = part1_search(
            valley, (exit_x, valley.n_rows), (entr_x, 0),
            start_minute=minutes0)
    print('after minutes1 ', minutes1)

    valley.entrance = (entr_x, -1)
    minutes2 = part1_search(
            valley, (entr_x, -1), (exit_x, valley.n_rows - 1),
            start_minute=minutes1)
    print('after minutes2 ', minutes2)

    total = minutes2
    print('part 2: ', minutes2)


if __name__ == '__main__':
    main()




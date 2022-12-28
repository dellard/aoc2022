#!/usr/bin/env python3

"""
Day 15 of the 2022 Advent of Code

Some comments about the algorithms here -- and things
I tried and abandoned.

This solution (particularly for part 2) doesn't satisfy
the requirement that the solutions run in a few seconds,
even on old and obsolete machines.  I've got a pretty
beefy i9, and it takes about 90-100 seconds to run through
both tests, and there's no obvious tricks to chop this
down by an order of magnitude without having a better
algorithm, and I don't have one.  But here's what I
was thinking about, followed by what I did.

The problem for part 2 is that you can't just build the
grid and color in all the spaces, unless you're willing
to wait a week for it to finish running.  So, we need to
prune the search space as aggressively as possible, without
losing any info.  What I attempted to do is to decrease
the "resolution" of the cave "grid", i.e instead of having
a 4M x 4M grid, have an N x N grid, where N is a tractable
number like 500.  (Ideally N should divide 4M, to keep the
arithmetic simple, but that's not strictly necessary, if
you're careful.)  So if N is 500, then each grid element
represents an 8000 x 8000 element of the original grid.
Then we can scale down the coordinates for the sensors
and beacons correspondingly, doing the rounding carefully.
If a grid element from the N x N grid is entirely covered,
(or entirely uncovered) then the corresponding 8k x 8k
grid element is also covered (or uncovered), and we don't
have to consider it again.  If the grid element from the
N x N grid is partially covered, then we need to drill down
closer, etc.  But the hope is that large parts of the
original grid would be quickly categorized.

It sort of worked.  It worked for the small test case,
and a few other contrived examples.  It doesn't seem like
a completely hopeless idea, but it had two significant
problems:

    1. Getting the scaling right is hard.  Lots of
        detail that has to be perfect.  Not the kind
        of code I can write in a hurry.  I don't
        think I got it right.

    2. Although it did prune down the search space,
        it didn't prune it down *enough*.  There
        were a lot of elements that needed to be
        examined closely because they contained a
        "border" between covered and uncovered
        regions.  It cut down the search space
        by two orders of magnitude, more or less,
        but I needed a lot more than that.  It would
        take less hour or so to run, perhaps -- but
        I never let it get very far before I
        gave up on it.

So, I abandoned this approach.  Note that this
approach solves a more general problem than the
one required by the task for today.  It finds
*all* of the uncovered spots in a given region,
however many there might turn out to be.  In some
context, that might be necessary, but for this
task, it ignores a very useful clue: for this
task, there is guaranteed to be exactly ONE
uncovered element in the region.

Since we know that there's only one, that contrains
its location a lot.  We know it can't be inside
the area covered by a sensor -- but it must be
immediately adjacent to two such areas, or squeezed
between one sensor area and the border of the region
itself.  Similar to the illustration from the
task if we have an area as shown below, then the
open spot can only possibly be one of the X
positions:

           X
          X#X
         X##BX
        X##S##X
         X###X
          X#X
           X


So, for each sensor, compute the annulus of
the spaces bordering the coverage area (the
positions marked with X here).  Then find
all of the spots that are in the intersection
of one or more annuli, or along the border.
[Note: I omitted this last test, because it
never came up, due to the "only one" rule,
which constrains where that one can be to a
very small number of cases, which I'll leave
as an exercise for the reader.  (hint... corners)

Now you have a complete list of all of the
areas that *might* be uncovered.  For my test
data, this decreased the search space from
4M x 4M to about 4.5M, which is a big help.
Then we just have to scan through the remaining
4.5M elements and find the first that's uncovered,
and we can prune these back a bit as well.

I'm certain that I'm missing some method that
would make this much faster, but I don't know
what it is.

"""

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


def find_annulus(
        sb_info,
        center_x, center_y, radius,
        min_x, min_y, max_x, max_y):
    """
    This is a lot more complicated than it needs to be,
    because I'm trying to prune the canidates as much
    as possible.  It's not very successful, however.

    What this function does is return the annulus around
    a given center at the given radius.  To reduce the
    search space a bit, it ignores any points that are
    outside the min/max bounding box.

    As a second optimization, it omits any of the
    segments of the annulus that are completely inside
    one of the other sensor detection areas.  This doesn't
    help all that much either.
    """

    if radius == 0:
        return [(center_x, center_y)]

    top = (center_x, center_y - radius)
    right = (center_x + radius, center_y)
    bottom = (center_x, center_y + radius)
    left = (center_x - radius, center_y)

    do_top_right = 1
    do_right_bottom = 1
    do_bottom_left = 1
    do_left_top = 1

    for center, _, ext in sb_info:
        if distance(top, center) <= ext and distance(right, center) <= ext:
            do_top_right = 0

        if distance(right, center) <= ext and distance(bottom, center) <= ext:
            do_right_bottom = 0

        if distance(bottom, center) <= ext and distance(left, center) <= ext:
            do_bottom_left = 0

        if distance(left, center) <= ext and distance(top, center) <= ext:
            do_left_top = 0

    # print('sides: %d' % (do_top_right + do_right_bottom + do_bottom_left + do_left_top))

    annulus = set()

    if do_top_right:
        for i in range(radius):
            point = (center_x + i, center_y - (radius - i))
            if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
                annulus.add(point)

    if do_right_bottom:
        for i in range(radius):
            point = (center_x + radius - i, center_y + i)
            if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
                annulus.add(point)

    if do_bottom_left:
        for i in range(radius):
            point = (center_x - i, center_y + (radius - i))
            if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
                annulus.add(point)

    if do_left_top:
        for i in range(radius):
            point = (center_x - (radius - i), center_y - i)
            if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
                annulus.add(point)

    return annulus


def distance(pos1, pos2):

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def find_uncovered(sb_info, min_x, min_y, max_x, max_y):

    # find all the annuli
    annuli = []
    for center, _, ext in sb_info:
        annuli.append(
                find_annulus(
                    sb_info,
                    center[0], center[1], ext + 1,
                    min_x, min_y, max_x, max_y))
        # print('annulus %d' % len(annuli[-1]))

    # find all the candidate positions that are in
    # the intersections of two annuli
    #
    candidates = set()
    for i in range(len(annuli) - 1):
        for j in range(i + 1, len(annuli), 1):
            candidates |= annuli[i] & annuli[j]

    # for each candidate pos, see whether it is uncovered
    #
    for pos in candidates:
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

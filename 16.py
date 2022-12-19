#!/usr/bin/env python3

import copy
import re
import sys

class CaveMap:

    def __init__(self, valves, root_name='AA'):

        self.valves = valves

        # This is badly named; it's not all the paths,
        # just a shortest path between the pairs of
        # valves that work (have rate > 0), and between
        # the root node and each of the valves that work
        #
        self.paths, self.distances = self.find_paths(root_name=root_name)

    def find_paths(self, root_name='AA'):

        paths = {}
        distances = {}
        working_valves = [name for name, val in self.valves.items()
                          if val.rate > 0]

        for start in working_valves:
            paths[start] = []

            for end in working_valves:
                if start != end:
                    dist = self._shortest_plen(start, end)
                    paths[start].append((end, dist))
                    distances[(start, end)] = dist

        if root_name not in paths:
            paths[root_name] = []
            for end in working_valves:
                dist = self._shortest_plen(root_name, end)
                paths[root_name].append((end, dist))
                distances[(root_name, end)] = dist

        return paths, distances

    def _shortest_plen(self, s_name, e_name):

        # I'm certain I was supposed to learn this in class.
        # Or maybe teach this in class.
        #
        # But I'm just going to blunder through it.

        reached = set([s_name])

        states = [[s_name]]

        while states and e_name not in reached:
            path = states.pop(0)

            last_name = path[-1]
            for name, distance in self.valves[last_name].neighbors:
                if name == e_name:
                    return len(path)
                elif name not in reached:
                    states.append(path + [name])
                    reached.add(name)
                else:
                    continue

        print('OOPS: unreachable?')
        return -1


class Valve:

    def __init__(self, name, vrate, neighbors):

        self.name = name
        self.rate = vrate
        self.neighbors = [(n, 1) for n in neighbors]
        self.closed = True

    def __repr__(self):
        return 'name %s rate %d closed %s neighbors %s' % (
                self.name, self.rate, self.closed, self.neighbors)


def reader():

    valves = {}

    for line in sys.stdin:
        tokens = line.strip().split()

        vname = tokens[1]
        vrate = int(re.findall(r'-*\d+', tokens[4])[0])
        vleads = [re.sub(',', '', lead.strip()) for lead in tokens[9:]]

        valves[vname] = Valve(vname, vrate, vleads)

    return valves


def extend1(cave, node, path, current_total, minutes):

    """
    if minutes < 5:
        spacer = ' ' * (30 - minutes)
        print('x%s%s flow %d mins %d %s' %
              (spacer, node, current_total, minutes, str(path)))
    """

    if minutes < 0:
        print('x WHOA')
        return current_total, path

    if minutes <= 0:
        return current_total, path

    # If we don't open any more valves, then this is
    # how much will flow during the remaining minutes
    #
    base_total = current_total
    highest_total = base_total
    highest_path = path

    neighbors = cave.paths[node]
    for neighbor, distance in neighbors:

        # If the neighbor is too far away to open
        # in time, then don't bother
        #
        if distance >= minutes:
            continue

        # If the neighbor is already on our path,
        # then we can't open it again
        # (we might pass through it on our way to
        # another node, but that's already accounted
        # for in the distance of the paths)
        #
        if neighbor in path:
            continue

        added_rate = cave.valves[neighbor].rate
        added_flow = added_rate * ((minutes - 1) - distance)
        # print('added flow %d rate %d' % (added_flow, added_rate))

        new_total, new_path = extend1(
                cave, neighbor, path + [neighbor],
                current_total + added_flow, (minutes - 1) - distance)

        if highest_total <= new_total:
            highest_total, highest_path = new_total, new_path
            # print('TOTAL %d FOR %s' % (highest_total, new_path))

    return highest_total, highest_path


def solver_pt1(cave, start='AA', minutes=30):

    # Examine every path through valves that can be traversed,
    # including the time required to open the valve, in the
    # time alloted, and then evaluate the total flow that
    # would result, and see whether it is better than the
    # highest flow we've found so far
    #
    # This might blow up for the big cases.  We'll see.

    highest_flow, highest_path = extend1(cave, start, [start], 0, minutes)
    return highest_flow, highest_path


def extend2(cave, node0, dist0, node1, dist1, path, current_total, minutes, hist):

    print('HIST %s' % str(hist))

    print('me %s dist %d ele %s dist %d total %d minutes %d %s %s'
          % (node0, dist0, node1, dist1, current_total, minutes,
             str(path), str(hist)))

    if minutes < 0:
        print('OOPS: not expected 0')
        return current_total, path, hist + [-1]

    if minutes == 0:
        print('ALL OUT ZERO %s %s' % (node0, node1))
        return current_total, path, hist + [-2]

    if len(path) == len(cave.paths):
        print('ALL OUT PREAMBLE %s %s' % (node0, node1))
        return current_total, path, hist + [-3]

    # If we don't open any more valves, then this is
    # how much will flow during the remaining minutes
    #
    base_total = current_total

    highest_total = base_total
    highest_path = path
    highest_hist = hist
    
    print('dist0 %d dist1 %d' % (dist0, dist1))

    if dist0 == 0 and dist1 == 0:
        print('CASE 0 0')

        unseen_pairs = set()
        unseen_nodes = []

        for n1 in cave.paths.keys():
            if n1 in path:
                continue

            unseen_nodes.append(n1)

            for n2 in cave.paths.keys():
                if n2 in path:
                    continue

                if n1 == n2:
                    continue

                unseen_pairs.add((n1, n2))

        if len(unseen_pairs) == 0:
            if len(unseen_nodes) != 1:
                print('OOPS what?')
            print('DOING THE SPECIAL CASE')

            new_n0 = unseen_nodes[0]

            # if there's only one valve left to open, then
            # figure out who is closer, and close it accordingly,
            # and then return.  There's nothing more to try
            #
            new_d0 = min(cave.distances[(node0, new_n0)],
                         cave.distances[(node1, new_n0)])
            if new_d0 >= minutes:
                print('OOPS RAN OUT OF MINUTES')

            increase = cave.valves[new_n0].rate * (minutes - (new_d0 + 1))
            s_highest, s_path = extend1(
                    cave, new_n0, path, current_total + increase, minutes - (new_d0 + 1))
            print('Returning %d' % s_highest)
            return s_highest, s_path, hist + [('S', new_n0, increase, minutes - 1)]

        for new_n0, new_n1 in unseen_pairs:

            new_d0 = cave.distances[(node0, new_n0)]
            new_d1 = cave.distances[(node1, new_n1)]

            if new_d0 >= minutes and new_d1 >= minutes:
                # if we can't get to either new_n0 or new_n1,
                # then we can't do anything with them
                continue

            # TODO: not sure about this case.  Hopefully
            # these will be scooped up in some other pair
            #
            if new_d0 >= minutes or new_d1 >= minutes:
                continue
            
            # To break symmetry, we ignore the case where
            # new_d0 is greater than new_d1.  We'll get a
            # chance to process these reflection of this
            # pair
            #
            if new_d0 > new_d1:
                continue

            warp = min(new_d0, new_d1)

            print('X0 node0 %s dist0 %d node1 %s dist1 %d warp %d'
                  % (new_n0, new_d0, new_n1, new_d1, warp))

            increase = (
                    cave.valves[new_n0].rate * (minutes - (new_d0 + 1)) +
                    cave.valves[new_n1].rate * (minutes - (new_d1 + 1)))
            new_total = base_total + increase

            ext_total, ext_path, ext_hist = extend2(
                    cave,
                    new_n0, new_d0 - warp,
                    new_n1, new_d1 - warp,
                    path + [new_n0, new_n1],
                    new_total,
                    minutes - (1 + warp),
                    hist + [('T', (new_n0, new_n1), increase, minutes - 1)])
                    #minutes - (warp + 1))

            if highest_total < ext_total:
                highest_total, highest_path, highest_hist = ext_total, ext_path, ext_hist
                print('NEW BEST HIST %d %s' % (highest_total, str(ext_hist)))

    elif dist0 > 0 or dist1 > 0:

        # reorder things so that name0/dist0 is always the zero
        #
        if dist1 == 0:
            print('REORDER')
            node0, node1 = node1, node0
            dist0, dist1 = dist1, dist0

        print('CASE X 0')

        neighbors = cave.paths[node0]
        for new_neighbor, new_distance in neighbors:
            # If the neighbor is too far away to open
            # in time, then don't bother
            #
            if new_distance >= minutes:
                continue

            # If the neighbor is already on our path,
            # then we can't open it again
            # (we might pass through it on our way to
            # another node, but that's already accounted
            # for in the distance of the paths)
            #
            if new_neighbor in path:
                continue

            #warp = min(new_distance + 1, dist1)
            warp = min(new_distance, dist1)

            print('X1 node0 %s dist0 %d node1 %s dist1 %d warp %d %s'
                  % (new_neighbor, new_distance, node1, dist1, warp, str(hist)))

            increase = cave.valves[new_neighbor].rate * (minutes - (new_distance + 1))
            new_total = base_total + increase

            # TODO: I think there's a bug in how many minutes we subtract.
            # There's a hidden extra 1 in the distance to a new node,
            # but it should only be added once.
            #
            ext_total, ext_path, ext_hist = extend2(
                    cave,
                    new_neighbor, new_distance - warp,
                    node1, dist1 - warp,
                    path + [new_neighbor],
                    new_total,
                    minutes - (1 + warp),
                    hist + [('O', new_neighbor, increase, minutes - 1)])
                    # minutes - (warp + 1))

            if highest_total < ext_total:
                highest_total, highest_path, highest_ext = ext_total, ext_path, ext_hist
                print('NEW BEST HIST %d %s' % (highest_total, str(ext_hist)))

    # This shouldn't happen, if we're doing things correctly.
    #
    if dist0 > 0 and dist1 > 0:
        print('OOPS CASE X X')
        ext_total, ext_path, ext_hist = extend2(
                cave,
                node0, dist0 - 1,
                node1, dist1 - 1,
                path,
                current_total,
                minutes - 1,
                hist)

        if highest_total < ext_total:
            highest_total, highest_path, highest_hist = ext_total, ext_path, ext_hist
            print('NEW BEST HIST %d %s' % (highest_total, str(ext_hist)))

    return highest_total, highest_path, highest_hist


def solver_pt2(cave, start='AA', minutes=26):

    highest_flow, highest_path, highest_hist = extend2(
            cave, start, 0, start, 0, [start], 0, minutes, [])
    return highest_flow, highest_path, highest_hist


def main():

    valves = reader()
    cm = CaveMap(valves)

    """
    for vname in sorted(valves.keys()):
        print(valves[vname])
    """

    for elem in cm.paths:
        related = ', '.join(['%s/d%d/r%d' % (v[0], v[1], valves[v[0]].rate) for v in cm.paths[elem]])
        #print('node ', elem, ' ', str(cm.paths[elem]))
        print('node ', elem, ' ', related)

    flow, path = solver_pt1(cm, start='AA', minutes=30)
    print('part 1 ', flow)
    #print('part 1 path ', path)

    flow, path, hist = solver_pt2(cm, start='AA', minutes=26)
    print('part 2 ', flow)
    print('part 2 path ', path)
    print('part 2 hist ', hist)


if __name__ == '__main__':
    main()

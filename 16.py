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
        self.paths = self.find_paths(root_name=root_name)

    def find_paths(self, root_name='AA'):

        paths = {}
        working_valves = [name for name, val in self.valves.items()
                          if val.rate > 0]

        for start in working_valves:
            paths[start] = []

            for end in working_valves:
                if start != end:
                    paths[start].append(
                            (end, self._shortest_plen(start, end)))

        if root_name not in paths:
            paths[root_name] = []
            for end in working_valves:
                paths[root_name].append(
                        (end, self._shortest_plen(root_name, end)))

        return paths

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


def extend2(cave, node0, dist0, node1, dist1, path, current_total, minutes):

    print('me %s dist %d ele %s dist %d total %d minutes %d %s'
          % (node0, dist0, node1, dist1, current_total, minutes,
             str(path)))

    if minutes < 0:
        return current_total, path

    if minutes == 0:
        return current_total, path

    if len(path) == len(cave.paths):
        print('ALL OUT PREAMBLE')
        return current_total, path

    # If we don't open any more valves, then this is
    # how much will flow during the remaining minutes
    #
    base_total = current_total
    highest_total = base_total
    highest_path = path
    
    print('dist0 %d dist1 %d' % (dist0, dist1))

    if dist0 == 0 and dist1 == 0:
        print('CASE 0 0')
        increase = cave.valves[node0].rate + cave.valves[node1].rate
        new_total = base_total + (increase * (minutes - 1))

        if len(path) == len(cave.paths):
            print('ALL OUT 0 0')
            return new_total, path

        for new_n0, new_d0 in cave.paths[node0]:
            if new_d0 >= minutes:
                continue
            if new_n0 in path:
                continue

            for new_n1, new_d1 in cave.paths[node1]:
                if new_n1 == new_n0:
                    continue

                # symmetry breaking: no need to consider
                # when the elephant and I cross routes
                #
                if new_n1 < new_n0:
                    continue

                if new_d1 >= minutes:
                    continue
                if new_n1 in path:
                    continue

                if new_d0 > new_d1:
                    new_n0, new_n1 = new_n1, new_n0
                    new_d0, new_d1 = new_d1, new_d0

                warp = min(new_d0 + 1, new_d1 + 1)

                ext_total, ext_path = extend2(
                        cave,
                        new_n0, new_d0 - warp,
                        new_n1, new_d1 - warp,
                        path + [new_n0, new_n1],
                        new_total,
                        minutes - warp)
                        #minutes - (warp + 1))

                if highest_total < ext_total:
                    highest_total, highest_path = ext_total, ext_path

    if dist0 == 0 or dist1 == 0:

        # reorder things so that name0/dist0 is always the zero
        #
        if dist1 == 0:
            print('REORDER')
            node0, node1 = node1, node0
            dist0, dist1 = dist1, dist0

        print('CASE X 0')
        increase = cave.valves[node0].rate
        new_total = base_total + (increase * (minutes - 1))

        if len(path) == len(cave.paths):
            print('ALL OUT 0 X')
            return new_total, path

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
            warp = min(new_distance + 1, dist1)
            ext_total, ext_path = extend2(
                    cave,
                    new_neighbor, new_distance - warp,
                    node1, dist1 - warp,
                    path + [new_neighbor],
                    new_total,
                    minutes - warp)
                    # minutes - (warp + 1))

            if highest_total < ext_total:
                highest_total, highest_path = ext_total, ext_path

    # This shouldn't happen, if we're doing things correctly.
    #
    if dist0 > 0 and dist1 > 0:
        print('OOPS CASE X X')
        ext_total, ext_path = extend2(
                cave,
                node0, dist0 - 1,
                node1, dist1 - 1,
                path,
                current_total,
                minutes - 1)

        if highest_total < ext_total:
            highest_total, highest_path = ext_total, ext_path

    return highest_total, highest_path


def solver_pt2(cave, start='AA', minutes=30):

    highest_flow, highest_path = extend2(
            cave, start, 0, start, 0, [start], 0, minutes)
    return highest_flow, highest_path


def main():

    valves = reader()
    cm = CaveMap(valves)

    """
    for vname in sorted(valves.keys()):
        print(valves[vname])
    """

    """
    for elem in cm.paths:
        related = ', '.join(['%s/d%d/r%d' % (v[0], v[1], valves[v[0]].rate) for v in cm.paths[elem]])
        #print('node ', elem, ' ', str(cm.paths[elem]))
        print('node ', elem, ' ', related)
    """

    flow, path = solver_pt1(cm, start='AA', minutes=30)
    print('part 1 ', flow)
    #print('part 1 path ', path)

    flow, path = solver_pt2(cm, start='AA', minutes=26)
    print('part 2 ', flow)
    #print('part 2 path ', path)


if __name__ == '__main__':
    main()

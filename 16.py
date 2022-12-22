#!/usr/bin/env python3

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


def extend_2a(
        cave, node0, dist0, node1, dist1,
        visited, current_total, minutes,
        scores):

    #spacer = ' ' * (30 - minutes)
    #
    #print('x%s min %d node0 %s dist0 %d node1 %s dist1 %d total %d %s' %
    #      (spacer, minutes, node0, dist0, node1, dist1, current_total, str(visited)))

    if minutes <= 0:
        return current_total, visited

    # If we don't open any more valves, then this is
    # how much will flow during the remaining minutes
    #
    base_total = current_total
    highest_total = base_total
    highest_path = visited

    # heuristic: consider the current set of visited nodes,
    # along with node0 and node1.  If we've gotten a higher
    # score for this state, then there's no point in
    # continuing this search -- we already found a better
    # solution elsewhere.
    #
    state = '.'.join(sorted(visited)) + '/' + '.'.join(sorted([node0, node1]))
    # state = (tuple(sorted(visited)), tuple(sorted([node0, node1])))
    if state not in scores:
        scores[state] = current_total
    else:
        if current_total < scores[state]:
            # print('ABANDONING at %d' % minutes)
            return current_total, visited
        else:
            scores[state] = current_total

    if dist0 == 0:
        for neighbor, distance in cave.paths[node0]:
            if distance >= minutes:
                continue
            if neighbor in visited:
                continue

            # OK, we've picked a valve to visit, now
            # that we're finished with node0.
            #
            # It will take us distance minutes to walk there,
            # plus another minute to open it, and then
            # after that it will flow at its rate until
            # we run out of minutes.

            added_rate = cave.valves[neighbor].rate
            added_flow = added_rate * (minutes - (distance + 1))

            # At some time in the future, it will be time for
            # one of us to make the next decision.  If dist1
            # is zero, then that time is right now, and zero
            # time will elapse before then
            #
            #elapsed = min(distance + 1, dist1)

            elapsed = min(dist1, distance + 1)

            new_total, new_path = extend_2a(
                    cave,
                    neighbor, 1 + distance - elapsed,
                    node1, dist1 - elapsed,
                    visited + [neighbor], current_total + added_flow,
                    minutes - elapsed, scores)
                    #(next_minutes - 1) - elapsed)

            if highest_total <= new_total:
                highest_total, highest_path = new_total, new_path
    elif dist1 == 0:
        new_total, new_path = extend_2a(
                cave,
                node1, dist1,
                node0, dist0,
                visited, current_total,
                minutes, scores)

        if highest_total <= new_total:
            highest_total, highest_path = new_total, new_path
    else:
        print('ZOUNDS')
        new_total, new_path = extend_2a(
                cave,
                node0, dist0 - 1,
                node1, dist1 - 1,
                visited, current_total,
                minutes - 1, scores)
 
        if highest_total <= new_total:
            highest_total, highest_path = new_total, new_path

    return highest_total, highest_path


def solver_pt2(cave, start='AA', minutes=26):

    """
    highest_flow, highest_path, highest_hist = extend_2a(
            cave, start, 0, start, 0, [start], 0, minutes, [])
    return highest_flow, highest_path, highest_hist
    """

    scores = {}

    highest_flow, highest_path = extend_2a(
            cave, start, 0, start, 0, [start], 0,
            minutes, scores)
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
    print('part 1: ', flow)
    #print('part 1 path ', path)

    #flow, path, hist = solver_pt2(cm, start='AA', minutes=26)
    flow, path = solver_pt2(cm, start='AA', minutes=26)
    print('part 2 ', flow)
    # print('part 2 path ', path)
    # print('part 2 hist ', hist)


if __name__ == '__main__':
    main()

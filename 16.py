#!/usr/bin/env python3

import copy
import re
import sys

class CaveMap:

    def __init__(self, valves, root_name='AA'):

        self.valves = valves
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
            path = states.pop()

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


def extend(cave, node, path, flow, minutes):

    spacer = ' ' * (30 - minutes)
    print('%s %s flow %d mins %d %s' %
          (spacer, node, flow, minutes, str(path)))

    if minutes <= 0:
        return flow

    # If we don't change any more valves,
    # this is how much will flow during the
    # remaining minutes
    #
    base_score = flow

    # How much we can improve the score by
    # opening a given valve
    #
    inc_score = 0
    highest_inc_score = base_score

    neighbors = cave.paths[node]
    for neighbor, distance in neighbors:
        if distance >= minutes:
            continue

        if neighbor in path:
            continue

        added_rate = cave.valves[neighbor].rate
        added_flow = added_rate * ((minutes - 1) - distance)
        print('added flow %d rate %d' % (added_flow, added_rate))
        inc_score = extend(
                cave, neighbor, path + [neighbor],
                flow + added_flow, (minutes - 1) - distance)

        highest_inc_score = max(inc_score, highest_inc_score)

    # print('best %d %s' % (highest_inc_score, str(path)))

    return highest_inc_score


def solver_pt1(cave, start='AA', minutes=30):

    # Examine every path through valves that can be traversed,
    # including the time required to open the valve, in the
    # time alloted, and then evaluate the total flow that
    # would result, and see whether it is better than the
    # highest flow we've found so far
    #
    # This might blow up for the big cases.  We'll see.

    highest = extend(cave, start, [start], 0, minutes)
    return highest



def log_state(valves, valve_states, minute, pressure):
    return '\n== Minute %d ==\nValves %s are open, releasing %d pressure' % (
            minute,
            ', '.join(sorted([v for v in valves if valve_states[v]])), pressure)


def part1_bfs(curr, valves, minutes_remaining):


    # The search state allows us to prune the search:
    # Whenever we decide to turn on a valve, we calculate
    # how much flow we've already accounted for (including
    # that valve) during the remaining minutes.  We then
    # compare that value to the value in this table: if the
    # new value is <= the value in the table, then there's
    # no point in continuing because already found a path
    # where we were doing better, so we abandon this path.
    # Otherwise, we update the table and continue on.
    #
    search_state = {name : (0, minutes_remaining) for name in valves.keys()}

    print('SEARCH STATE')
    print(search_state)

    return part1_bfs_worker(curr, valves, minutes_remaining - 1, search_state)


def part1_bfs_worker(curr, valves, minutes_remaining, search_state):

    search_queue = []

    # If the rate of a valve is zero, then just pretend that
    # it's already open.  We can't "open" it any more than it
    # already is.
    #
    open_v = [v.name for v in valves.values() if v.rate == 0]
    print('OPEN_V ', open_v)

    # Each queue entry: (vname, minutes_remaining,s
    # curr_flow, minutes_needed, total_flow, open_v, path)
    #
    search_queue.append((curr, minutes_remaining, 0, 0, 0, open_v, []))

    highest_total = 0

    already = set()

    while search_queue:
        # print('LENQ %d' % len(search_queue))

        cand = search_queue.pop()
        # print('CAND ', cand)
        (vname, minutes, curr_flow, minutes_needed, total_flow,
                open_v, path_since_turn) = cand

        # print('v %s m %d c %d t %d' % (vname, minutes, curr_flow, total_flow))

        for _ in range(min(minutes, minutes_needed)):
            total_flow += curr_flow
            minutes -= 1

        if minutes <= 0:
            final_total = total_flow + curr_flow # WHA?
            #print('T vname %s total %d' % (vname, total_flow))
            if final_total > highest_total:
                highest_total = final_total
                # print('HIGHEST %d len %d' % (highest_total, len(search_queue)))
                # print(search_state)

            continue

        # print('open_v ', open_v)
        if len(open_v) == len(valves):
            # print('we ran out of valves to open at %d' % minutes)
            final_total = total_flow + curr_flow * (minutes + 1)
            if final_total > highest_total:
                highest_total = final_total
                # print('VHIGHEST %d len %d' % (highest_total, len(search_queue)))
                # print('V curr_flow %d total_flow %d r %d' % (
                #     curr_flow, total_flow, minutes))

            continue


        valve = valves[vname]

        if valve.rate >= 0 and vname not in open_v:
            # If this valve isn't open on this path,
            # add a state where we open it.
            # The position stays the same, but the
            # flow increases, the valve gets added
            # to the set of open valves, and the
            # current valve-less path gets reset to
            # just be name of this valve
            #
            next_step = (
                    vname, minutes - 1,
                    curr_flow + valve.rate,
                    0,
                    total_flow + curr_flow,
                    open_v + [vname], [vname])

            search_queue.append(next_step)

        for neighbor, distance in valve.neighbors:
            print('PST ', path_since_turn)
            print('N %s DISTANCE %d' % (neighbor, distance))

            if neighbor not in path_since_turn:
                next_step = (
                        neighbor, minutes,
                        curr_flow,
                        distance,
                        total_flow,
                        open_v, path_since_turn + [neighbor])
                # search_queue.append(next_step)

                """
                # don't keep pushing the same stuff
                #
                rep = str(next_step)
                if rep not in already:
                    already.add(rep)
                    search_queue.append(next_step)
                else:
                    print('OMIT duplicate: %s' % rep)
                    pass
                """

            else:
                #print('skipping path %s + %s' % (str(path_since_turn), vname))
                pass

    return highest_total


def part2_bfs(curr0, curr1, valves, minutes_remaining):

    # The search state allows us to prune the search:
    # Whenever we decide to turn on a valve, we calculate
    # how much flow we've already accounted for (including
    # that valve) during the remaining minutes.  We then
    # compare that value to the value in this table: if the
    # new value is <= the value in the table, then there's
    # no point in continuing because already found a path
    # where we were doing better, so we abandon this path.
    # Otherwise, we update the table and continue on.
    #
    search_state = {name : (0, minutes_remaining) for name in valves.keys()}

    print('SEARCH STATE')
    print(search_state)

    return part2_bfs_worker(
            curr0, curr1, valves, minutes_remaining - 1, search_state)


def part2_bfs_worker(curr0, curr1, valves, minutes_remaining, search_state):

    search_queue = []

    # If the rate of a valve is zero, then just pretend that
    # it's already open.  We can't "open" it any more than it
    # already is.
    #
    open_v = [v.name for v in valves.values() if v.rate == 0]
    print('2 OPEN_V ', open_v)

    # Each queue entry: (vname1, vname2, minutes_remaining,
    # curr_flow, minutes_needed, total_flow, open_v, path)
    #
    search_queue.append(
            (curr0, curr1, minutes_remaining, 0, 0, open_v, [], []))

    highest_total = 0

    already = set()

    while search_queue:
        # print('LENQ %d' % len(search_queue))

        cand = search_queue.pop()
        # print('CAND ', cand)
        (vname0, vname1, minutes, curr_flow, total_flow,
                open_v, pst0, pst1) = cand

        # print('v %s m %d c %d t %d' % (vname, minutes, curr_flow, total_flow))

        if minutes <= 0:
            # print('MINUTES <= 0')
            final_total = total_flow + curr_flow # WHA?
            #print('T vname %s total %d' % (vname, total_flow))
            if final_total > highest_total:
                highest_total = final_total
                # print('HIGHEST %d len %d' % (highest_total, len(search_queue)))
                # print(search_state)

            continue

        if len(open_v) == len(valves):
            # print('ALL OPEN')
            final_total = total_flow + curr_flow * (minutes + 1)
            if final_total > highest_total:
                highest_total = final_total

            continue

        valve0 = valves[vname0]
        valve1 = valves[vname1]

        next_v0 = []
        next_v1 = []

        new_open_v = open_v[:]

        if valve0.rate >= 0 and vname0 not in new_open_v:
            new_open_v.append(vname0)
            next_v0.append(
                    (vname0, valve0.rate, open_v + [vname0], [vname0]))

        if valve1.rate >= 0 and vname1 not in new_open_v:
            next_v1.append(
                    (vname1, valve1.rate, open_v + [vname1], [vname1]))

        for neighbor, distance in valve0.neighbors:
            if neighbor not in pst0:
                next_v0.append((neighbor, 0, open_v, pst0 + [vname0]))

        for neighbor, distance in valve1.neighbors:
            if neighbor not in pst1:
                next_v1.append((neighbor, 0, open_v, pst1 + [vname1]))

        for e0 in next_v0:
            next0, flow_change0, open_v0, new_pst0 = e0
            for e1 in next_v1:
                next1, flow_change1, open_v1, new_pst1 = e1

                search_queue.append(
                        (next0, next1,
                         minutes - 1,
                         curr_flow + flow_change0 + flow_change1,
                         total_flow + curr_flow,
                         list(set(open_v0 + open_v1)),
                         new_pst0, new_pst1))

    return highest_total


def main():

    valves = reader()
    for vname in sorted(valves.keys()):
        print(valves[vname])

    #total_flow = part1_dfs('AA', valves, 30, 0, [], [])
    #print('part 1: %d' % total_flow)

    #total_flow = part1_bfs('AA', valves, 30)
    #print('part 1a: %d' % total_flow)

    cm = CaveMap(valves)

    for elem in cm.paths:
        print('node ', elem, ' ', str(cm.paths[elem]))

    print('Ex ', solver_pt1(cm, start='AA', minutes=30))

    sys.exit(0)

    total_flow = part2_bfs('AA', 'AA', cm.valves, 26)
    print('part 2: %d' % total_flow)


if __name__ == '__main__':
    main()

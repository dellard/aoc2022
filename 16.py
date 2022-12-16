#!/usr/bin/env python3

import copy
import re
import sys

class CaveMap:

    def __init__(self, valves):
        self.valves = valves

    def simplify(self):

        working_valves = [copy.deepcopy(v) for v in self.valves if v.rate > 0]

        for start_valve in working_valves:
            start_valve.neighbors = []

            for end_valve in working_valves:
                if start_valve == end_valve:
                    continue

                start_valve.neighbors.append(
                        self.find_shortest(start_valve, end_valve))

        self.valves = working_valves

    def find_shortest(self, start, end):
        # I'm certain I was supposed to learn this in class.
        # Or maybe teach this in class.
        #
        # But I'm just going to make the attempt
        # 
        pass


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

        """
        # don't keep pushing the same stuff
        #
        rep = str(next_step)
        if rep not in already:
            already.add(rep)
            search_queue.append(next_step)
        else:
            # print('omitting duplicate: %s' % rep)
            pass
        """

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
            # print('PST ', path_since_turn)
            # print('DISTANCE %d' % distance)

            if neighbor not in path_since_turn:
                next_step = (
                        neighbor, minutes,
                        curr_flow,
                        distance,
                        total_flow,
                        open_v, path_since_turn + [neighbor])
                search_queue.append(next_step)
            else:
                #print('skipping path %s + %s' % (str(path_since_turn), vname))
                pass

    return highest_total


def part1_dfs(
        curr, valves, minutes_remaining, curr_flow,
        path_so_far, sequence):

    # At each timestep, we can either move to another valve
    # immediately (which takes one minute) or open the current valve
    # if it's closed (which takes a minute)

    if minutes_remaining == 0:
        # print('curr BASE %s' % curr)
        #print('====')
        #print('\n'.join(sequence))
        return 0

    best_score = 0

    # If a valve is closed, it takes one minute to open it.
    # This means that it might make sense to skip opening
    # and use that minute to move to another valve that
    # has a higher rate
    #
    if valves[curr].closed and valves[curr].rate > 0:

        #sequence.append(
        #        log_state(valves, valve_states,
        #                  30 - minutes_remaining, curr_flow))
        #sequence.append('You open valve %s.' % curr)

        new_flow = curr_flow + valves[curr].rate
        valves[curr].closed = False
        score = part1_dfs(
                curr, valves,
                minutes_remaining - 1,
                new_flow, [], sequence)
        valves[curr].closed = True

        #sequence.pop()
        #sequence.pop()

        if best_score < score:
            best_score = score

    for next_valve, distance in valves[curr].neighbors:

        if distance != 1:
            print('OOPS this code DOES NOT support distances')

        # observation: it just wastes time to loop around to
        # some place that we've already seen, unless we open
        # a valve somewhere along the way

        if next_valve in path_so_far:
            # print('POINTLESS LOOPING %s' % path_so_far)
            continue

        #print('curr %s next %s min %d flow %d' %
        #      (curr, next_valve, minutes_remaining, flow_this_minute))

        #sequence.append('at valve %s at %d release %d' % (
        #    next_valve, 30 - minutes_remaining, flow_this_minute))

        #sequence.append(
        #        log_state(valves, valve_states,
        #                  30 - minutes_remaining, curr_flow))
        #sequence.append('You move to valve %s.' % next_valve)
        score = part1_dfs(
                next_valve, valves, minutes_remaining - 1,
                curr_flow, path_so_far + [next_valve], sequence)
        #sequence.pop()
        #sequence.pop()

        if score > best_score:
            best_score = score

    return curr_flow + best_score


def main():

    valves = reader()
    for vname in sorted(valves.keys()):
        print(valves[vname])

    #total_flow = part1_dfs('AA', valves, 30, 0, [], [])
    #print('part 1: %d' % total_flow)

    total_flow = part1_bfs('AA', valves, 30)
    print('part 1a: %d' % total_flow)


if __name__ == '__main__':
    main()

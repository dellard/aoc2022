#!/usr/bin/env python3

import re
import sys

class Valve:

    def __init__(self, name, vrate, neighbors):

        self.name = name
        self.rate = vrate
        self.neighbors = neighbors
        self.closed = True


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


def part1_search(
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
        score = part1_search(
                curr, valves,
                minutes_remaining - 1,
                new_flow, [], sequence)
        valves[curr].closed = True

        #sequence.pop()
        #sequence.pop()

        if best_score < score:
            best_score = score

    for next_valve in valves[curr].neighbors:

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
        score = part1_search(
                next_valve, valves, minutes_remaining - 1,
                curr_flow, path_so_far + [next_valve], sequence)
        #sequence.pop()
        #sequence.pop()

        if score > best_score:
            best_score = score

    return curr_flow + best_score


def main():
    valves = reader()
    #print(valves)

    valve_states = {valve : False for valve in valves}
    print(valve_states)

    path = []
    x = part1_search('AA', valves, 30, 0, [], [])
    print(x)
    print(path)


if __name__ == '__main__':
    main()

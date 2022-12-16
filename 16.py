#!/usr/bin/env python3

import re
import sys


def reader():

    valves = {}

    for line in sys.stdin:
        tokens = line.strip().split()

        vname = tokens[1]
        vrate = int(re.findall(r'-*\d+', tokens[4])[0])
        vleads = [re.sub(',', '', lead.strip()) for lead in tokens[9:]]

        valves[vname] = (vname, vrate, vleads)

    return valves


def sum_open(valves, valve_states):

    total = 0

    for valve in valves:
        if valve_states[valve]:
            total += valves[valve][1]

    return total

def log_state(valves, valve_states, minute, pressure):
    return '\n== Minute %d ==\nValves %s are open, releasing %d pressure' % (
            minute,
            ', '.join(sorted([v for v in valves if valve_states[v]])), pressure)


def part1_search(
        curr, valves, valve_states, minutes_remaining, path_so_far, sequence):

    # At each timestep, we can either move to another valve
    # immediately (which takes one minute) or open the current valve
    # if it's closed (which takes a minute)

    flow_this_minute = sum_open(valves, valve_states)
    #sequence.append(
    #        log_state(valves, valve_states, 30 - minutes_remaining, flow_this_minute))

    if minutes_remaining == 0:
        # print('curr BASE %s' % curr)
        print('====')
        print('\n'.join(sequence))
        return 0

    # Is there ever any reason to not open a valve with
    # a non-zero rate as soon as we reach it?
    #
    if valve_states[curr] == False and valves[curr][1] > 0:

        valve_states[curr] = True

        #sequence.append('You open valve %s.' % curr)

        score = part1_search(
                curr, valves, valve_states, minutes_remaining - 1, [], sequence)

        #sequence.pop()
        #sequence.pop()

        valve_states[curr] = False

        return flow_this_minute + score

    best_score = 0
    for next_valve in valves[curr][2]:
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

        #sequence.append('You move to valve %s' % next_valve)
        score = part1_search(
                next_valve, valves, valve_states, minutes_remaining - 1,
                path_so_far + [next_valve], sequence)
        #sequence.pop()
        if score > best_score:
            best_score = score

    #sequence.pop()

    return flow_this_minute + best_score


def main():
    valves = reader()
    #print(valves)

    valve_states = {valve : False for valve in valves}
    print(valve_states)

    path = []
    x = part1_search('AA', valves, valve_states, 30, [], [])
    print(x)
    print(path)


if __name__ == '__main__':
    main()

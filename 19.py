#!/usr/bin/env python3

import re
import sys


class Blueprint:

    def __init__(
            self, number, ore_cost, clay_cost,
            obs_cost_ore, obs_cost_clay,
            geo_cost_ore, geo_cost_obs):

        self.number = number

        # pretending things might cost geodes makes the
        # calculations easier later
        #
        self.ore_cost = (ore_cost, 0, 0, 0)
        self.clay_cost = (clay_cost, 0, 0, 0)
        self.obs_cost = (obs_cost_ore, obs_cost_clay, 0, 0)
        self.geo_cost = (geo_cost_ore, 0, geo_cost_obs, 0)
        self.none_cost = (0, 0, 0, 0)

        self.costs = {
                'ore' : self.ore_cost,
                'clay' : self.clay_cost,
                'obsidian' : self.obs_cost,
                'geode' : self.geo_cost,
                'none' : self.none_cost,
            }
 
    def __repr__(self):
        return '%d: ore %s clay %s obs %s geo %s' % (
                self.number, self.ore_cost,
                self.clay_cost, self.obs_cost,
                self.geo_cost)

    def new_robots(self, supplies):
        """
        Return the types of robots we can construct with
        the given quantity of ore, clay, and obsidian, and
        the corresponding remaining ore, clay, and obsidian.
        """

        const = {}

        # This is the worst way to do this
        # FIXME
        for r_type, r_costs in self.costs.items():
            if all([supplies[i] >= r_costs[i] for i in range(4)]):
                const[r_type] = tuple(
                        [supplies[i] - r_costs[i] for i in range(4)])

        return const


def reader():

    blueprints = []
    for line in sys.stdin:
        tokens = [int(x) for x in re.findall(r'\d+', line)]
        blueprints.append(Blueprint(*tokens))

    return blueprints


def max_cracked(minutes_remaining):
    """
    If we started build new geode-cracking robots at
    one per minute right now, and each takes a minute to
    build, and each starts cracking one geode per minute
    until time runs out, how many geodes could they crack?
    """

    cracked = 0
    for i in range(minutes_remaining):
        cracked += i

    return cracked


def solver1_dfs(blueprint, minutes, robots, supplies, seen):

    stack = []
    stack.append((minutes, robots, supplies))

    max_possibles = [max_cracked(x) for x in range(minutes + 1)]
    print('MAX_POSSIBLES ', max_possibles)

    highest_score = 0
    while stack:
        key = stack.pop()

        if key in seen:
            print('%sCUT min %d %d' % (spacer, minutes, seen[key]))
            continue

        seen[key] = 1

        (minutes, robots, supplies) = key
        spacer = ' ' * (24 - minutes)

        if minutes < 2:
            if minutes == 0:
                score = supplies[3]
                print('OOPS HIT BOTTOM')
            elif minutes == 1:
                score = supplies[3] + robots[3]
                # print('HIT ALMOST')

            print(spacer, 'got ', score)
            if score > highest_score:
                highest_score = score
                print('NEW high score y %d' % highest_score)

            continue

        curr_score = supplies[3]
        max_possible = curr_score + (robots[3] * minutes) + max_possibles[minutes]
        if max_possible <= highest_score:
            print('IMP %d' % minutes)
            continue


        # base case: if we have enough robots to supply us with
        # the materials to make a new geode robot, then we might
        # as well just make new geode robots from now on.
        #
        geo_cost = blueprint.geo_cost
        if all([robots[i] >= geo_cost[i] for i in range(3)]):
            print('BASE for max construction')
            # FIXME: this probably isn't right: the number of geode robots
            # will increase with each passing minute, so it's a square
            # but the parameters are iffy
            score = ((minutes - 1) * (minutes - 2)) + supplies[3]
            if score > highest_score:
                highest_score = score
                print('NEW high score z %d' % highest_score)

            continue

        print('%smin %d r %s s %s' % (spacer, minutes, str(robots), str(supplies)))

        factory_choices = blueprint.new_robots(supplies)
        # print('FACT ', factory_choices)

        # order matters; we want to leave the move that is likely
        # to be best on the top of the stack so it will get expanded
        # first.  Unfortunately, we can only guess what the best move
        # is, although in the long run we want lots of geode robots
        #
        for name in ['none', 'ore', 'clay', 'obsidian', 'geode']:
            if name in factory_choices:
                new_supplies = factory_choices[name]
                # print('NAME = %s %s' % (name, supplies))

                if name == 'none':
                    new_robots = robots
                elif name == 'ore':
                    new_robots = (robots[0] + 1, robots[1], robots[2], robots[3])
                elif name == 'clay':
                    new_robots = (robots[0], robots[1] + 1, robots[2], robots[3])
                elif name == 'obsidian':
                    new_robots = (robots[0], robots[1], robots[2] + 1, robots[3])
                elif name == 'geode':
                    new_robots = (robots[0], robots[1], robots[2], robots[3] + 1)
                else:
                    print('OOPS')

                next_state = (minutes - 1, new_robots,
                        tuple([robots[i] + new_supplies[i] for i in range(4)]))
                if next_state in seen:
                    print('%sCUT min %d %d' % (spacer, minutes, seen[key]))
                    continue
                else:
                    stack.append(next_state)

    return highest_score


def solver1(blueprints, minutes):

    best_scores = []
    total = 0
    ind = 1
    for blueprint in blueprints:
        seen = {}
        score = solver1_dfs(
                blueprint, minutes, (1, 0, 0, 0), (0, 0, 0, 0), seen)
        total += ind * score
        best_scores.append(score)
        ind += 1

    ind = 1
    for score in best_scores:
        print('score %d = %d' % (ind, score))
        ind += 1

    return total


def solver2(blueprints, minutes):

    best_scores = []
    prod = 1
    for blueprint in blueprints[:3]:
        seen = {}
        score = solver1_dfs(
                blueprint, minutes, (1, 0, 0, 0), (0, 0, 0, 0), seen)
        prod *= score
        best_scores.append(score)

    ind = 1
    for score in best_scores:
        print('score %d = %d' % (ind, score))
        ind += 1

    return prod


def main():

    blueprints = reader()

    #for bluep in blueprints:
    #    print(bluep)

    #new_stuff = blueprints[0].new_robots(supplies)
    #for row in new_stuff:
    #    print(row)

    #for i in range(10):
    #    print('%d %d' % (i, max_cracked(i)))

    print('part 1: ', solver1(blueprints, 24))
    print('part 2: ', solver2(blueprints, 32))


if __name__ == '__main__':
    main()

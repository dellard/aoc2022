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


def solver1_dfs(blueprint, minutes, robots, supplies, seen):

    spacer = ' ' * (24 - minutes)

    key = (minutes, robots, supplies)
    # key = (robots, supplies)
    if key in seen:
        print('%sCUT min %d %d' % (spacer, minutes, seen[key]))
        return seen[key]

    if minutes == 0:
        print(spacer, 'got ', supplies[3])

        return supplies[3]

    # base case: if there's only one minute left, then
    # there's no point in trying to build any more robots;
    # just run the geode-cracking robots we have one more
    # cycle
    if minutes == 1:
        print('BASE stop')
        return supplies[3] + robots[3]

    # base case: if we have enough robots to supply us with
    # the materials to make a new geode robot, then we might
    # as well just make new geode robots from now on.
    #
    geo_cost = blueprint.geo_cost
    if all([robots[i] >= geo_cost[i] for i in range(3)]):
        print('BASE')
        # FIXME: this probably isn't right: the number of geode robots
        # will increase with each passing minute, so it's a square
        # but the parameters are iffy
        return ((minutes - 1) * (minutes - 2)) + supplies[3]

    print('%smin %d r %s s %s' % (spacer, minutes, str(robots), str(supplies)))

    scores = []
    factory_choices = blueprint.new_robots(supplies)
    print('FACT ', factory_choices)

    for name in ['geode', 'obsidian', 'clay', 'ore', 'none']:
        if name in factory_choices:
            new_supplies = factory_choices[name]
            print('NAME = %s %s' % (name, supplies))

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

            scores.append(solver1_dfs(
                    blueprint, minutes - 1, new_robots, 
                    tuple([robots[i] + new_supplies[i] for i in range(4)]),
                    seen))

    if not scores:
        best = 0
    else:
        best = max(scores)
    seen[key] = best

    return best


def solver1(blueprints, minutes):

    best_scores = []
    # TODO: skipping 0 for now
    for blueprint in blueprints:
        seen = {}
        best_scores.append(
                solver1_dfs(blueprint, minutes,
                            (1, 0, 0, 0), (0, 0, 0, 0), seen))

    return best_scores


def main():

    blueprints = reader()

    for bluep in blueprints:
        print(bluep)

    #new_stuff = blueprints[0].new_robots(supplies)
    #for row in new_stuff:
    #    print(row)

    print('1 ', solver1(blueprints, 24))


if __name__ == '__main__':
    main()

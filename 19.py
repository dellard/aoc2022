#!/usr/bin/env python3

import re
import sys


class Blueprint:

    def __init__(
            self, number, ore_cost, clay_cost,
            obs_cost_ore, obs_cost_clay,
            geo_cost_ore, geo_cost_obs):

        self.number = number
        self.ore_cost = (ore_cost, 0, 0)
        self.clay_cost = (clay_cost, 0, 0)
        self.obs_cost = (obs_cost_ore, obs_cost_clay, 0)
        self.geo_cost = (geo_cost_ore, 0, geo_cost_obs)

    def __repr__(self):
        return '%d: ore %s clay %s obs %s geo %s' % (
                self.number, self.ore_cost,
                self.clay_cost, self.obs_cost,
                self.geo_cost)


def reader():

    blueprints = []
    for line in sys.stdin:
        tokens = [int(x) for x in re.findall(r'\d+', line)]
        blueprints.append(Blueprint(*tokens))

    return blueprints


def main():

    blueprints = reader()

    for bluep in blueprints:
        print(bluep)


if __name__ == '__main__':
    main()

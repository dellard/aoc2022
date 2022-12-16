#!/usr/bin/env python3

import re
import sys


def reader():

    valves = []

    for line in sys.stdin:
        tokens = line.strip().split()

        vname = tokens[1]
        vrate = int(re.findall(r'-*\d+', tokens[4])[0])
        vleads = tokens[9:]

        valves.append((vname, vrate, vleads))

    return valves


def main():
    valves = reader()
    #print(valves)


if __name__ == '__main__':
    main()

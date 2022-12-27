#!/usr/bin/env python3

"""
Advent of Code 2022, day 7
"""

import sys

class DirNode:

    def __init__(self, path):

        self.path = path

        # updated later
        self.total_size = 0

    def __repr__(self):
        return self.path


class FileNode:

    def __init__(self, path, size):

        self.path = path
        self.total_size = size

    def __repr__(self):
        return '%s %d' % (self.path, self.total_size)


def reader():

    path_sep = '/'
    known_nodes = {}

    curr_path = ''
    curr_dirs = []
    curr_files = []
    in_ls = False

    for line in sys.stdin:
        tokens = line.strip().split()

        if tokens[0] == '$':
            if tokens[1] == 'cd':

                # If we're in the ls state, and we see a cd, then the ls
                # is finished, so add the info we've learned to the
                # known_nodes.  Note that if there's an ls before the
                # first cd, the resulting info ends up with a path
                # where it will be ignored, but this doesn't seem to
                # happen.
                #
                if in_ls:
                    known_nodes[curr_path] = (curr_dirs, curr_files)
                    # print('%s -> %s %s' % (curr_path, str(curr_dirs), str(curr_files)))

                    curr_dirs = []
                    curr_files = []
                    in_ls = False

                if tokens[2] == '/':
                    curr_path = '/'
                else:
                    if tokens[2] == '..':
                        if not curr_path:
                            print('oops 1')
                            curr_path = '/'
                        elif curr_path == '/':
                            curr_path = '/'
                        else:
                            # print('we are [%s]' % curr_path)
                            curr_path = curr_path[:curr_path[:-1].rindex(path_sep)] + '/'
                            # what if we cd past '/'?  It's not defined.
                            # print('popping to %s' % curr_path)
                    else:
                        curr_path = curr_path + tokens[2] + path_sep
                        # print('pushing %s' % curr_path)
            elif tokens[1] == 'ls':
                in_ls = True
        else:
            # we might create entries more than once, if the user does an
            # ls multiple times in the same directory, but they'll just
            # replace each other, so no harm done beyond the inefficiency
            #
            item_path = curr_path + tokens[1]
            if tokens[0] == 'dir':
                curr_dirs.append(DirNode(item_path + path_sep))
            else:
                curr_files.append(FileNode(item_path, int(tokens[0])))

    # deal with any stragglers, if the last command is an ls (not a cd)
    if in_ls:
        known_nodes[curr_path] = (curr_dirs, curr_files)

    return known_nodes


def dir_walk(nodes, root_path, sizes, level=0):
    # compute the size of each file and directory

    if root_path not in nodes:
        print('oops walker root [%s] level %d' % (root_path, level))
        return 0

    root_node = nodes[root_path]

    my_size = 0

    for child_dir in root_node[0]:
        #print('%s %s' % ('   ' * level, child_dir.path))
        dir_size = dir_walk(nodes, child_dir.path, sizes, level=level + 1)
        sizes[child_dir.path] = dir_size
        my_size += dir_size

    for child_file in root_node[1]:
        sizes[child_file.path] = child_file.total_size
        my_size += child_file.total_size
        #print('%s %d %s' % ('   ' * level, child_file.total_size, child_file.path))

    #print('here %s total %d' % (root_path, my_size))
    sizes[root_path] = my_size
    return my_size


def find_sum_of_smalls(sizes, max_size):

    total = 0

    for path in sizes:
        if path.endswith('/') and sizes[path] <= max_size:
            total += sizes[path]

    return total


def find_smallest_above(sizes, target):

    candidate_size = -1

    for path in sizes:
        if not path.endswith('/'):
            continue

        if sizes[path] >= target:
            if candidate_size < 0:
                # print('starting at %s' % path)
                candidate_size = sizes[path]
            elif sizes[path] < candidate_size:
                # print('switching to %s' % path)
                candidate_size = sizes[path]

    return candidate_size


def main():
    nodes = reader()
    # print(nodes)

    sizes = {}
    dir_walk(nodes, '/', sizes)

    #print(sizes)

    print('part 1: %d' % find_sum_of_smalls(sizes, 100000))

    total_space_used = sizes['/']
    total_space_free = 70000000 - total_space_used
    needed_space = 30000000 - total_space_free

    print('part 2: %d' % find_smallest_above(sizes, needed_space))


if __name__ == '__main__':
    main()

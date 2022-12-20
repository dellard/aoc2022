#!/usr/bin/env python3

import array
import sys


def reader():

    numbers = []

    for line in sys.stdin:
        numbers.append(int(line))

    return numbers

def rotate_backward(arr, start, length, alen):

    if length >= alen:
        length %= alen

    # print('backward s %d l %d' % (start, length))
    temp = arr[start]

    for i in range(length):
        arr[(start - i) % alen] = arr[(start - (i + 1)) % alen]

    arr[(start - length) % alen] = temp

    # print('back arr ', arr)


def rotate_forward(arr, start, length, alen):

    # This might be an off-by-one bug, but we peel off
    # 1 less than you'd think
    #
    if length >= alen:
        length -= (alen - 1)

    # print('foreward s %d l %d' % (start, length))
    temp = arr[start]

    for i in range(length):
        # print('%d %d' % (start - i, start + (i - 1)))
        arr[(start + i) % alen] = arr[(start + i + 1) % alen]

    arr[(start + length) % alen] = temp

    # print('fore arr ', arr)


def mixer_part1(olist):

    nlist_len = len(olist)

    ilist = array.array('l', [i for i in range(nlist_len)])

    for i in range(nlist_len):
        # print(i, ' ', [olist[ilist[i]] for i in range(nlist_len)])

        movement = olist[i]
        try:
            offset = ilist.index(i)
        except ValueError as exc:
            print(exc, ' i = ', i)
            sys.exit(1)

        if movement > 0:
            rotate_forward(ilist, offset, movement, nlist_len)
        elif movement < 0:
            rotate_backward(ilist, offset, -movement, nlist_len)
        else:
            pass

    return [olist[ilist[i]] for i in range(nlist_len)]


def tests_part1(input):

    a = [0, 1, 2, 3, 4, 5, 6]
    print(a)
    rotate_forward(a, 1, 4, len(a))
    print('a ', a, ' r a ')
    rotate_backward(a, 5, 4, len(a))
    print('a ', a, ' r a ')
    print('-----')

    a = [0, 1, 2, 3, 4, 5, 6]
    rotate_forward(a, 1, 1, len(a))
    print('a ', a, ' r a ')
    rotate_backward(a, 1, 1, len(a))
    print('a ', a, ' r a ')

    a = [0, 1, 2, 3, 4, 5, 6]
    rotate_forward(a, 5, 2, len(a))
    print('a ', a, ' r a ')
    rotate_backward(a, 5, 2, len(a))
    print('a ', a, ' r a ')

    # sys.exit(0)

    #print(input)

    #print(mixer_part1(input))

    #x = [4, 5, 6, 1, 7, 8, 9]
    x = [1, 2, -3, 3, -2, 0, 4]
    print('F %s -> %s' % (str(x), str(mixer_part1(x))))

    for x in [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [2, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 2, 0],
            [0, 0, 0, 2],
            [-1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, -1],
            ]:
        print('==========')
        msg = mixer_part1(x[:])
        print('D x ', x, ' msg ', msg)

    # sys.exit(0)



def main():

    input = reader()

    msg = mixer_part1(input)
    msg_offset = msg.index(0)
    msg_len = len(msg)
    offsets = [(msg_offset + i * 1000) % msg_len for i in [1, 2, 3]]

    print('part 1: %d' % (msg[offsets[0]] + msg[offsets[1]] + msg[offsets[2]]))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import array
import sys


def reader():

    numbers = []

    for line in sys.stdin:
        numbers.append(int(line))

    return numbers

def rotate_backward(arr, start, length, alen):

    print('backward s %d l %d' % (start, length))
    temp = arr[start]

    for i in range(length):
        arr[(start - i) % alen] = arr[(start - (i + 1)) % alen]

    arr[(start - length) % alen] = temp

    print('back arr ', arr)


def rotate_forward(arr, start, length, alen):

    print('foreward s %d l %d' % (start, length))
    temp = arr[start]

    for i in range(length):
        print('%d %d' % (start - i, start + (i - 1)))
        arr[(start + i) % alen] = arr[(start + i + 1) % alen]

    arr[(start + length) % alen] = temp

    print('fore arr ', arr)



def mixer2(olist):

    nlist_len = len(olist)

    ilist = array.array('l', [i for i in range(nlist_len)])

    for i in range(nlist_len):
        print(i, ' ', [olist[ilist[i]] for i in range(nlist_len)])

        movement = olist[i]
        try:
            offset = ilist.index(i)
        except ValueError as exc:
            print(exc, ' i = ', i)

        if movement > 0:
            rotate_forward(ilist, offset, movement, nlist_len)
        elif movement < 0:
            rotate_backward(ilist, offset, -movement, nlist_len)
        else:
            pass

    return [olist[ilist[i]] for i in range(nlist_len)]



def mix_numbers(olist):

    nlist_len = len(olist)
    ilist = [i for i in range(nlist_len)]

    for i in range(nlist_len):

        movement = olist[i]
        try:
            o_pos = ilist.index(i)
        except ValueError as exc:
            print(exc, ' i = ', i)


        n_pos = (o_pos + movement) % nlist_len

        print('move %d (pos %d) by %d to position %d'
              % (movement, o_pos, mov, n_pos))

        if movement == 0:
            print('case no-move')
            continue

        # I think direction matters?
        if movement > 0:

            if o_pos < n_pos:
                left = ilist[0:o_pos]
                mid = ilist[o_pos + 1:n_pos + 1]
                right = ilist[n_pos + 1:]

                #print('left %s o_pos %d mid %s n_pos %d right %s' %
                #      (left, o_pos, mid, n_pos, right))

                if n_pos == nlist_len - 1:
                    # special case?
                    print('SAW IT')
                    ilist = [i] + left + mid + right
                else:
                    ilist = left +  mid + [i] + right

            elif n_pos < o_pos:
                left = ilist[0:n_pos]
                mid = ilist[n_pos:o_pos]
                right = ilist[o_pos + 1:]

                if n_pos == 0:
                    # special case?
                    ilist = left + mid + right + [i]
                else:
                    ilist = left + [i] + mid + right

        if len(ilist) != len(olist):
            print('WHOOPS')
            return

        # print('ind result ', ilist)
        # print('result ', [olist[ilist[i]] for i in range(nlist_len)])
        # print('')

    return [olist[ilist[i]] for i in range(nlist_len)]


def main():

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

    input = reader()

    #print(input)

    #print(mixer2(input))

    #x = [4, 5, 6, 1, 7, 8, 9]
    x = [1, 2, -3, 3, -2, 0, 4]
    print('F %s -> %s' % (str(x), str(mixer2(x))))

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
        msg = mixer2(x[:])
        print('D x ', x, ' msg ', msg)

    # sys.exit(0)


    #msg = mix_numbers(input)
    msg = mixer2(input)
    msg_offset = msg.index(0)
    msg_len = len(msg)
    offsets = [(msg_offset + i * 1000) % msg_len for i in [1, 2, 3]]

    s0 = sorted(input)
    s1 = sorted(msg)
    if s0 != s1:
        print('whoops')

    print('msg = ', msg)
    print(offsets)
    print([msg[i] for i in offsets])
    print('part 1: %d' % (msg[offsets[0]] + msg[offsets[1]] + msg[offsets[2]]))





if __name__ == '__main__':
    main()

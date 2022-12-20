#!/usr/bin/env python3

import sys


def reader():

    numbers = []

    for line in sys.stdin:
        numbers.append(int(line))

    return numbers


def mix_numbers(olist):

    new_nlist = olist[:]

    print('input = %s' % str(olist))

    nlist_len = len(olist)
    ilist = [i for i in range(nlist_len)]

    for i in range(nlist_len):

        n_to_move = olist[i]
        o_pos = ilist.index(i)
        n_pos = (o_pos + n_to_move) % nlist_len

        mov = (o_pos + n_to_move)
        if mov < 0:
            # mov += (2 * nlist_len) - 1
            mov += -1
        elif mov >= nlist_len:
            mov += 1

        n_pos = mov % nlist_len

        print('move %d (pos %d) to position %d' % (n_to_move, o_pos, n_pos))

        if n_to_move == 0:
            print('case no-move')
            continue

        if o_pos == 0:
            print('case 0')
            left = ilist[1:n_pos + 1]
            right = ilist[n_pos + 1:]
            ilist = left + [i] + right
            # print('o_pos 0 l %s r %s' % (left, right))
        elif n_pos == 0:
            # special case: it goes on the end?
            # I think it depends on whether we're moving forward
            # or backward
            if n_to_move > 0:
                print('SAW THIS')
                print('SAW THIS move %d (pos %d) to position %d' % (n_to_move, o_pos, n_pos))
                left = ilist[0:o_pos] + ilist[o_pos + 1:]
                ilist = left + [i]
            else:
                print('SAW THAT move %d (pos %d) to position %d' % (n_to_move, o_pos, n_pos))
                right = ilist[0:o_pos] + ilist[o_pos + 1:]
                ilist = [i] + right
        elif o_pos == nlist_len - 1:
            print('OOPS 1')
            left = ilist[0:n_pos]
            right = ilist[n_pos:-1]
            ilist = left + [i] + right
        elif o_pos < n_pos:
            print('case 1')
            left = ilist[0:o_pos] + ilist[o_pos + 1:n_pos + 1]
            right = ilist[n_pos + 1:]
            # print('left ', left)
            # print('right ', right)
            ilist = left + [i] + right
        elif o_pos > n_pos:
            print('case 2')
            left = ilist[0:n_pos]
            right = ilist[n_pos:o_pos] + ilist[o_pos + 1:]
            # print('left ', left)
            # print('right ', right)
            ilist = left + [i] + right
        else:
            print('OOPS 2 move %d (pos %d) to position %d' % (n_to_move, o_pos, n_pos))

        """
        else:
            print('OOPS2')
            left = ilist[0:o_pos] + ilist[o_pos + 1:n_pos + 1]
            right = ilist[n_pos + 1:]
            ilist = left + [i] + right
        """

        if len(ilist) != len(olist):
            print('WHOOPS')
            return


        #print('ind result ', ilist)
        print('result ', [olist[ilist[i]] for i in range(nlist_len)])
        print('')

    return [olist[ilist[i]] for i in range(nlist_len)]


def main():

    input = reader()

    print(input)

    x = [4, 5, 6, 1, 7, 8, 9]
    x = [1, 2, -3, 3, -2, 0, 4]
    print('%s -> %s' % (str(x), str(mix_numbers(x))))

    msg = mix_numbers(x)
    msg_offset = msg.index(0)
    msg_len = len(msg)
    offsets = [(msg_offset + i * 1000) % msg_len for i in [1, 2, 3]]

    print('part 1: %d' % (msg[offsets[0]] + msg[offsets[1]] + msg[offsets[2]]))




if __name__ == '__main__':
    main()

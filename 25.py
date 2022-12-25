#!/isr/bin/env python3


import sys

class Snafu:

    DIGIT2VAL = {
            '2' : 2,
            '1' : 1,
            '0' : 0,
            '-' : -1,
            '=' : -2
            }

    VAL2DIGIT = {
            2: '2',
            1: '1',
            0: '0',
            -1: '-',
            -2: '=',
            }

    @staticmethod
    def sn2int(text):

        # print('text ', text)

        power = 1
        total = 0

        digits = [c for c in text]
        digits.reverse()
        # print('digits ', digits)

        for digit in digits:
            dval = Snafu.DIGIT2VAL[digit]
            total += power * dval
            power *= 5

        return total

    @staticmethod
    def int2sn(value):

        # this is the tricky part

        power = 1
        digits = []

        while value:
            t_val = value + 2
            rem = (t_val % 5) - 2
            digits.append(rem)
            value //= 5
            if rem < 0:
                value += 1
            power *= 5

        digits.reverse()

        return ''.join([Snafu.VAL2DIGIT[c] for c in digits])


def reader():


    vals = []
    for line in sys.stdin:
        vals.append(Snafu.sn2int(line.strip()))

    return vals


def main():

    vals = reader()
    total = sum(vals)
    # print(vals)
    print('part 1: ', Snafu.int2sn(total))

    """
    print('====')
    for v in vals:
        print('%20s %d' % (Snafu.int2sn(v), v))
    """


if __name__ == '__main__':
    main()



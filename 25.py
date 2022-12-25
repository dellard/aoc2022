#!/isr/bin/env python3

"""
Advent of Code, 2022 -- day 25
"""

import sys


class Snafu:
    """
    Convenience class for the SNAFU decoder/encoder
    """

    # SNAFU digits to their integer equivalents
    #
    DIGIT2VAL = {
            '2' : 2,
            '1' : 1,
            '0' : 0,
            '-' : -1,
            '=' : -2
            }

    # Decimal numbers to their SNAFU digit equivalents
    #
    VAL2DIGIT = {
            2: '2',
            1: '1',
            0: '0',
            -1: '-',
            -2: '=',
            }

    @staticmethod
    def sn2int(text):
        """
        Convert a SNAFU text into an integer
        """

        power = 1
        total = 0

        digits = list(text)
        digits.reverse()

        for digit in digits:
            dval = Snafu.DIGIT2VAL[digit]
            total += power * dval
            power *= 5

        return total

    @staticmethod
    def int2sn(value):
        """
        Convert an integer into a SNAFU text
        """

        power = 1
        digits = []

        while value:
            # this is the tricky part: add 2,
            # then take the mod and subtract 2
            # again, to bring the mod from 0..4
            # to -2..2
            #
            # But then, if this made the remainder
            # "negative", it means that we had to
            # borrow from the modulo of the next
            # higher power, so add it back
            #
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
    """
    Read SNAFU numbers, one per line, from stdin,
    and return list of equivalent integers
    """

    vals = []
    for line in sys.stdin:
        vals.append(Snafu.sn2int(line.strip()))

    return vals


def main():
    """
    Find the test values for day 25
    """

    vals = reader()
    total = sum(vals)
    print('part 1: ', Snafu.int2sn(total))


if __name__ == '__main__':
    main()

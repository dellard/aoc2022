
import sys

totals = list()

current_sum = 0

for l in sys.stdin:

    l = l.strip()
    if not l:
        totals.append(current_sum)
        current_sum = 0
    else:
        current_sum += int(l)

# deal with any leftovers
if current_sum > 0:
    totals.append(current_sum)

# For the first part:
totals = sorted(totals)

print('Part A: %d' % totals[-1])
print('Part B: %d' % sum(totals[-3:]))

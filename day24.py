import sys
from itertools import combinations
import operator
from functools import reduce

def main():
  nums = frozenset(map(int, sys.stdin.readlines()))
  print('part 1: ', next(solve(nums, 3)))
  print('part 1: ', next(solve(nums, 4)))

def solve(xs, n):
  target = sum(xs) // n
  current_min = float('+inf')

  for g in select_group(xs, target):
    xs1 = xs - {g}
    for g2 in select_group(xs1, target):
      candidate = min(product(g), product(g2), product(xs1 - {g2}))
      if candidate < current_min:
        current_min = candidate
        yield current_min

def select_group(xs, s):
  for i in range(len(xs)):
    for c in combinations(xs, i):
      if sum(c) == s:
        yield c

def product(xs):
  return reduce(operator.mul, xs, 1)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()

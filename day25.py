import sys
from itertools import count
from utils import iterate, nth

def main():
  row, col = parse(sys.stdin.readline())
  print('part 1: ', code(row - 1, col - 1))

def code(row, col):
  return nth(iterate(next_code, 20151125), ns(row, col))

def next_code(code):
  return code*252533 % 33554393

"""
   | 0   1   2   3   4   5  
---+---+---+---+---+---+---+
 0 |  0   2   5  9  14  20
 1 |  1   4   8  13  19
 2 |  3   7  12  18
 3 |  6  11  17
 4 | 10  16
 5 | 15
"""

def ns(row, col):
  i = 0
  for m in count(0):
    for x in range(m + 1):
      if x == col and m - x == row:
        return i
      i += 1


def parse(line):
  import re
  return map(int, re.findall(r'\d+', line))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
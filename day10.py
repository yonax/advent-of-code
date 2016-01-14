import sys
from itertools import groupby
from utils import nth, iterate, timereport, count_it

@timereport
def main():
  n = sys.stdin.readline().strip()

  part1 = nth(iterate(las, n), 40)
  print "part 1: ", len(part1)
  print "part 2: ", len(nth(iterate(las, part1), 10))

def las(n):
  return ''.join(str(count_it(g)) + k for k, g in groupby(n))

if __name__ == '__main__':
  main()
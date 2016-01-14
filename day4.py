import sys
from hashlib import md5
from utils import timereport
from itertools import count

@timereport
def main():
  prefix = sys.stdin.readline().strip()

  part1 = solve(prefix, startswith='0'*5)
  print('part 1: ', part1)

  part1 = solve(prefix, startswith='0'*6)
  print('part 2: ', part1)

def solve(prefix, startswith):
  for i in count():
    if md5((prefix + str(i)).encode('utf-8')).hexdigest().startswith(startswith):
      return i

if __name__ == '__main__':
  main()
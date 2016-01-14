import sys
from itertools import groupby
from utils import nth, iterate, timereport, count_it

@timereport
def main():
  sizes = list(map(int, sys.stdin.readlines()))
  nways, used = ways(150, sizes)
  print('part 1: ', nways)
  print('part 2: ', sum(1 for u in used if len(u) == len(min(used, key=len))))

def ways(amount, sizes):
  actual = set()
  def go(amount, usedInPath, used):
    if not amount:
      actual.add(usedInPath)
      return 1
    elif amount > 0 and len(usedInPath) < len(sizes):
      return sum(go(amount - size, usedInPath | {i}, (used.add(usedInPath | {i}), used)[1])
                 for i, size in enumerate(sizes)
                 if i not in usedInPath and (usedInPath | {i}) not in used and amount >= size
                )
    return 0
  return go(amount, frozenset(), set()), actual

if __name__ == '__main__':
  main()
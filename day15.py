import sys
import re
from itertools import combinations
from functools import partial, reduce
from operator import mul
from utils import timereport, pairwise

@timereport
def main():
  ingredients = list(map(parse_line, sys.stdin.readlines()))

  weights = compositions(100, len(ingredients))
  # len(compositions(100, 4)) == 176 851
  totals = list(map(partial(weighted_sum, ingredients), weights))
  
  best = max(totals, key=total)
  print('part 1: ', total(best))

  totals = filter(lambda t: t['calories'] == 500, totals)
  best = max(totals, key=total)
  print('part 2: ', total(best))

def total(d, reject=['calories']):
  return reduce(mul, (v for k, v in d.items() if k not in reject), 1)

def weighted_sum(ingredients, weights):
  """
  >>> a, b = dict(f=1, s=-1), dict(f=5, s=100)
  >>> weighted_sum([a, b], [1, 0]) == dict(f=1, s=0)
  True
  """
  return {k : max(0, sum(i[k]*w for i, w in zip(ingredients, weights)))
          for k in ingredients[0].keys()}

def parse_line(line, pattern=re.compile(r'(\w+) (-?\d)')):
  """
  >>> parse_line('Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9') == \
      dict(capacity=-3, durability=3, flavor=0, texture=0, calories=9)
  True
  """
  return {k:int(v) for k, v in pattern.findall(line)}

# composition       code     c(6, 2)
# 0+0+4         0 0 1 1 1 1    0 1
# 0+1+З         0 1 0 1 1 1    0 2
# 0+2+2         0 1 1 0 1 1    0 3
# ...               ...        ... 
# 3+0+1         1 1 1 0 0 1    3 4
# 3+1+0         1 1 1 0 1 0    3 5
# 4+0+0         1 1 1 1 0 0    4 5
def compositions(n, m):
  """
  >>> len(list(compositions(4, 3)))
  15
  >>> list(compositions(2, 1))
  [(2,)]
  >>> list(compositions(2, 2))
  [(0, 2), (1, 1), (2, 0)]
  """
  for c in combinations(range(n + m - 1), m - 1):
    yield tuple(b-a-1 for a, b in pairwise((-1,) + c + (n+m-1,)))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()

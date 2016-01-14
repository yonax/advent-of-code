import sys
import re
from functools import partial
from operator import ge, le, eq
from utils import find

REF_AUNT = {
  'children': 3,
  'cats': 7,
  'samoyeds': 2,
  'pomeranians': 3,
  'akitas': 0,
  'vizslas': 0,
  'goldfish': 5,
  'trees': 3,
  'cars': 2,
  'perfumes': 1
}

def main():
  aunts = parse(sys.stdin.readlines())
  
  similar = lambda ref, x: all(x.get(k, v) == v for k, v in ref.items())
  best_aunt = find(partial(similar, REF_AUNT), aunts)
  print('part 1:', best_aunt['id'])

  key2cmp = {'cats': ge, 'trees': ge, 'pomeranians': le, 'goldfish': le}
  compare = lambda key, fst, snd: key2cmp.get(key, eq)(fst, snd)
  similar = lambda ref, x: all(compare(k, x.get(k, v), v) for k, v in ref.items())
  best_aunt = find(partial(similar, REF_AUNT), aunts)
  print('part 2:', best_aunt['id'])

def parse(lines):
  return map(parse_line, lines)

def parse_line(line):
  """
  >>> parse_line('Sue 1: goldfish: 9, cars: 0, samoyeds: 9\\n') == \
      {'id': 1, 'samoyeds': 9, 'goldfish': 9, 'cars': 0}
  True
  """
  aunt = dict(id=int(re.match(r'Sue (\d+)', line).group(1)))
  aunt.update((k, int(v)) for k, v in re.findall(r'(\w+): (\d+)', line))
  return aunt
  
if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
import sys
from collections import defaultdict
from itertools import cycle, permutations, starmap
from utils import window, take
from operator import methodcaller

def main():
  happiness, attendees = parse(sys.stdin.readlines())
  print('attendees: ', attendees)
  print('part1: ', max_happiness(happiness, attendees)[1])
  
  ME = "Yes me! Couldnt be! Then who?"
  for a in attendees:
    happiness[a][ME] = 0
    happiness[ME][a] = 0
  attendees.add(ME)
  print('part2: ', max_happiness(happiness, attendees)[1])

def max_happiness(happiness, attendees):
  h = lambda a, b, c: happiness[b][a] + happiness[b][c]
  seating = lambda xs: take(len(attendees), window(cycle(xs), 3))
  total = lambda xs: sum(starmap(h, seating(xs)))
  optimal = max(permutations(attendees), key=total)
  return optimal, total(optimal)


def parse(lines):
  happiness, attendees = defaultdict(dict), set()
  for line in lines:
    a, b, amount = parse_line(line)
    happiness[a][b] = amount
    attendees.add(a)
    attendees.add(b)
  return happiness, attendees

def parse_line(line):
  """
  >>> parse_line('Mallory would gain 91 happiness units by sitting next to David.')
  ('Mallory', 'David', 91)

  >>> parse_line('Alice would lose 2 happiness units by sitting next to Bob.')
  ('Alice', 'Bob', -2)
  """
  a, _, gain_or_lose, amount, *_, b = map(methodcaller('strip', ' .'), line.split())
  return a, b, int(amount)*(-1 if gain_or_lose == 'lose' else 1)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
import sys
import re
from itertools import chain

def main():
  instructions = list(map(parse, sys.stdin.readlines()))

  actions = dict(
    on=lambda x: 1,
    off=lambda x: 0,
    toggle=lambda x: x ^ 1
  )
  print('part 1: ', process(instructions, actions))

  actions = dict(
    on=lambda x: x + 1,
    off=lambda x: max(0, x - 1),
    toggle=lambda x: x + 2
  )
  print('part 2: ', process(instructions, actions))

def process(instructions, actions):
  grid = [[0 for x in range(1000)] for y in range(1000)]
  for action, start, end in instructions:
      execute(grid, actions[action], start, end)

  return sum(chain(*grid))

def execute(grid, action, start, end):
  for x in range(start[0], end[0] + 1):
    for y in range(start[1], end[1] + 1):
      grid[y][x] = action(grid[y][x])

def parse(line):
  """
  >>> parse('turn off 587,176 through 850,273')
  ('off', (587, 176), (850, 273))
  >>> parse('turn on 587,176 through 850,273')
  ('on', (587, 176), (850, 273))
  >>> parse('toggle 587,176 through 850,273')
  ('toggle', (587, 176), (850, 273))
  """
  if line.startswith('turn on'):
    action = 'on'
  elif line.startswith('turn off'):
    action = 'off'
  elif line.startswith('toggle'):
    action = 'toggle'
  else:
    raise Exception('Unexpected input: "{}"'.format(line))
  start, end = map(parse_pair, re.findall(r'\d+,\d+', line))
  return action, start, end

def parse_pair(s):
  """
  >>> parse_pair('587, 176')
  (587, 176)
  >>> parse_pair('850,273')
  (850, 273)
  """
  return tuple(int(x) for x in s.split(','))


if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
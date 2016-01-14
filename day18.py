import sys
from itertools import chain
from utils import iterate, nth, pipe

def main():
  grid = parse(sys.stdin.readlines())

  after100 = nth(iterate(animate, grid), 100)
  print('part1: ', count_on(after100))

  after100 = nth(iterate(pipe(animate, turn_edges), grid), 100)
  print('part1: ', count_on(after100))

DIRS = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))

def animate(grid):
  w, h = len(grid[0]), len(grid)
  fit = lambda x, y: (0 <= x < w) and (0 <= y < h)
  neighbours = lambda x, y: sum(1 for dx, dy in DIRS if fit(x+dx, y+dy) and grid[y+dy][x+dx])
  new = [[0 for c in range(w)] for r in range(h)]
  for y, row in enumerate(grid):
    for x, cell in enumerate(row):
      n = neighbours(x, y)
      new[y][x] = int(n in (2, 3)) if cell else int(n == 3)
  return new

def turn_edges(grid):
  w, h = len(grid[0]), len(grid)
  grid[0][0] = 1
  grid[0][w-1] = 1
  grid[h-1][w-1] = 1
  grid[h-1][0] = 1
  return grid

def count_on(grid):
  return sum(chain(*grid))

def parse(lines):
  return list(map(parse_line, lines))

def parse_line(line):
  """
  >>> parse_line('.#.#.#')
  [0, 1, 0, 1, 0, 1]
  """
  return [1 if c == '#' else 0 for c in line.strip()]

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
import sys
from functools import partial

def main():
  *replacements, (molecule, *_) = map(parse, sys.stdin.readlines())

  distinct = set(generate(replacements, molecule))
  print('part 1: ',  len(distinct))

  neighbours = partial(generate, replacements)
  neighbours2 = partial(generate, [(t, f) for (f, t) in replacements])
  print('part 2: ', greedy(molecule, 'e', neighbours2))

def generate(rs, s):
  for f, t in rs:
    pos = None
    while pos != -1:
      pos = s.find(f, pos + 1 if pos is not None else 0)
      if pos != -1:
        yield s[:pos] + s[pos:].replace(f, t, 1)

def bfs(start, goal, neighbours): # heh :)
  fringe, visited = set([(start, 0)]), set([start])
  while fringe:
    current, pathlen = fringe.pop()
    if current == goal:
      return pathlen

    for neighbour in neighbours(current):
      if neighbour not in visited:
        visited.add(neighbour)
        fringe.add((neighbour, pathlen + 1))

def greedy(start, goal, neighbours): # this works just by accident
  i = 0
  while start != goal:
    start = min(neighbours(start), key=len)
    i += 1
  return i

def parse(line):
  return tuple(map(str.strip, line.split('=>')))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
import sys

def main():
  instructions = sys.stdin.readline().strip()

  part1 = len(santa(instructions))
  print('part 1: ', part1)

  part2 = len(santa(instructions[::2]) | santa(instructions[1::2]))
  print('part 2: ', part2)

def santa(instructions):
  current = (0, 0)
  seen = set([current])

  for instruction in instructions:
    current = advance(current, instruction)
    seen.add(current)

  return seen

def advance(current, where):
  (x, y) = current
  if where == '^':
    return (x, y - 1)
  elif where == 'v':
    return (x, y + 1)
  elif where == '>':
    return (x + 1, y)
  elif where == '<':
    return (x - 1, y)
  raise Exception('Unexpected input %s' % where)

if __name__ == '__main__':
  main()
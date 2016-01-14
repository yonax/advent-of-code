import sys
from operator import methodcaller
from collections import namedtuple

State = namedtuple('State', 'a, b, ip')

def main():
  program = list(map(parse, lines(sys.stdin.readlines())))

  initialState = State(a=0, b=0, ip=0)
  state = execute(program, initialState)
  print('part 1: ', state, state.b)

  initialState = State(a=1, b=0, ip=0)
  state = execute(program, initialState)
  print('part 2: ', state, state.b)

def execute(program, state):
  while state.ip < len(program):
    state = execute_command(program[state.ip], state)
  return state

def execute_command(command, state):
  cmd, r, *maybe_offset = command
  assert r in 'ab' and cmd in ('hlf', 'tpl', 'inc', 'jmp', 'jie', 'jio')

  if cmd == 'hlf':
    return state._replace(ip=state.ip + 1, **{r: getattr(state, r) // 2})
  elif cmd == 'tpl':
    return state._replace(ip=state.ip + 1, **{r: getattr(state, r) * 3})
  elif cmd == 'inc':
    return state._replace(ip=state.ip + 1, **{r: getattr(state, r) + 1})
  elif cmd == 'jmp':
    return state._replace(ip=state.ip + maybe_offset[0])
  elif cmd == 'jie':
    if getattr(state, r) % 2 == 0:
      return state._replace(ip=state.ip + maybe_offset[0])
    else:
      return state._replace(ip=state.ip + 1)
  elif cmd == 'jio':
    if getattr(state, r) == 1:
      return state._replace(ip=state.ip + maybe_offset[0])
    else:
      return state._replace(ip=state.ip + 1)
  raise Exception('SNAFU', command, state)

def parse(line):
  """
  >>> parse('inc a')
  ('inc', 'a')
  >>> parse('jio a, -2')
  ('jio', 'a', -2)
  >>> parse('jmp +23')
  ('jmp', '', 23)
  """
  cmd, r, *maybe_offset = map(methodcaller('strip', ', '), line.split())
  if cmd == 'jmp':
    return (cmd, '', int(r))
  elif maybe_offset:
    return (cmd, r, int(maybe_offset[0]))
  return (cmd, r)

def lines(ls):
  return filter(None, map(lambda l: l.strip(), ls))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
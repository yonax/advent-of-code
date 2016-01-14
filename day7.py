import sys
from collections import namedtuple
from operator import and_, or_
from utils import timereport, memo

@timereport
def main():
  bindings = map(parse, sys.stdin.readlines())
  circuit = {}
  for left, right in bindings:
    circuit[right] = left

  a = evalute(circuit, 'a')
  print('part 1: %s' % a)
  
  circuit['b'] = a
  print('part 2: %s' % evalute(circuit, 'a'))

Binary = namedtuple('Binary', 'op, first, second')
Unary = namedtuple('Unary', 'op, first')

def evalute(circuit, x):
  @memo
  def eval(x):
    if isinstance(x, int):
      return x
    elif isinstance(x, str):
      return eval(circuit[x])
    elif isinstance(x, Binary):
      return op2func[x.op](eval(x.first), eval(x.second))
    elif isinstance(x, Unary):
      return op2func[x.op](eval(x.first))
    else:
      raise Exception('Unexpected %s' % x)

  return eval(x)

def parse(line):
  left, right = map(str.strip, line.split('->'))
  if left.isdigit():
    return int(left), right
  parts = left.split()
  if len(parts) == 1:
    return left, right
  elif len(parts) == 3:
    op = parts[1]
    x = int(parts[0]) if parts[0].isdigit() else parts[0]
    y = int(parts[2]) if parts[2].isdigit() else parts[2]
    return Binary(op, x, y), right

  x = Constant(int(parts[1])) if parts[1].isdigit() else parts[1]
  return Unary(parts[0], x), right

op2func = {
  'AND': and_,
  'OR': or_,
  'LSHIFT': lambda x, s: (x << s) & 0xffff,
  'RSHIFT': lambda x, s: x >> s,
  'NOT': lambda x: 0xffff - x
}


if __name__ == '__main__':
  main()

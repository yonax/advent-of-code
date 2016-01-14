import sys
import json
from numbers import Number

def main():
  obj = json.loads(''.join(sys.stdin.readlines()))
  select = lambda node: isinstance(node, Number)
  reduce = lambda n, acc: acc + n
  reject1 = lambda _: False
  reject2 = lambda x: x == 'red'
  print('part 1: ', walk(obj, select, reduce, reject1, 0))
  print('part 2: ', walk(obj, select, reduce, reject2, 0))

def walk(obj, select, reduce, reject, initial):
  val = initial

  def go(root):
    nonlocal val
    if isinstance(root, list):
      for v in root:
        go(v)
    elif isinstance(root, dict):
      if any(reject(v) for v in root.values()):
        return
      for k, v in root.items():
        go(k)
        go(v)
    elif select(root):
      val = reduce(root, val)

  go(obj)
  return val


if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()

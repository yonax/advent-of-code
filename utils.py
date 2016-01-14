from datetime import datetime
from itertools import islice, count, tee, chain
from collections import deque
from functools import wraps, reduce

def scanl(f, x0, xs):
  """
  scanl(f, xs) == [x0, f(x0, xs[0]), f(f(x0, xs[0]), xs[1]) ...]
  >>> from operator import add
  >>> list(scanl(add, 0, []))
  [0]
  >>> list(scanl(add, 1, [-1]))
  [1, 0]
  >>> list(scanl(add, 0, [1, 2, 3]))
  [0, 1, 3, 6]
  >>> list(scanl(add, 0, [1, 2, 3, 4, 5]))
  [0, 1, 3, 6, 10, 15]
  """
  yield x0
  for x in xs:
    x0 = f(x0, x)
    yield x0

def scanl1(f, xs):
  """
  scanl1(f, xs) == [xs[0], f(xs[0], xs[1]), f(f(xs[0], xs[1]), xs[2]) ...]
  >>> from operator import add
  >>> list(scanl1(add, []))
  []
  >>> list(scanl1(add, [1]))
  [1]
  """
  if xs:
    it = iter(xs)
    x0 = next(it)
    yield from scanl(f, x0, it)

def timereport(f):
  @wraps(f)
  def inner(*args, **kwargs):
    start = datetime.now()
    f(*args, **kwargs)
    end = datetime.now()
    print('{} take {}'.format(f.__name__, end - start))
  return inner

def memo(f):
  cache = {}
  @wraps(f)
  def inner(*args):
    if args not in cache:
      cache[args] = f(*args)
    return cache[args]
  return inner  

def nth(iterable, n, default=None):
  "Returns the nth item or a default value"
  return next(islice(iterable, n, None), default)

def iterate(f, x):
  """
  iterate(f, x) == (x, f(x), f(f(x)), ...)
  >>> take(2, iterate(lambda x: x, 1))
  [1, 1]
  >>> take(3, iterate(lambda x: x + 1, 1))
  [1, 2, 3]
  """
  yield x
  while True:
    x = f(x)
    yield x

def count_it(iterable):
  # 20s - cpython, 4.41s - pypy
  # return len(list(iterable))

  # 22s - cpython, 17s - pypy
  # counter = count()
  # deque(zip(iterable, counter), maxlen=0)
  # return next(counter)

  # 13.9s - cpython, 5s - pypy
  #return sum(1 for item in iterable)

  # and the winner is:
  # 8.64s - cpython, 4.58 - pypy
  count = 0
  for _ignore in iterable:
    count += 1
  return count

def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(map(pred, iterable))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def window(iterable, size=2):
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each, None)
    return zip(*iters)

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def find(f, xs, default=None):
  return next((x for x in xs if f(x)), default)

def find_index(f, xs):
  """
  >>> find_index(lambda x: x > 10, range(20))
  11
  >>> find_index(lambda x: x == 1, range(10, 20))
  -1
  >>> find_index(lambda x: x == 1, [])
  -1
  """
  result = find(lambda t: f(t[1]), enumerate(xs))
  return result[0] if result else -1

def flatten(xs, cons=tuple):
  """
  >>> flatten([(1,), (2,)])
  (1, 2)
  >>> flatten([(1,), (2, 3), (4,)], list)
  [1, 2, 3, 4]
  """
  return cons(chain.from_iterable(xs))

def pipe(*fs):
  """
  >>> inc = lambda x: x + 1
  >>> double = lambda x: x * 2
  >>> pipe(inc, double)(0)
  2
  >>> pipe(double, inc)(0)
  1
  >>> p = pipe(inc, inc)
  >>> pipe(p, double)(0)
  4
  """
  return lambda x: reduce(lambda v, f: f(v), fs, x)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
import sys
import re
from utils import iterate, window, timereport

@timereport
def main():
  password = sys.stdin.readline().strip()
  ps = valid_passwords(password)
  print('part 1: ', next(ps))
  print('part 2: ', next(ps))

def valid(password, pattern=re.compile(r'([a-z])\1.*([a-z])\2')):
  """
  >>> valid('hijklmmn')
  False
  >>> valid('abbceffg')
  False
  >>> valid('abbcegjk')
  False
  >>> valid('abcbbee')
  True
  """
  if any(l in password for l in 'iol'):
    return False
  if not pattern.search(password):
    return False
  for a, b, c in window(to_int_list(password), 3):
    if b - a == 1 and c - b == 1:
      return True
  return False

def next_password(password):
  """
  >>> next_password('a')
  'b'
  >>> next_password('xx')
  'xy'
  >>> next_password('xy')
  'xz'
  >>> next_password('xz')
  'ya'
  >>> next_password('z')
  'aa'
  """
  i = len(password) - 1
  xs = to_int_list(password)

  carry = 1
  while carry:
    if i == -1:
      xs.insert(0, carry // 26)
      break
    xs[i] += 1
    carry = xs[i] // 26
    xs[i] %= 26
    i -= 1

  return from_int_list(xs)

def valid_passwords(start):
  return filter(valid, generate_passwords(start))

def generate_passwords(start):
  return iterate(next_password, start)

def to_int_list(p):
  """
  >>> to_int_list('abc')
  [0, 1, 2]
  """
  return [ord(c) - ord('a') for c in p]

def from_int_list(xs):
  """
  >>> from_int_list([0, 1, 2])
  'abc'
  """
  return ''.join(chr(x + ord('a')) for x in xs)

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()

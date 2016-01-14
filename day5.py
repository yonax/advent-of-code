import sys
import re
from utils import quantify, count_it

def main():
  xs = list(map(str.strip, sys.stdin.readlines()))

  print('part 1: ', count_it(filter(nice, xs)))

  print('part 2: ', count_it(filter(nice2, xs)))

def nice(s, pat=re.compile(r'([a-z])\1')):
  """
  >>> nice('ugknbfddgicrmopn')
  True
  >>> nice('aaa')
  True
  >>> nice('jchzalrnumimnmhp')
  False
  >>> nice('haegwjzuvuyypxyu')
  False
  >>> nice('dvszwmarrgswjxmb')
  False
  """
  # It contains at least three vowels (aeiou only)
  if quantify(s, lambda c: c in 'aeiou') < 3:
    return False
  # It contains at least one letter that appears twice in a row
  if not pat.search(s):
    return False
  if any(bad in s for bad in ('ab', 'cd', 'pq', 'xy')):
    return False
  return True

def nice2(s, p1=re.compile(r'([a-z]{2}).*\1'), p2=re.compile(r'([a-z])[a-z]\1')):
  """
  >>> nice2('qjhvhtzxzqqjkmpb')
  True
  >>> nice2('xxyxx')
  True
  >>> nice2('uurcxstgmygtbstg')
  False
  >>> nice2('ieodomkazucvgmuy')
  False
  """
  return bool(p1.search(s) and p2.search(s))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
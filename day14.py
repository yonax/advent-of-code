import sys
import re
from operator import itemgetter

def main():
  reindeers = list(map(parse, sys.stdin.readlines()))
  model(reindeers, 2503)
  print('part 1: ', max(reindeers, key=itemgetter('distance'))['distance'])
  print('part 2: ', max(reindeers, key=itemgetter('points'))['points'])

def model(reindeers, time):
  for _ in range(time):
    for r in reindeers:
      if r['state'] == 'run':
        r['distance'] += r['speed']
      r['left'] -= 1
      if not r['left']:
        r['state'] = 'run' if r['state'] == 'rest' else 'rest'
        r['left'] = r[r['state']]

    best = max(reindeers, key=itemgetter('distance'))
    best['points'] += 1

def parse(line, pattern=re.compile(r'\d+')):
  """
  >>> parse('Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.') == \
    {'speed': 8, 'run': 8, 'rest': 53, 'state': 'run', 'left': 8, 'distance': 0, 'points': 0}
  True
  """
  d = dict(state='run', distance=0, points=0)
  d.update(zip(['speed', 'run', 'rest'], map(int, pattern.findall(line))))
  d['left'] = d['run']
  return d

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
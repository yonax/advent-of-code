import sys
import re
from collections import namedtuple
from itertools import combinations, product
from functools import partial
from utils import flatten

def main():
  shop = parse_shop(SHOP_INFO)
  hero = Unit(name='Hero', hp=100, damage=0, armor=0)
  boss = Unit(name='Boss', hp=104, damage=8, armor=1)

  restrictions = [('Weapons', 1, 1), ('Armor', 0, 1), ('Rings', 0, 2)]
  equipment_variants = list(distribute(shop, restrictions))

  best = min(filter(partial(can_win, hero, boss, 'Hero'), equipment_variants), key=total_cost)
  print('part 1: ', best, total_cost(best))

  best = max(filter(partial(can_win, hero, boss, 'Boss'), equipment_variants), key=total_cost)
  print('part 2: ', best, total_cost(best))

def total_cost(equipment):
  return sum(item.cost for item in equipment)

def can_win(hero, boss, winner, equipment):
  attacker, defender = equip(hero, equipment), boss
  assert attacker.damage > 0 or defender.damage > 0

  while True:
    defender = fight(attacker, defender)
    if defender.dead:
      break
    attacker, defender = defender, attacker
  # we exit loop on defender's dead
  return defender.name != winner

def equip(unit, equipment):
  damage = sum(item.damage for item in equipment)
  armor = sum(item.armor for item in equipment)
  return unit._replace(damage=unit.damage + damage, armor=unit.armor + armor)

def distribute(items, restrictions):
  """
  >>> shop = parse_shop(SHOP_INFO) # 5 Weapons, 5 Armor, 6 Rings
  >>> len(list(distribute(shop, [('Weapons', 1, 1), ('Armor', 0, 0), ('Rings', 0, 0)])))
  5
  >>> len(list(distribute(shop, [('Weapons', 1, 1), ('Armor', 1, 1), ('Rings', 0, 0)])))
  25
  >>> len(list(distribute(shop, [('Weapons', 1, 1), ('Armor', 0, 1), ('Rings', 0, 2)])))
  660
  """
  gs = [tuple(select(filter(lambda i: i.group == group, items), start, end))
        for group, start, end in restrictions
       ]
  return map(flatten, product(*gs))
  

def select(xs, start, end):
  """
  >>> list(select([], 0, 0))
  [()]
  >>> list(select([1], 0, 1))
  [(), (1,)]
  >>> list(select([1, 2], 0, 1)) 
  [(), (1,), (2,)]
  >>> list(select([1], 1, 1))
  [(1,)]
  >>> list(select([1, 2, 3], 1, 1))
  [(1,), (2,), (3,)]
  >>> list(select(range(1, 4), 0, 2))
  [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3)]
  """
  xs = tuple(xs)
  for i in range(start, end + 1):
    yield from combinations(xs, i)

SHOP_INFO = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

Item = namedtuple('Item', 'group, cost, damage, armor')
class Unit(namedtuple('Unit', 'name, hp, damage, armor')):
  @property
  def dead(self):
    return self.hp <= 0

def fight(attacker, defender):
  """
  >>> fight(Unit('a', hp=100, damage=8, armor=0), Unit('b', hp=100, damage=8, armor=3)).hp == 95
  True
  >>> fight(Unit('a', hp=100, damage=8, armor=0), Unit('b', hp=100, damage=8, armor=8)).hp == 99
  True
  >>> fight(Unit('a', hp=100, damage=8, armor=0), Unit('b', hp=100, damage=8, armor=300)).hp == 99
  True
  """
  damage = max(1, attacker.damage - defender.armor)
  return defender._replace(hp=defender.hp - damage)

def parse_shop(shop_info):
  shop, group = [], None
  for l in filter(None, shop_info.split('\n')):
    if re.match('(\w+):', l):
      group = re.match('(\w+):', l).group(1)
      continue
    item = Item(group, *map(int, re.split(r'\s{2,}', l)[1:]))
    shop.append(item)
  return shop

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  main()
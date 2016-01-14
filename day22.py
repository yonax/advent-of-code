from collections import namedtuple
from operator import itemgetter
import heapq

def main():
  player = Unit('Player', hp=50, mana=500, abilities=PLAYER_ABILITIES)
  boss = Unit('Boss', hp=55, damage=8, abilities=BOSS_ABILITIES)

  state = State(attacker=player, defender=boss)
  result = search(state)
  print('part 1: ', result)

  player = Unit('Player', hp=50, mana=500, abilities=PLAYER_ABILITIES, effects=(DecreasingLife,))
  state = State(attacker=player, defender=boss)
  result = search(state)
  print('part 2: ', result)

def search(initial):
  fringe, visited = PQ([(initial, 0)], key=itemgetter(1)), set([initial])

  while fringe:
    current, mana_spend = fringe.pop()

    if current.is_win('Player'):
      return current, mana_spend
    elif not current.is_win('Boss'):
      working = set([e.name for e in current.attacker.effects] + 
                    [e.name for e in current.defender.effects])
      for ability in current.attacker.abilities:
        if ability.cost > current.attacker.mana or ability.name in working:
          continue
        new_state, ability_used = turn(current, ability)
        if new_state not in visited:
          visited.add(new_state)
          fringe.push((new_state, mana_spend + ability.cost*ability_used))

def turn(state, ability):
  attacker = state.attacker.apply_effects(True)
  if attacker.dead: return State(attacker=state.defender, defender=attacker), False

  defender = state.defender.apply_effects()
  if defender.dead: return State(attacker=defender, defender=attacker), False

  attacker, defender = ability(attacker, defender)
  return State(attacker=defender, defender=attacker), True

class Ability(namedtuple('Ability', 'name, action, cost')):
  def __call__(self, attacker, defender):
    return self.action(attacker, defender)

class Effect(namedtuple('Effect', 'name, timer, on_activate, on_deactivate, tick')):
  def __call__(self, unit, mine=False):
    return self.tick(unit, mine)

  def __repr__(self):
    return "{}x{}".format(self.name, self.timer)

ShieldEffect = Effect(
  name='Shield',
  timer=6,
  on_activate=lambda u: u._replace(armor=u.armor + 7, effects=u.effects + (ShieldEffect,)),
  on_deactivate=lambda u: u._replace(armor=u.armor - 7),
  tick=lambda u, mine: u
)

PoisonEffect = Effect(
  name='Poison',
  timer=6,
  on_activate=lambda u: u._replace(effects=u.effects + (PoisonEffect,)),
  on_deactivate=lambda u: u,
  tick=lambda u, mine: u._replace(hp=u.hp - 3)
)

RechargeEffect = Effect(
  name='Recharge',
  timer=5,
  on_activate=lambda u: u._replace(effects=u.effects + (RechargeEffect,)),
  on_deactivate=lambda u: u,
  tick=lambda u, mine: u._replace(mana=u.mana + 101)
)

DecreasingLife = Effect(
  name='DecreasingLife',
  timer=2**32,
  on_activate=lambda u: u,
  on_deactivate=lambda u: u,
  tick=lambda u, mine: u._replace(hp=u.hp - 1) if mine else u
)

PLAYER_ABILITIES = (
  Ability(
    name='Magic Missile',
    cost=53,
    action=lambda self, other: (self._replace(mana=self.mana - 53), other._replace(hp=other.hp - 4))
  ),
  Ability(
    name='Drain',
    cost=73,
    action=lambda self, other: (self._replace(mana=self.mana - 73, hp=self.hp + 2), other._replace(hp=other.hp - 2))
  ),
  Ability(
    name='Shield',
    cost=113,
    action=lambda self, other: (ShieldEffect.on_activate(self)._replace(mana=self.mana-113), other)
  ),
  Ability(
    name='Poison',
    cost=173,
    action=lambda self, other: (self._replace(mana=self.mana-173), PoisonEffect.on_activate(other))
  ),
  Ability(
    name='Recharge',
    cost=229,
    action=lambda self, other: (RechargeEffect.on_activate(self)._replace(mana=self.mana-229), other)
  ),
)
BOSS_ABILITIES = (
  Ability(
    name='Physical damage', 
    cost=0,
    action=lambda self, other: (self, other._replace(hp=other.hp - max(1, self.damage - other.armor)))
  ),
)

class State(namedtuple('State', 'attacker, defender')):
  def is_win(self, who):
    units = self.attacker, self.defender
    return all(u.alive for u in units if u.name == who) and \
           all(u.dead for u in units if u.name != who)

class Unit(namedtuple('Unit', 'name, hp, mana, damage, armor, abilities, effects')):
  @property
  def alive(self):
    return self.hp > 0

  @property
  def dead(self):
    return not self.alive

  def apply_effects(self, mine_turn=False):
    transient, new_effects = self, []
    for effect in self.effects:
      transient = effect(transient, mine_turn)
      if transient.dead:
        return transient
      if effect.timer - 1 == 0:
        transient = effect.on_deactivate(transient)
      else:
        new_effects.append(effect._replace(timer=effect.timer - 1))
    return transient._replace(effects=tuple(new_effects))

  def __repr__(self):
    return '{}(hp={}, mana={}, armor={}, effects={})'.format(self.name, self.hp, self.mana, self.armor, self.effects)

Unit.__new__.__defaults__ = (0, 0, 0, 0, (), ())

class PQ(object):
  def __init__(self, xs, key):
    self._key = key
    self._heap = []
    self._index = 0
    for x in xs:
      self.push(x)

  def push(self, x):
    heapq.heappush(self._heap, (self._key(x), self._index, x))

  def pop(self):
    return heapq.heappop(self._heap)[-1]

  def __bool__(self):
    return bool(len(self._heap))


if __name__ == '__main__':
  main()
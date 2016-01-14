import sys
from itertools import permutations
from utils import pairwise
from collections import defaultdict

def main():
    distances = parse(sys.stdin.readlines())

    print('part 1: ', tsp(distances))
    print('part 2: ', tsp(distances, max))

def tsp(distances, f=min):
    total = lambda xs: sum(distances[a][b] for a, b in pairwise(xs))
    min_route = f(permutations(distances.keys()), key=total)
    return total(min_route)

def parse(lines):
    d = defaultdict(dict)
    for line in lines:
        a, _, b, _, cost = map(str.strip, line.split())
        d[a][b] = int(cost)
        d[b][a] = int(cost)
    return d

if __name__ == '__main__':
    main()
import sys
from itertools import starmap

def main():
    dims = list(map(parse, sys.stdin.readlines()))
    print('part 1: ', sum(starmap(area, dims)))
    print('part 2: ', sum(starmap(ribbon, dims)))

def area(l, w, h):
    """
    >>> area(2, 3, 4)
    58
    >>> area(1, 1, 10)
    43
    """
    sides = l*w, w*h, h*l
    return sum(side*2 for side in sides) + min(sides)

def ribbon(l, w, h):
    """
    >>> ribbon(2, 3, 4)
    34
    >>> ribbon(1, 1, 10)
    14
    """
    a, b, *_ = sorted((l, w, h))
    return 2*a + 2*b + l*w*h

def parse(line):
    return tuple(int(x) for x in line.split('x'))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()

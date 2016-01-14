import sys
from operator import add
from utils import scanl, find_index

def main():
  seq = sys.stdin.readline().strip()

  num_coded = [1 if c == '(' else -1 for c in seq]

  part1 = sum(num_coded)
  print('part 1: ', part1)

  part2 = find_index(lambda x: x < 0, scanl(add, 0, num_coded))
  print('part 2: ', part2)  

if __name__ == '__main__':
  main()
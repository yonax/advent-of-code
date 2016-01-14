import sys
import ast

def main():
  strings = list(map(str.strip, sys.stdin.readlines()))
  all_sum = sum(len(s) for s in strings)
  
  part1 = sum(len(ast.literal_eval(s)) for s in strings)
  print("part 1: ", (all_sum - part1))
  
  part2 = sum(2+len(s.replace('\\', '\\\\').replace('"', '\\"')) for s in strings)
  print("part 2: ", (part2 - all_sum))

if __name__ == '__main__':
  main()
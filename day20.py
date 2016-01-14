import sys
from utils import timereport

@timereport
def main():
  n = int(sys.stdin.readline())

  print('part 1:', solution(n))
  print('part 2:', solution(n, 11, 50))

def solution(n, m=10, lim=2**32):
  d = n // m
  counts = [0] * d
  for i in range(1, d):
    for j in range(min(d // i, lim)):
      counts[j*i - 1] += i*m
    if counts[i-1] >= n:
      return i

if __name__ == '__main__':
  main()
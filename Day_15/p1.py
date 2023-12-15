from pathlib import Path

HOME = Path(__file__).parent

def _hash(s):
    x = 0
    for c in s:
        x = ((x + ord(c)) * 17) % 256
    return x

with open(HOME/"input.txt") as f:
    print(sum(map(_hash, f.readline().rstrip().split(","))))
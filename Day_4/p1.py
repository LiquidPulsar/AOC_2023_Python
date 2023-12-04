from pathlib import Path

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    tot = 0
    for line in f:
        line = line.split(": ",1)[1]
        left,_,right = line.partition("|")
        l = set(map(int,left.split()))
        r = set(map(int,right.split()))
        if n := len(l & r):
            tot += 1<<(n-1)
    print(tot)
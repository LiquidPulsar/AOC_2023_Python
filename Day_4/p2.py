from pathlib import Path

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    tot = 0
    m = []
    counts = []

    for line in f:
        line = line.split(": ",1)[1]
        left,_,right = line.partition("|")
        l = set(map(int,left.split()))
        r = set(map(int,right.split()))
        n = len(l & r)
        m.append(n)
        counts.append(1)

    for i,n in enumerate(counts):
        tot += n
        for j in range(i+1, i+m[i]+1): counts[j] += n
    print(tot)
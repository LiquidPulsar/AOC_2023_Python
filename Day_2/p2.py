from pathlib import Path
HOME = Path(__file__).parent

from collections import Counter
target = Counter(dict(zip("rgb",range(12,15))))

print(target)
tot = 0
with open(HOME / "test.txt") as f:
    for i,l in enumerate(f,start=1):
        l = l.split(": ",1)[1]
        accum = Counter()
        for turn in l.split("; "):
            count = Counter()
            for c in turn.split(", "):
                amt, col = c.split(" ",1)
                count[col[0]] = int(amt)
            accum |= count
        print(accum)
        tot += accum["r"]*accum["g"]*accum["b"]
    print(tot)

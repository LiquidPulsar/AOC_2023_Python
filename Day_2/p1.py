from pathlib import Path
HOME = Path(__file__).parent

from collections import Counter
target = Counter(dict(zip("rgb",range(12,15))))

print(target)
tot = 0
with open(HOME / "input.txt") as f:
    for i,l in enumerate(f,start=1):
        l = l.split(": ",1)[1]
        for turn in l.split("; "):
            count = Counter()
            for c in turn.split(", "):
                amt, col = c.split(" ",1)
                count[col[0]] = int(amt)
            if not count <= target:
                # print(i, "failed")
                break
        else:
            # print(i, "passed")
            tot += i
    print(tot)

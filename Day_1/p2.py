from pathlib import Path
import re

HOME = Path(__file__).parent

nums = "zero one two three four five six seven eight nine".split()
rep = dict(zip(nums,range(10)))
pat = re.compile(r"(?=(\d|"+r"|".join(nums)+"))")

def replace(m):
    g = m.group(1)
    return rep[g] if g in rep else int(g)

# print(re.findall(pat, "1 two 3 four 5 six 7 eight 9"))
# print(*map(replace,re.findall(pat, "1 two 3 four 5 six 7 eight 9")))

with open(HOME / "input.txt") as f:
    print(
        sum(
            int(
                (d:=[*map(replace,re.finditer(pat, l))]
                )[0]*10+d[-1]
            ) for l in f
        )
    )
from pathlib import Path
from math import ceil,floor

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    t = int("".join(filter(str.isdigit,f.readline())))
    d = int("".join(filter(str.isdigit,f.readline())))

    print(f"Test {t=} {d=}")
    # for s in range(t):
    #     dist = (t-s) * s
    #     if dist>d: print(f"{s}({dist}) ",end="")
    # print()
    l = (t - (t**2 - 4*d)**.5)/2
    r = (t + (t**2 - 4*d)**.5)/2
    # Roots on exact boundary, so shift by epsilon for >
    l = ceil(l + 1e-9)
    r = floor(r - 1e-9)
    print(f"{r-l+1=}")

    print(r-l+1)
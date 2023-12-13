from pathlib import Path
import numpy as np

HOME = Path(__file__).parent

def reflected(pat):
    half_y = pat.shape[0]//2
    # print(half_y,pat.shape)
    for y in range(1,half_y+1):
        # print(pat[:y])
        # print(pat[y:2*y])
        assert pat[:y].shape == pat[2*y-1:y-1:-1].shape, (y, pat[:y].shape, pat[2*y:y-1:-1].shape)
        if (pat[:y]!=pat[2*y-1:y-1:-1]).sum()==1: return y
        # print()
    # print("Second half")
    for y in range(1,half_y+1): # sourcery skip
        # print(pat[-2*y:-y])
        # print(pat[-y:])
        assert pat[-y-1:-2*y-1:-1].shape == pat[-y:].shape, (y, pat[-y-1:-2*y-1:-1].shape, pat[-y:].shape)
        if (pat[-y-1:-2*y-1:-1]!=pat[-y:]).sum()==1: return pat.shape[0]-y
        # print()
    return None

with open(HOME/"input.txt") as f:
    patterns = f.read().split("\n\n")
    # print(patterns)
    tot = 0
    for pat in patterns:
        pat = np.array([*map(list,pat.splitlines())])
        if (n:=reflected(pat)) is not None:
            tot += 100 * n
        elif (n:=reflected(pat.T)) is not None:
            tot += n
        else:
            print("No match",pat)
            break
    print(tot)


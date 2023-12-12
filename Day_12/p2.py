from functools import cache
from pathlib import Path

from tqdm import tqdm

HOME = Path(__file__).parent

def view(f):
    def wrapper(*args,**kwargs):
        res = f(*args,**kwargs)
        tqdm.write(f"{f.__name__}({', '.join(map(repr,args))}) -> {res}")
        return res
    return wrapper

# @view

def solve(pat:str,nums:list[int]):
    @cache
    def can_fit(num:int,p_i:int):
        return num + p_i <= plen \
        and all(c!='.' for c in pat[p_i:p_i+num]) \
       and (num+p_i == plen or pat[p_i+num] != '#')

    plen = len(pat)
    nlen = len(nums)
    last_hash = pat.rfind("#")
    
    @cache
    # @view
    def solve(p_i,n_i):

        if n_i == nlen: return p_i > last_hash
        if p_i >= plen: return 0

        n = nums[n_i]
        if pat[p_i] == "#":
            return solve(p_i+n+1,n_i+1) if can_fit(n,p_i) else 0
        if pat[p_i] == ".":
            return solve(p_i+1,n_i)
        if pat[p_i] == "?":
            return solve(p_i+1,n_i) + solve(p_i+n+1,n_i+1) if can_fit(n,p_i) else solve(p_i+1,n_i)
        assert False
    return solve(0,0)

tot = 0
with open(HOME/"input.txt") as f:
    for i,line in tqdm(list(enumerate(f))):
        pat,nums = line.split()
        pat = "?".join([pat]*5)
        nums = [*map(int,nums.split(","))]*5

        s = solve(pat,nums)
        tqdm.write(str(s))
        tot += s
    print("Part 2:",tot)

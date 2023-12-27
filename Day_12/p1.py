from pathlib import Path

HOME = Path(__file__).parent

def can_fit(num:int,string:str):
    return num <= len(string) \
       and '.' not in string[:num] \
       and (num == len(string) or string[num] != '#')

def view(f):
    def wrapper(*args,**kwargs):
        res = f(*args,**kwargs)
        print(f"{f.__name__}({', '.join(map(repr,args))}) -> {res}")
        return res
    return wrapper

# @view
def solve(pat,nums):

    if not nums: return int('#' not in pat)
    if not pat: return 0

    n,*rest = nums
    if pat[0] == "#":
        return solve(pat[n+1:],rest) if can_fit(n,pat) else 0
    if pat[0] == ".":
        return solve(pat[1:],nums)
    if pat[0] == "?":
        return solve(pat[1:],nums) + solve(pat[n+1:],rest) if can_fit(n,pat) else solve(pat[1:],nums)
    assert False

tot = 0
with open(HOME/"input.txt") as f:
    for line in f:
        pat,nums = line.split()
        nums = [*map(int,nums.split(","))]

        s = solve(pat,nums)
        print(s)
        tot += s
    print("Part 1:",tot)

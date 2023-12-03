from pathlib import Path

HOME = Path(__file__).parent


with open(HOME / "input.txt") as f:
    print(sum(int((d:="".join(filter(str.isdigit,l)))[0]+d[-1]) for l in f))
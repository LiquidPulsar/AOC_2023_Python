from pathlib import Path

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    histories = [[*map(int, line.split())] for line in f]
    tot = 0
    for history in histories:
        lines = [history]
        while any(lines[-1]):
            lines.append([b-a for a, b in zip(lines[-1], lines[-1][1:])])
        col = [line[0] for line in lines]
        s = sum(col[::2]) - sum(col[1::2])
        tot += s
    print(tot)

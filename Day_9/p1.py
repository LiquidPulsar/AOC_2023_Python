from pathlib import Path

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    histories = [[*map(int, line.split())] for line in f]
    tot = 0
    for history in histories:
        lines = [history]
        while any(lines[-1]):
            lines.append([b-a for a, b in zip(lines[-1], lines[-1][1:])])
        tot += sum(line[-1] for line in lines)
    print(tot)

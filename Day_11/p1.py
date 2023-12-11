from pathlib import Path

HOME = Path(__file__).parent

with open(HOME/"input.txt") as f:
    board = [[*line.rstrip()] for line in f]
    W,H = len(board[0]),len(board)

    empty_cols = set(range(W))
    empty_rows = set(range(H))
    galaxies = []
    for y,line in enumerate(board):
        for x,c in enumerate(line):
            if c != ".":
                empty_cols.discard(x)
                empty_rows.discard(y)
                galaxies.append((y,x))

    tot = 0
    for i,g1 in enumerate(galaxies):
        for g2 in galaxies[i+1:]:
            y1,x1 = g1
            y2,x2 = g2
            distancex = abs(x1-x2) + len(empty_cols & set(range(min(x1,x2)+1,max(x1,x2))))
            distancey = abs(y1-y2) + len(empty_rows & set(range(min(y1,y2)+1,max(y1,y2))))
            tot += distancex + distancey
    print(tot)
from pathlib import Path

HOME = Path(__file__).parent

def roll_up(board):
    for row, line in enumerate(board):
        for col, char in enumerate(line):
            if char == "O":
                r = row
                while r>0 and board[r-1][col]==".":
                    board[r-1][col] = "O"
                    board[r][col] = "."
                    r -= 1
    return board

def calc_load(board):
    tot = 0
    for row, line in enumerate(board):
        for char in line:
            if char == "O":
                tot += (len(board)-row)
    return tot

with open(HOME/"input.txt") as f:
    board = [*map(list,f.read().splitlines())]
    print(*board,sep="\n")
    print()
    print(*roll_up(board),sep="\n")
    print()
    print(calc_load(board))

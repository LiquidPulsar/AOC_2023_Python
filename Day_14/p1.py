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
    return sum(
        line.count("O") * (len(board) - row)
        for row, line in enumerate(board)
    )

with open(HOME/"input.txt") as f:
    board = [*map(list,f.read().splitlines())]
    print(*map("".join,board),sep="\n")
    print()
    print(*map("".join,roll_up(board)),sep="\n")
    print()
    print(calc_load(board))

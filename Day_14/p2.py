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
        line.count("O") * (len(board) - row) for row, line in enumerate(board)
    )

END = 1000000000

with open(HOME/"input.txt") as f:
    board = [*map(list,f.read().splitlines())]
    states = {}
    state_list = []
    for i in range(1,END+1): # 1000000001
        states["\n".join(map("".join,board))] = i
        state_list.append(calc_load(board))
        for _ in range(4):
            board = [*map(list,zip(*roll_up(board)[::-1]))]

        if "\n".join(map("".join,board)) in states:
            prev = states["\n".join(map("".join,board))]
            index = prev + (END - i) % (i - prev + 1) - 1
            print(state_list[index])
            break
from pathlib import Path
import re

HOME = Path(__file__).parent

moves = {
    "U": -1j,
    "D": 1j,
    "L": -1,
    "R": 1,
}

hexes  = "RDLU"

with open(HOME/"input.txt") as f:
    dig:dict[complex,list[int|None]] = {} # pos: color
    edges_dug = 0
    pos = 0j
    shoelace = [0j]
    for _,_,col in re.findall(r"([UDLR]) (\d+) \(#(\w+)\)",f.read()):
        length = int(col[:-1],16)
        edges_dug += length
        pos += moves[hexes[int(col[-1],16)]]*length
        shoelace.append(pos)

    area = abs(sum(
        a.real * b.imag
        - b.real * a.imag
        for a,b in zip(shoelace,shoelace[1:])
    )) / 2
    print("Area:", area + edges_dug / 2 + 1) # +1 for the starting square maybe?
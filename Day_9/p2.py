from pathlib import Path

HOME = Path(__file__).parent

with open(HOME/"test.txt") as f:
    pass

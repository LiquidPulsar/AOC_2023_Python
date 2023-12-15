from pathlib import Path

HOME = Path(__file__).parent

def _hash(s):
    x = 0
    for c in s:
        x = ((x + ord(c)) * 17) % 256
    return x


boxes = [{} for _ in range(256)]

with open(HOME/"input.txt") as f:
    for bit in f.readline().rstrip().split(","):
        if bit.endswith("-"):
            label = bit[:-1]
            boxes[_hash(label)].pop(label, None)
        else:
            label = bit[:-2]
            boxes[_hash(label)][label] = int(bit[-1])
    print(*((i,boxes[i]) for i in range(256) if boxes[i]))
    print(sum(i * sum(j*l for j,l in enumerate(box.values(),1)) for i,box in enumerate(boxes,1) if box))
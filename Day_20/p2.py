from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import count
import math
from pathlib import Path

from tqdm import tqdm

HOME = Path(__file__).parent

LOW = False
HIGH = True

@dataclass
class Module:
    typ:str
    name:str
    state:bool
    deps:list[str]

    def pulse(self, pulse:bool, inp:str, todo:deque):
        if self.name in counters and pulse == LOW and self.name not in dcts:
            dcts[self.name] = i
        if self.typ == "%":
            if pulse == LOW:
                self.state = not self.state
                for dep in self.deps:
                    todo.append((dep, self.name, self.state))
            # ignore HIGH pulse
        elif self.typ == "&":
            inputs[self.name][inp] = pulse
            out = not all(inputs[self.name].values())
            for dep in self.deps:
                todo.append((dep, self.name, out))
        elif self.typ == "b":
            for dep in self.deps:
                todo.append((dep, self.name, pulse))
        else:
            raise ValueError("Unknown type",self.typ)

with open(HOME/"input.txt") as f:
    modules = {}
    inputs = defaultdict(dict)

    for line in f:
        name,_,dests = line.rstrip().partition(" -> ")
        dests = dests.split(", ")
        if name[0] == "%":
            name = name[1:]
            modules[name] = Module("%", name, LOW, dests)
        elif name[0] == "&":
            name = name[1:]
            modules[name] = Module("&", name, LOW, dests)
        elif name == "broadcaster":
            modules[name] = Module("b", name, LOW, dests)
        else:
            raise ValueError("Unknown type for",name)
        for dest in dests: inputs[dest][name] = LOW

    # print(modules)
    # import networkx as nx
    # import matplotlib.pyplot as plt
    # G = nx.DiGraph(inputs)
    # nx.draw_networkx(G, with_labels=True)
    # plt.show()


    """
    Graph has a NAND gate with 4 inverted inputs from binary counters
    Find the counters and their cycles.
    Answer is the LCM of the cycles.
    """

    counters = [*inputs[next(iter(inputs["rx"].keys()))].keys()]
    dcts = {}

    print(counters)
    for i in count(1): # sourcery skip
        todo = deque([("broadcaster","button",LOW)])
        inputs["broadcaster"]["button"] = LOW
        while todo:
            name,inp,pulse = todo.popleft()
            # print(inp,"-high->" if pulse else "-low->",name)
            if name in modules: modules[name].pulse(pulse, inp, todo)
        # print(pulses)
        if len(dcts) == len(counters): break
    print(dcts,math.lcm(*dcts.values()))
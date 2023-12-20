from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

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

    pulses = [0,0]
    for _ in range(1000):
        todo = deque([("broadcaster","button",LOW)])
        inputs["broadcaster"]["button"] = LOW
        while todo:
            name,inp,pulse = todo.popleft()
            # print(inp,"-high->" if pulse else "-low->",name)
            pulses[pulse] += 1
            if name in modules: modules[name].pulse(pulse, inp, todo)
        # print(pulses)
    print(pulses[0] * pulses[1])
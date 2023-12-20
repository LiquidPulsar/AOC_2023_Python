from pathlib import Path
import re

from dataclasses import dataclass

HOME = Path(__file__).parent

Xmas = dict[str,int] # letter: val

@dataclass
class Rule:
    letter:str
    direction:str
    threshold:int
    result:str
    def __call__(self, xmas:Xmas) -> str|None:
        if self.direction == "<":
            if xmas[self.letter] < self.threshold:
                return self.result
        elif self.direction == ">":
            if xmas[self.letter] > self.threshold:
                return self.result
        return None
    
    @classmethod
    def from_str(cls, s:str) -> "Rule":
        threshold,result = s[2:].split(":")
        threshold = int(threshold)
        return cls(s[0],s[1],threshold,result)

@dataclass
class Flow:
    name:str
    rules:list[Rule]
    default:str
    def __call__(self, xmas:Xmas) -> str:
        for rule in self.rules:
            if (result := rule(xmas)) is not None:
                return result
        return self.default

with open(HOME/"input.txt") as f:
    a,b = f.read().split("\n\n")
    
    flowdict = {}
    for line in a.splitlines():
        name,_,rest = line[:-1].partition("{")
        *rules,default = rest.split(",")
        flowdict[name] = Flow(name, [*map(Rule.from_str,rules)], default)

    tot = 0
    for xmas in re.findall(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}",b):
        xmas = dict(zip("xmas",map(int,xmas)))
        
        curr = "in"
        while True:
            res = flowdict[curr](xmas)
            if res == "A":
                print("Accepted",sum(xmas.values()))
                tot += sum(xmas.values())
                break
            elif res == "R":
                print("Rejected")
                break
            else:
                curr = res
    print(tot)
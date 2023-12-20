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
    def __call__(self, xmas:Xmas) -> int:
        # print("Rule",self.letter,self.direction,self.threshold,self.result,xmas)
        if self.direction == "<":
            if xmas[self.letter + "l"] < self.threshold: # sourcery skip
                copy = xmas.copy()
                copy[self.letter + "h"] = min(copy[self.letter + "h"], self.threshold-1)
                xmas[self.letter + "l"] = self.threshold
                return solve(self.result, copy)

        elif self.direction == ">":
            if xmas[self.letter + "h"] > self.threshold:
                copy = xmas.copy()
                copy[self.letter + "l"] = max(copy[self.letter + "l"], self.threshold+1)
                xmas[self.letter + "h"] = self.threshold
                return solve(self.result, copy)
        return 0
    
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
    def __call__(self, xmas:Xmas) -> int:
        return sum(rule(xmas) for rule in self.rules) + solve(self.default, xmas)

def solve(curr:str, xmas:Xmas) -> int:
    # print(curr,xmas)
    if curr == "A":
        return (xmas["xh"] - xmas["xl"] + 1) \
             * (xmas["mh"] - xmas["ml"] + 1) \
             * (xmas["ah"] - xmas["al"] + 1) \
             * (xmas["sh"] - xmas["sl"] + 1)
    if curr == "R": # sourcery skip
        return 0
    return flowdict[curr](xmas)

with open(HOME/"input.txt") as f:
    a,b = f.read().split("\n\n")

    flowdict = {}
    for line in a.splitlines():
        name,_,rest = line[:-1].partition("{")
        *rules,default = rest.split(",")
        flowdict[name] = Flow(name, [*map(Rule.from_str,rules)], default)
    print(solve("in", {"xh":4000,"xl":1,
                       "mh":4000,"ml":1,
                       "ah":4000,"al":1,
                       "sh":4000,"sl":1}))

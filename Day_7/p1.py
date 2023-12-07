from collections import Counter
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

HOME = Path(__file__).parent


class Type(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0

    def __lt__(self, other: "Type"):
        return self.value < other.value

    def __repr__(self):
        return self.name.replace("_", " ").title().replace("Of", "of")

class Card(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    T = 10
    J = 11
    Q = 12
    K = 13
    A = 14

    def __lt__(self, other: "Card"):
        return self.value < other.value

    @classmethod
    def parse(cls, s:str) -> "Card":
        return cls[s] if s in 'TJQKA' else cls(int(s))

    def __repr__(self):
        return str(self.value) if self.value < 10 else 'TJQKA'[self.value - 10]

@dataclass
class Hand:
    cards: list[Card]

    def __lt__(self, other: "Hand"):
        return self.score < other.score

    # real scoring
    # @property
    # def score(self):
    #     counts = self.counts
    #     if counts[0][1] == 5:
    #         return (Type.FIVE_OF_A_KIND, *map(fst, counts))
        
    #     if counts[0][1] == 4:
    #         return (Type.FOUR_OF_A_KIND, *map(fst, counts))
        
    #     if counts[0][1] == 3 and counts[1][1] == 2:
    #         return (Type.FULL_HOUSE, *map(fst, counts))

    #     if counts[0][1] == 3:
    #         return (Type.THREE_OF_A_KIND, *map(fst, counts))

    #     if counts[0][1] == counts[1][1] == 2:
    #         return (Type.TWO_PAIR, *map(fst, counts))
        
    #     if counts[0][1] == 2:
    #         return (Type.PAIR, *map(fst, counts))
        
    #     return (Type.HIGH_CARD, *map(fst, counts))

    # camel scoring
    @property
    def score(self) -> tuple[Type, list[Card]]:
        counts = self.counts
        if counts[0][1] == 5:
            return (Type.FIVE_OF_A_KIND, self.cards)
        
        if counts[0][1] == 4:
            return (Type.FOUR_OF_A_KIND, self.cards)
        
        if counts[0][1] == 3 and counts[1][1] == 2:
            return (Type.FULL_HOUSE, self.cards)

        if counts[0][1] == 3:
            return (Type.THREE_OF_A_KIND, self.cards)

        if counts[0][1] == counts[1][1] == 2:
            return (Type.TWO_PAIR, self.cards)
        
        if counts[0][1] == 2:
            return (Type.PAIR, self.cards)
        
        return (Type.HIGH_CARD, self.cards)

    @property
    def counts(self):
        # sort to make sure the highest card is first in a tie
        return sorted(Counter(self.cards).most_common(),key=lambda x:(x[1], x[0]), reverse=True)
    
    @classmethod
    def parse(cls,hand:str):
        cards = [*map(Card.parse,hand)]
        assert len(cards) == 5
        return cls(cards)


with open(HOME/"input.txt") as f:
    lst = []
    for line in f:
        hand,bid = line.split()
        lst.append((Hand.parse(hand),int(bid)))

    lst.sort()
    # for rank, (_, bid) in enumerate(lst,start=1): print(rank, bid)
    tot = sum(rank*bid for rank, (_, bid) in enumerate(lst,1))
    print(*map(lambda x:x[0].score, lst))
    print(*(bid for rank, (_, bid) in enumerate(lst,1)))
    print(tot)
import sys

from typing import Self

CARD_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
CARD_ORDER_JOKER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def rank_value(counts_per_value: list[int]) -> int:
    if counts_per_value == [5]:
        return 6
    if 4 in counts_per_value:
        return 5
    if 3 in counts_per_value and 2 in counts_per_value:
        return 4
    if 3 in counts_per_value:
        return 3
    if counts_per_value.count(2) == 2:
        return 2
    if 2 in counts_per_value:
        return 1
    return 0


class CamelHand:
    def __init__(self, hand: str, jokers: bool = False) -> None:
        hand = hand.split(sep=" ")
        self.bid = int(hand[1])
        self.hand = hand[0]
        self.cards_in_hand = list(set(self.hand))
        if not jokers:
            self.cards_order = [CARD_ORDER.index(card) for card in self.hand]
            self.counts_per_value = [
                self.hand.count(card) for card in self.cards_in_hand
            ]
        else:
            self.cards_order = [CARD_ORDER_JOKER.index(card) for card in self.hand]
            self.counts_per_value = [
                self.hand.count(card) for card in self.cards_in_hand if card != "J"
            ]
            if not self.counts_per_value:
                self.counts_per_value = [5]
            else:
                joker_count = self.hand.count("J")
                max_index = self.counts_per_value.index(max(self.counts_per_value))
                self.counts_per_value[max_index] += joker_count
        self.rank = rank_value(self.counts_per_value)

    def __repr__(self) -> str:
        return f"Hand {self.hand} with bid {self.bid}"

    def __eq__(self, __value: Self) -> bool:
        return self.hand == __value.hand

    def __lt__(self, __value: Self) -> bool:
        return (self.rank, self.cards_order) < (__value.rank, __value.cards_order)

    def __le__(self, __value: Self) -> bool:
        return self.__eq__(__value) or self.__lt__(__value)


def winnings(hands: list[CamelHand]) -> int:
    hands.sort()
    return sum([(index + 1) * hands[index].bid for index in range(len(hands))])


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n")
    hands = [CamelHand(hand) for hand in text]
    print(f"The total winnings are {winnings(hands)}.")
    hands_joker = [CamelHand(hand, jokers=True) for hand in text]
    print(f"The total winnings are {winnings(hands_joker)}.")

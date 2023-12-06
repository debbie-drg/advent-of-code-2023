import sys
import re


def to_set_int(numbers: str) -> set[int]:
    return set([int(element) for element in re.split("\s+", numbers.strip())])


def number_matches(card: str) -> int:
    card = card.split(":")[1]
    winners, numbers = card.split(sep="|")
    winners = to_set_int(winners)
    numbers = to_set_int(numbers)
    combination = winners.intersection(numbers)
    return len(combination)


def card_value(card: str) -> int:
    num_matches = number_matches(card)
    return 0 if not num_matches else 2 ** (num_matches - 1)


def process_pile(cards: list[str]) -> int:
    card_nums = [1 for _ in range(len(cards))]
    for index, card in enumerate(cards):
        num_matches = number_matches(card)
        current_num = card_nums[index]
        for offset in range(num_matches):
            card_nums[index + offset + 1] += current_num
    return sum(card_nums)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n")
    print(f"The pile is worth {sum(map(card_value, text))} points.")
    print(f"The final number of scratchcards is {process_pile(text)}.")

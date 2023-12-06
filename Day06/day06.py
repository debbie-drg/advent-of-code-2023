import sys
import re

from functools import reduce
from operator import mul
from math import ceil, floor


def count_ways_to_win(time: int, record: int) -> int:
    count = 0
    root_part = (time**2 - 4 * record) ** (1 / 2)
    sol_high = floor((time + root_part) / 2 - 1e-10)
    sol_low = ceil((time - root_part) / 2 + 1e-10)
    return sol_high - sol_low + 1


def count_all_races(times: list[int], records: list[int]) -> list[int]:
    return [count_ways_to_win(time, record) for time, record in zip(times, records)]


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n")
    times = [int(item) for item in re.findall("\d+", text[0])]
    records = [int(item) for item in re.findall("\d+", text[1])]
    numbers_win_races = count_all_races(times, records)
    product_number_wins = reduce(mul, numbers_win_races)
    print(f"The product of the ways to win is {product_number_wins}")

    time = int("".join([str(time) for time in times]))
    record = int("".join([str(record) for record in records]))
    number_win_race = count_ways_to_win(time, record)
    print(f"The number of ways to win the big race is {number_win_race}")

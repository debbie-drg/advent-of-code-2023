import sys
from functools import cache
from multiprocessing import Pool


def parse_input(springs_list: list[str]) -> list[tuple[str, tuple[int]]]:
    springs_list = [line.split(sep=" ") for line in springs_list]
    parsed_list = []
    for line in springs_list:
        parsed_list.append(
            (line[0], tuple([int(element) for element in line[1].split(sep=",")]))
        )
    return parsed_list


def times_five_and_count(springs_count: tuple[str, tuple[int]]) -> int:
    spring_map = (5 * (springs_count[0] + "?")).removesuffix("?")
    return count_possibilities((spring_map, 5 * springs_count[1]))


@cache
def count_possibilities(springs_count: tuple[str, tuple[int]]) -> int:
    count = 0
    if not springs_count[1]:
        if "#" in springs_count[0]:
            return 0
        return 1
    if len(springs_count[0]) < springs_count[1][0]:
        return 0
    if not "." in springs_count[0][: springs_count[1][0]]:
        if (
            len(springs_count[0]) == springs_count[1][0]
            or springs_count[0][springs_count[1][0]] != "#"
        ):
            count += count_possibilities(
                (springs_count[0][springs_count[1][0] + 1 :], springs_count[1][1:])
            )
    if springs_count[0][0] != "#":
        count += count_possibilities((springs_count[0][1:], springs_count[1]))
    return count


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    springs_list = open(file_name).read().strip().split(sep="\n")
    springs_list = parse_input(springs_list)
    with Pool(processes=12) as pool:
        print(
            f"The sum of possible arrangements is {sum(pool.map(count_possibilities, springs_list))}"
        )
        print(f"When unfolded, the sum is {sum(pool.map(times_five_and_count, springs_list))}")

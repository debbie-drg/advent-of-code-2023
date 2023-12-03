import sys


def find_symbols(line: str) -> set[int]:
    row_symbols = set()
    for index, element in enumerate(line):
        if not element.isnumeric() and element != ".":
            row_symbols.add(index)
    return row_symbols


def valid_positions(symbol_list: list[int]) -> list[set[int]]:
    row_positions = []
    for index, line in enumerate(symbol_list):
        new_line = set()
        for element in line:
            new_line.update({element - 1, element, element + 1})
        row_positions.append(new_line)
    final_positions = []
    for index in range(len(row_positions)):
        line = set()
        line.update(row_positions[index])
        if index > 0:
            line.update(row_positions[index - 1])
        if index < len(row_positions) - 1:
            line.update(row_positions[index + 1])
        final_positions.append(line)
    return final_positions


def part_numbers(
    input_diagram: list[str], number_positions: list[set[int]]
) -> list[int]:
    parts = []
    for row_pos, line in enumerate(input_diagram):
        number = ""
        part = False
        for col_pos, element in enumerate(line):
            if element.isnumeric():
                number += element
                if col_pos in number_positions[row_pos]:
                    part = True
            else:
                if part:
                    parts.append(int(number))
                    part = False
                number = ""
        if part:
            parts.append(int(number))
    return parts


def find_gears(input_diagram: list[str]) -> int:
    ratio = 0
    number_lines = len(input_diagram)
    for row_index, line in enumerate(input_diagram):
        for col_index, element in enumerate(line):
            if element == "*":
                if row_index == 0:
                    cog = [set() for _ in range(2)]
                    cog[0].add(col_index)
                    adjacent_cog = valid_positions(cog)
                    parts_adjacent_cog = part_numbers(input_diagram[:1], adjacent_cog)
                elif row_index == number_lines - 1:
                    cog = [set() for _ in range(2)]
                    cog[1].add(col_index)
                    adjacent_cog = valid_positions(cog)
                    parts_adjacent_cog = part_numbers(input_diagram[-2:], adjacent_cog)
                else:
                    cog = [set() for _ in range(3)]
                    cog[1].add(col_index)
                    adjacent_cog = valid_positions(cog)
                    parts_adjacent_cog = part_numbers(
                        input_diagram[row_index - 1 : row_index + 2], adjacent_cog
                    )
                if len(parts_adjacent_cog) == 2:
                    ratio += parts_adjacent_cog[0] * parts_adjacent_cog[1]
    return ratio


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n")
    symbol_positions = [find_symbols(line) for line in text]
    number_valid_positions = valid_positions(symbol_positions)
    sum_parts = sum(part_numbers(text, number_valid_positions))
    print(f"The sum of the part numbers is {sum_parts}")
    print(f"The sum of the ratios is {find_gears(text)}")

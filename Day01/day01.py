import sys
import re

NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def calibration_value(line: str) -> int:
    for element in list(line):
        if element.isnumeric():
            value = element
            break
    for element in reversed(list(line)):
        if element.isnumeric():
            return int(value + element)
    return 0


def replace_letters(line: str) -> int:
    found_letters = re.findall(f"(?=(\d|{'|'.join(NUMBERS.keys())}))", line)
    result = ""
    for index in [0, -1]:
        if found_letters[index].isnumeric():
            result += found_letters[index]
        else:
            result += str(NUMBERS[found_letters[index]])
    return int(result)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n")
    computed_value = sum(map(calibration_value, text))
    print(f"The sum of the calibration values is {computed_value}")
    computed_value_letters = sum(map(replace_letters, text))
    print(
        f"The sum of the calibration values swapping letters is {computed_value_letters}"
    )

import sys
import re
from math import lcm

INSTRUCTIONS_MATCH = {"L": 0, "R": 1}


def coordinates_parser(coordinates: str) -> dict:
    coordinates = coordinates.split(sep="\n")
    coordinates_dict = {}
    for line in coordinates:
        coordinate_values = re.findall("[0-9A-Z]+", line)
        coordinates_dict[coordinate_values[0]] = (
            coordinate_values[1],
            coordinate_values[2],
        )
    return coordinates_dict


def number_steps(
    coordinates_dict: dict,
    instructions: str,
    start_node: str = "AAA",
    any_end_Z: bool = False,
) -> int:
    current_node = start_node
    count = 0
    if any_end_Z:
        condition = lambda x: x[-1] != "Z"
    else:
        condition = lambda x: x != "ZZZ"
    while condition(current_node):
        instruction = instructions[count % len(instructions)]
        count += 1
        current_node = coordinates_dict[current_node][INSTRUCTIONS_MATCH[instruction]]
    return count


def ghosts_nodes(coordinates_dict: dict) -> list[str]:
    nodes = []
    for node in coordinates_dict:
        if node[-1] == "A":
            nodes.append(node)
    return nodes


def ghost_navigation(coordinates_dict: dict, instructions: str) -> int:
    nodes = ghosts_nodes(coordinates_dict)
    steps = map(
        lambda node: number_steps(coordinates_dict, instructions, node, True), nodes
    )
    return lcm(*steps)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    instructions, coordinates = open(file_name).read().strip().split(sep="\n\n")
    coordinates_dict = coordinates_parser(coordinates)
    result = number_steps(coordinates_dict, instructions)
    print(f"The number of steeps needed to reach the exit is {result}.")
    ghost_steps = ghost_navigation(coordinates_dict, instructions)
    print(f"The number of steeps needed for the ghosts is {ghost_steps}.")

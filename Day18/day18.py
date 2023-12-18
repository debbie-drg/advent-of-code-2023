import sys

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}
NEIGHBOURS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
DIRECTIONS_CODE = {"0": "R", "1": "D", "2": "L", "3": "U"}


def sum_duples(
    duple_1: tuple[int, int], duple_2: tuple[int, int], times: int
) -> tuple[int, int]:
    return (duple_1[0] + times * duple_2[0], duple_1[1] + times * duple_2[1])


def hexadecimal_instructions_converter(instruction: list[str]) -> tuple[int, str, str]:
    code = instruction[2]
    code, direction = code[:-2], code[-2]
    return [
        DIRECTIONS_CODE[direction],
        int(code.removeprefix("(#"), 16),
        instruction[2],
    ]


class LavaPit:
    def __init__(self, dig_instructions: list[list[str]]) -> None:
        location = (0, 0)
        self.dig_vertices = [(0, 0)]
        self.num_boundary_points = 0
        for instruction in dig_instructions:
            direction, num_steps, _ = instruction
            num_steps = int(num_steps)
            location = sum_duples(location, DIRECTIONS[direction], num_steps)
            self.num_boundary_points += num_steps
            self.dig_vertices.append(location)

    def lava_holding_capability(self) -> int:
        shoelace = 0
        for index in range(len(self.dig_vertices) - 1):
            shoelace += self.dig_vertices[index][0] * self.dig_vertices[index + 1][1]
            shoelace -= self.dig_vertices[index][1] * self.dig_vertices[index + 1][0]
        return (abs(shoelace) + self.num_boundary_points) // 2 + 1


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    instructions = [
        line.split(" ") for line in open(file_name).read().strip().splitlines()
    ]
    lava_pit = LavaPit(instructions)
    print(
        f"The pit can hold {lava_pit.lava_holding_capability()} cubic metters of lava."
    )

    large_instructions = map(hexadecimal_instructions_converter, instructions)
    lava_pit_large = LavaPit(large_instructions)
    print(
        f"The large pit can hold {lava_pit_large.lava_holding_capability()} cubic metters of lava."
    )

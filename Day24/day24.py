import sys
from itertools import combinations
import numpy as np


def parse_stone(stone: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    positions, velocity = stone.split("@")
    positions = tuple(int(pos) for pos in positions.split(","))
    velocities = tuple(int(vel) for vel in velocity.split(","))
    return positions, velocities


def intersection_point(
    stone_1: tuple[tuple[int, int, int], tuple[int, int, int]],
    stone_2: tuple[tuple[int, int, int], tuple[int, int, int]],
) -> tuple[float, float]:
    pos_1, vel_1 = stone_1
    pos_2, vel_2 = stone_2

    if vel_1[0] / vel_2[0] == vel_1[1] / vel_2[1]:  # Parallel, no intersection
        return None, None

    numerator = pos_2[1] - pos_1[1] + (pos_1[0] - pos_2[0]) / vel_2[0] * vel_2[1]
    denominator = vel_1[1] - vel_1[0] * vel_2[1] / vel_2[0]
    parameter_1 = numerator / denominator

    if parameter_1 < 0:  # In the past
        return None, None

    parameter_2 = (pos_1[0] - pos_2[0] + parameter_1 * vel_1[0]) / vel_2[0]

    if parameter_2 < 0:  # In the past
        return None, None

    return pos_1[0] + parameter_1 * vel_1[0], pos_1[1] + parameter_1 * vel_1[1]


def in_range(
    stone_1: tuple[tuple[int, int, int], tuple[int, int, int]],
    stone_2: tuple[tuple[int, int, int], tuple[int, int, int]],
    interval: list[int],
):
    intersection = intersection_point(stone_1, stone_2)
    if intersection == (None, None):
        return 0
    return (
        interval[0] <= intersection[0] <= interval[1]
        and interval[0] <= intersection[1] <= interval[1]
    )


def position_throw_obliterate(
    hail_stones: list[tuple[tuple[int, int, int], tuple[int, int, int]]]
):
    (x0, y0, z0), (vx0, vy0, vz0) = hail_stones[0]
    (x1, y1, z1), (vx1, vy1, vz1) = hail_stones[1]
    (x2, y2, z2), (vx2, vy2, vz2) = hail_stones[2]

    equation_matrix = np.zeros((6, 6), dtype=np.float64)
    vector = np.zeros(6, dtype=np.float64)

    equation_matrix[0, 1] = vz0 - vz1
    equation_matrix[0, 2] = vy1 - vy0
    equation_matrix[0, 4] = z1 - z0
    equation_matrix[0, 5] = y0 - y1

    equation_matrix[1, 0] = vz1 - vz0
    equation_matrix[1, 2] = vx0 - vx1
    equation_matrix[1, 3] = z0 - z1
    equation_matrix[1, 5] = x1 - x0

    equation_matrix[2, 0] = vy0 - vy1
    equation_matrix[2, 1] = vx1 - vx0
    equation_matrix[2, 3] = y1 - y0
    equation_matrix[2, 4] = x0 - x1

    equation_matrix[3, 1] = vz0 - vz2
    equation_matrix[3, 2] = vy2 - vy0
    equation_matrix[3, 4] = z2 - z0
    equation_matrix[3, 5] = y0 - y2

    equation_matrix[4, 0] = vz2 - vz0
    equation_matrix[4, 2] = vx0 - vx2
    equation_matrix[4, 3] = z0 - z2
    equation_matrix[4, 5] = x2 - x0

    equation_matrix[5, 0] = vy0 - vy2
    equation_matrix[5, 1] = vx2 - vx0
    equation_matrix[5, 3] = y2 - y0
    equation_matrix[5, 4] = x0 - x2

    indepx0 = y0 * vz0 - vy0 * z0
    indepx1 = y1 * vz1 - vy1 * z1
    indepx2 = y2 * vz2 - vy2 * z2

    indepy0 = z0 * vx0 - vz0 * x0
    indepy1 = z1 * vx1 - vz1 * x1
    indepy2 = z2 * vx2 - vz2 * x2

    indepz0 = x0 * vy0 - vx0 * y0
    indepz1 = x1 * vy1 - vx1 * y1
    indepz2 = x2 * vy2 - vx2 * y2

    vector[0] = indepx0 - indepx1
    vector[1] = indepy0 - indepy1
    vector[2] = indepz0 - indepz1
    vector[3] = indepx0 - indepx2
    vector[4] = indepy0 - indepy2
    vector[5] = indepz0 - indepz2

    result = np.linalg.solve(equation_matrix, vector)
    return int(np.round(np.sum(result[:3])))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    interval_range = (
        [7, 27] if "example" in file_name else [200000000000000, 400000000000000]
    )
    hail_stones = open(file_name).read().strip().splitlines()
    hail_stones = list(map(parse_stone, hail_stones))
    count = 0
    for stone_1, stone_2 in combinations(hail_stones, 2):
        count += in_range(stone_1, stone_2, interval_range)
    print(f"The number of stones intersecting within the range is {count}")
    print(
        f"You have to throw the stone from a position whose coordinates add up to {position_throw_obliterate(hail_stones)}"
    )

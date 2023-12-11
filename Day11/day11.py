import sys
import re
from itertools import combinations

# from copy import copy


def sum_duples(duple_1: (int, int), duple_2: (int, int)) -> (int, int):
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def manhattan_distance(duple_1: (int, int), duple_2: (int, int)) -> (int, int):
    return abs(duple_1[0] - duple_2[0]) + abs(duple_1[1] - duple_2[1])


class GalaxyMap:
    def __init__(self, galaxy_map: list[str]) -> None:
        self.galaxies = []
        self.empty_rows = []
        self.empty_cols = []
        for index in range(len(galaxy_map[0])):
            if not "#" in [row[index] for row in galaxy_map]:
                self.empty_cols.append(index)
        for row_index, row in enumerate(galaxy_map):
            galaxy_positions = [item.start() for item in re.finditer("#", row)]
            if not galaxy_positions:
                self.empty_rows.append(row_index)
            else:
                for col_index in galaxy_positions:
                    self.galaxies.append((row_index, col_index))

    def pairwise_distances(self, empty_value: int = 2) -> int:
        galaxies = []
        for galaxy in self.galaxies:
            below_row = (empty_value - 1) * sum(
                [empty_row < galaxy[0] for empty_row in self.empty_rows]
            )
            below_col = (empty_value - 1) * sum(
                [empty_col < galaxy[1] for empty_col in self.empty_cols]
            )
            galaxies.append(sum_duples(galaxy, (below_row, below_col)))
        distances = 0
        for combination in combinations(galaxies, 2):
            distances += manhattan_distance(combination[0], combination[1])
        return distances


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n")
    galaxy_map = GalaxyMap(text)
    print(f"The sum of the distances is {galaxy_map.pairwise_distances()}")
    print(
        f"In the even more expanded universe, the sum of distances is {galaxy_map.pairwise_distances(empty_value=1000000)}"
    )

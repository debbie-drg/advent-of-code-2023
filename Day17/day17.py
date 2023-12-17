import sys
from collections import defaultdict
from heapq import heappop, heappush
from math import inf

DIRECTIONS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
INVERSE_DIRECTIONS = {(-1, 0): "N", (1, 0): "S", (0, 1): "E", (0, -1): "W"}
PERP_DIRECTIONS = {
    "N": [(0, 1), (0, -1)],
    "S": [(0, 1), (0, -1)],
    "E": [(1, 0), (-1, 0)],
    "W": [(1, 0), (-1, 0)],
}


def sum_duples(duple_1: tuple[int, int], duple_2: tuple[int, int]) -> tuple[int, int]:
    return (duple_1[0] + duple_2[0], duple_1[1] + duple_2[1])


def min_to_dict(dictionary, key, value):
    try:
        dictionary[key] = min(value, dictionary[key])
    except KeyError:
        dictionary[key] = value


class HeatMap:
    def __init__(self, heat_map: list[str]) -> None:
        self.heat_levels = {}
        self.width = len(heat_map[0])
        self.depth = len(heat_map)
        for row_index, line in enumerate(heat_map):
            for col_index, character in enumerate(line):
                self.heat_levels[(row_index, col_index)] = int(character)

    def best_path(self, min_per_dir_steps: int = 1, max_per_dir_steps: int = 3) -> int:
        costs = defaultdict(lambda: inf)
        goal = (self.depth - 1, self.width - 1)
        queue = [(0, ((0, 0), "E")), (0, ((0, 0), "S"))]
        while queue:
            cost, (position, direction) = heappop(queue)
            if position == goal:
                return cost
            if cost > costs[position, direction]:
                continue
            for inc_dir_x, inc_dir_y in PERP_DIRECTIONS[direction]:
                inc_cost = cost
                for dist in range(1, max_per_dir_steps + 1):
                    new_x, new_y = (
                        position[0] + inc_dir_x * dist,
                        position[1] + inc_dir_y * dist,
                    )
                    if 0 <= new_x < self.depth and 0 <= new_y < self.width:
                        inc_cost += self.heat_levels[(new_x, new_y)]
                        if dist < min_per_dir_steps:
                            continue
                        new_entry = (
                            (new_x, new_y),
                            INVERSE_DIRECTIONS[(inc_dir_x, inc_dir_y)],
                        )
                        if inc_cost < costs[new_entry]:
                            costs[new_entry] = inc_cost
                            heappush(queue, (inc_cost, new_entry))
        return -1


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    heat_map = [
        [int(heat) for heat in line]
        for line in open(file_name).read().strip().splitlines()
    ]
    heat_map = HeatMap(heat_map)
    print(f"The minimum heat cost for part 1 is {heat_map.best_path()}")
    print(f"The minimum heat cost for part 2 is {heat_map.best_path(4,10)}")

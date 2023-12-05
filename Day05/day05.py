import sys


def parser(input_text: str) -> (list[int], list[list[list[int]]]):
    seeds = [int(seed) for seed in input_text[0].split(" ")[1:]]
    range_maps = []
    for element in input_text[1:]:
        current_map = []
        lines = element.split("\n")[1:]
        for line in lines:
            current_map.append([int(number) for number in line.split(" ")])
        current_map.sort(key=lambda x: x[1])  # Sort by start range
        range_maps.append(current_map)
    return seeds, range_maps


def placement(input_location: int, location_map: list[list[int]]) -> int:
    for line in location_map:
        if line[1] <= input_location < line[1] + line[2]:
            return line[0] + input_location - line[1]
    return input_location


def interval_placement(
    input_locations: list[int], location_map: list[list[int]]
) -> list[int]:
    placements = []
    while input_locations:
        start = input_locations.pop(0)
        length = input_locations.pop(0)
        for index, line in enumerate(location_map):
            interval_start = line[1]
            interval_end = line[1] + line[2]
            if interval_start <= start < interval_end:
                remaining_interval_length = interval_end - start
                to_add_length = min(length, remaining_interval_length)
                placements.extend([line[0] + start - interval_start, to_add_length])
                if length > remaining_interval_length:
                    input_locations.extend([interval_end, length - to_add_length])
                break
            elif index == len(location_map) - 1:
                placements.extend([start, length])
            elif start >= interval_end and start < location_map[index + 1][1]:
                next_start = location_map[index + 1][1]
                to_add_length = min(next_start - start, length)
                placements.extend([start, to_add_length])
                if length > to_add_length:
                    input_locations.extend([next_start, length - to_add_length])
                break
    return placements


def seed_placement(input_location: int, location_maps: list[list[list[int]]]) -> int:
    for location_map in location_maps:
        input_location = placement(input_location, location_map)
    return input_location


def seed_interval_placements(
    input_locations: list[int], location_maps: list[list[list[int]]]
) -> list[int]:
    for location_map in location_maps:
        input_locations = interval_placement(input_locations, location_map)
    return input_locations


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    text = open(file_name).read().strip().split(sep="\n\n")
    seeds, range_maps = parser(text)
    final_placements = map(lambda x: seed_placement(x, range_maps), seeds)
    print(f"The minimum placement for the seeds is {min(final_placements)}.")
    interval_placements = seed_interval_placements(seeds, range_maps)
    print(
        f"The minimum location with seeds placed as intervals is {min(interval_placements[::2])}."
    )

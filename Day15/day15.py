import sys


def aoc_hash(input_str: str) -> int:
    return_hash = 0
    for char in input_str:
        return_hash += ord(char)
        return_hash *= 17
        return_hash %= 256
    return return_hash


def hashmap(input_str: str) -> int:
    boxes = [[] for _ in range(256)]
    for instruction in input_str:
        if "=" in instruction:
            label, number = instruction.split("=")
            target_box = aoc_hash(label)
            for lense in boxes[target_box]:
                if label in lense:
                    lense[label] = int(number)
                    break
            else:
                boxes[target_box].append({label: int(number)})
        if "-" in instruction:
            label = instruction.removesuffix("-")
            to_remove = -1
            target_box = aoc_hash(label)
            for index in range(len(boxes[target_box])):
                if label in boxes[target_box][index]:
                    to_remove = index
                    break
            if to_remove != -1:
                boxes[target_box].pop(to_remove)
    focusing_power = 0
    for box_index, box in enumerate(boxes):
        if box:
            box_power = box_index + 1
            for lense_index, lense in enumerate(box):
                focusing_power += (
                    box_power * (lense_index + 1) * list(lense.values())[0]
                )
    return focusing_power


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    strings = open(file_name).read().strip().split(sep=",")
    result = sum(map(aoc_hash, strings))
    print(f"The sum of the hashes is {result}")
    print(f"The focusing power of the lens configuration is {hashmap(strings)}")

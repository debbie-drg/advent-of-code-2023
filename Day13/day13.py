import sys
import numpy as np


def replace_and_parse(mirrors: list[str]) -> list[np.ndarray]:
    return_arrays = []
    for mirror in mirrors:
        mirror = mirror.replace(".", "0")
        mirror = mirror.replace("#", "1")
        mirror = [list(line) for line in mirror.split("\n")]
        mirror = [[int(element) for element in line] for line in mirror]
        return_arrays.append(np.array(mirror, dtype=int))
    return return_arrays


def is_reflection(mirror: np.ndarray, row: int, smudge: bool = False) -> bool:
    tolerance = 1 if smudge else 0
    to_top = mirror.shape[0] - row
    number_rows = min(row, to_top)
    min_row = row - number_rows
    max_row = row + number_rows
    return np.sum(mirror[min_row:row] != mirror[row:max_row][::-1]) == tolerance


def detect_reflections(mirror: np.ndarray, smudge: bool = False) -> int:
    candidate_rows = np.where(np.all(np.diff(mirror, axis=0) == 0, axis=1))[0] + 1
    if smudge:
        candidate_rows = np.concatenate(
            (
                candidate_rows,
                np.where(np.sum(np.diff(mirror, axis=0) != 0, axis=1) == 1)[0] + 1,
            )
        )
    for candidate_row in candidate_rows:
        if is_reflection(mirror, candidate_row, smudge):
            return candidate_row
    return -1


def reflection_detection(mirror: np.ndarray, smudge: bool = False) -> int:
    rows = detect_reflections(mirror, smudge)
    if rows >= 0:
        return 100 * rows
    return detect_reflections(mirror.T, smudge)


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    mirrors = open(file_name).read().strip().split(sep="\n\n")
    mirrors = replace_and_parse(mirrors)
    sum_reflections = sum(map(reflection_detection, mirrors))
    print(f"The sum of the reflections is {sum_reflections}")
    smudge_detection = lambda x: reflection_detection(x, smudge=True)
    smudge_reflections = sum(map(smudge_detection, mirrors))
    print(f"After cleaning the smudges, it's {smudge_reflections}")

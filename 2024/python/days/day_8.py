from collections import defaultdict
from typing import List

from helpers import get_file_data
from itertools import combinations


def part1(data: List[str]):
    grid = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}
    antennas = defaultdict(set)
    antinodes = set()

    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if val != '.':
                antennas[val].add((x, y))

    for key, positions in antennas.items():
        for (x1, y1), (x2, y2) in combinations(positions, 2):
            dx, dy = x1 - x2, y1 - y2
            antinode_pos1, antinode_pos2 = (x1 + dx, y1 + dy), (x2 - dx, y2 - dy)
            antinodes.update({antinode_pos1, antinode_pos2} & grid.keys())

    return len(antinodes)


def part2(data: List[str]):
    grid = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}
    antennas = defaultdict(set)
    antinodes = set()

    def find_along_vector(from_x, from_y, vec_x, vec_y):
        antinode_pos = (from_x + vec_x, from_y + vec_y)

        while antinode_pos in grid:
            antinodes.add(antinode_pos)
            antinode_pos = (antinode_pos[0] + vec_x, antinode_pos[1] + vec_y)

    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if val != '.':
                antennas[val].add((x, y))

    for key, positions in antennas.items():
        for (x1, y1), (x2, y2) in combinations(positions, 2):
            antinodes.update({(x1, y1), (x2, y2)})
            dx, dy = x1 - x2, y1 - y2
            find_along_vector(x1, y1, dx, dy)
            find_along_vector(x2, y2, -dx, -dy)

    return len(antinodes)


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day8_test', decode=True)
    real_data = get_file_data('2024/python/inputs/day8', decode=True)

    assert part1(test_data) == 14
    assert part2(test_data) == 34
    print(f'Part 1 answer: {part1(real_data)}')  # 271
    print(f'Part 2 answer: {part2(real_data)}')  # 994

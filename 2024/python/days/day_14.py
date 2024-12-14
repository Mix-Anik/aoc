from collections import defaultdict
from typing import List

from helpers import get_file_data, ints

MW = 101
MH = 103


def print_grid(grid):
    grid_str = ''
    for y in range(MH):
        for x in range(MW):
            val = len(grid[(x, y)])
            grid_str += str(val) if val else '.'
        grid_str += '\n'

    print(grid_str)


def simulate(grid: dict, seconds: int):
    for _ in range(seconds):
        new_grid = defaultdict(list)

        for (x, y), shift_vectors in grid.items():
            for dx, dy in shift_vectors:
                new_pos = ((x + dx) % MW, (y + dy) % MH)
                new_grid[new_pos].append((dx, dy))

        grid = new_grid

    return grid


def part1(data: List[str]):
    grid = defaultdict(list)

    for robot_data in data:
        pos, vel = [tuple(ints(x[2:].split(','))) for x in robot_data.split()]
        grid[pos].append(vel)

    grid = simulate(grid, 100)
    safety_factor = 1
    middle_x = MW // 2
    middle_y = MH // 2

    for (x_shift, y_shift) in [(0, 0), (middle_x+1, 0), (0, middle_y+1), (middle_x+1, middle_y+1)]:
        quadrant_robots = 0
        for (x, y), val in grid.items():
            if x_shift <= x < (middle_x + x_shift) and y_shift <= y < (middle_y + y_shift):
                quadrant_robots += len(val)
        safety_factor *= quadrant_robots

    return safety_factor


def part2(data: List[str]):
    grid = defaultdict(list)

    for robot_data in data:
        pos, vel = [tuple(ints(x[2:].split(','))) for x in robot_data.split()]
        grid[pos].append(vel)

    sec_elapsed = 0
    while True:
        tree_patterns_detected = 0
        sec_elapsed += 1
        grid = simulate(grid, 1)

        for x, y in grid.keys():
            if (grid.get((x+1, y+1)) and grid.get((x-1, y-1))) or (grid.get((x+1, y-1)) and grid.get((x-1, y+1))):
                tree_patterns_detected += 1

        if tree_patterns_detected > 110:  # manually picked number
            break

    print_grid(grid)
    return sec_elapsed


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day14_test', decode=True)
    real_data = get_file_data('2024/python/inputs/day14', decode=True)

    MW, MH = 11, 7
    assert part1(test_data) == 12
    MW, MH = 101, 103
    print(f'Part 1 answer: {part1(real_data)}')  # 228410028
    print(f'Part 2 answer: {part2(real_data)}')  # 8258

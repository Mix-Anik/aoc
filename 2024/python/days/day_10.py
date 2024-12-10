from typing import List

from helpers import get_file_data


def hike(grid: dict, cur_pos: tuple, cur_height: int):
    if cur_height == 9:
        return [cur_pos]

    branches = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_pos = (cur_pos[0] + dx, cur_pos[1] + dy)
        if next_pos in grid and grid[next_pos] == cur_height + 1:
            branches += hike(grid, next_pos, cur_height + 1)

    return branches


def solve(data: List[str]):
    grid = {(x, y): int(data[y][x]) for y in range(len(data)) for x in range(len(data[y]))}
    trailhead_scores = 0
    trailhead_ratings = 0

    for pos, height in grid.items():
        if height == 0:
            hike_path = hike(grid, pos, 0)
            trailhead_scores += len(set(hike_path))
            trailhead_ratings += len(hike_path)

    return trailhead_scores, trailhead_ratings


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day10_test', decode=True)
    real_data = get_file_data('2024/python/inputs/day10', decode=True)

    part1, part2 = solve(test_data)
    assert part1 == 36
    assert part2 == 81
    part1, part2 = solve(real_data)
    print(f'Part 1 answer: {part1}')  # 548
    print(f'Part 2 answer: {part2}')  # 1252

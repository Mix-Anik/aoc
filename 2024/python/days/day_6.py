import time
from typing import List

from helpers import get_file_data


TURN = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
INCR = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}
step = lambda p, d: tuple(map(sum, zip(p, INCR.get(d))))


def has_loops(grid: dict, pos: tuple, _direction: str, sizex: int, sizey: int):
    cur_pos = pos
    direction = _direction
    visited = set()

    while cur_pos in grid:
        if (*cur_pos, direction) in visited:
            return True

        new_pos = step(cur_pos, direction)

        if grid.get(new_pos) == '#':
            direction = TURN.get(direction)
            continue

        visited.add((*cur_pos, direction))
        cur_pos = new_pos

    return False


def part1(data: List[str]):
    grid = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}
    cur_pos, direction = [(pos, val) for pos, val in grid.items() if val in '><^v'][0]
    visited = set()

    while cur_pos in grid:
        new_pos = step(cur_pos, direction)

        if grid.get(new_pos) == '#':
            direction = TURN.get(direction)
            continue

        visited.add(cur_pos)
        cur_pos = new_pos

    return len(visited)


def part2(data: List[str]):
    grid = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}
    cur_pos, direction = [(pos, val) for pos, val in grid.items() if val in '><^v'][0]
    visited = set()
    loop_positions = 0

    while cur_pos in grid:
        new_pos = step(cur_pos, direction)

        if grid.get(new_pos) == '#':
            direction = TURN.get(direction)
            continue

        _grid = {**grid, new_pos: '#'}
        if new_pos not in visited and has_loops(_grid, cur_pos, direction, len(data[0]), len(data)):
            loop_positions += 1

        visited.add(cur_pos)
        cur_pos = new_pos

    return loop_positions


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day6_test', decode=True)
    real_data = get_file_data('2024/python/inputs/day6', decode=True)

    assert part1(test_data) == 41
    assert part2(test_data) == 6
    print(f'Part 1 answer: {part1(real_data)}')  # 4515
    start = time.time()
    print(f'Part 2 answer: {part2(real_data)}')  # 1309
    print(f'Done in {time.time() - start:.3f} s')

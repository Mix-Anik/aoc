from typing import List

from helpers import get_file_data


def part1(data: List[str]):
    transposed = [''.join(x) for x in zip(*data)]
    grid = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}
    count = 0

    for line in data:
        count += line.count('XMAS') + line.count('SAMX')

    for line in transposed:
        count += line.count('XMAS') + line.count('SAMX')

    for (x, y), val in grid.items():
        if val + grid.get((x+1, y+1), '') + grid.get((x+2, y+2), '') + grid.get((x+3, y+3), '') in ['XMAS', 'SAMX']:
            count += 1
        if val + grid.get((x+1, y-1), '') + grid.get((x+2, y-2), '') + grid.get((x+3, y-3), '') in ['XMAS', 'SAMX']:
            count += 1

    return count


def part2(data: List[str]):
    grid = {(x, y): data[y][x] for y in range(len(data)) for x in range(len(data[y]))}
    count = 0

    for (x, y), val in grid.items():
        cross = (val +
                 grid.get((x+1, y-1), '') +
                 grid.get((x+1, y+1), '') +
                 grid.get((x-1, y+1), '') +
                 grid.get((x-1, y-1), ''))
        if cross in ['AMMSS', 'ASSMM', 'AMSSM', 'ASMMS']:
            count += 1

    return count


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day4_test', decode=True)
    real_data = get_file_data('2024/python/inputs/day4', decode=True)

    assert part1(test_data) == 18
    assert part2(test_data) == 9
    print(f'Part 1 answer: {part1(real_data)}')  # 2344
    print(f'Part 2 answer: {part2(real_data)}')  # 1815

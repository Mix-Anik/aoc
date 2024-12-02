from itertools import pairwise
from typing import List

from helpers import get_file_data, ints


def is_safe(nums: List[int]):
    increasing = nums[0] < nums[1]

    if all(0 < abs(a - b) < 4 and (b > a if increasing else b < a) for a, b in pairwise(nums)):
        return True

    return False


def part1(data: List[bytes]):
    return sum(is_safe(ints(line.split())) for line in data)


def part2(data: List[bytes]):
    count = 0

    for line in data:
        nums = ints(line.split())

        if any(is_safe(nums[0: i] + nums[i + 1:]) for i in range(len(nums))):
            count += 1

    return count


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day2_test')
    real_data = get_file_data('2024/python/inputs/day2')

    assert part1(test_data) == 2
    assert part2(test_data) == 4
    print(f'Part 1 answer: {part1(real_data)}')  # 246
    print(f'Part 2 answer: {part2(real_data)}')  # 318

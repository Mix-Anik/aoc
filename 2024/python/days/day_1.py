from collections import Counter

from helpers import get_file_data, ints


def total_distance(data: bytes):
    total = 0
    nums = ints(data.split())

    for l, r in zip(sorted(nums[::2]), sorted(nums[::-2])):
        total += abs(l - r)

    return total


def total_similarity(data: bytes):
    total = 0
    nums = data.split()
    left = Counter(nums[::2])
    right = Counter(nums[::-2])

    for k, v in left.items():
        total += int(k) * v * right.get(k, 0)

    return total


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day1_test', split_lines=False)
    real_data = get_file_data('2024/python/inputs/day1', split_lines=False)

    assert total_distance(test_data) == 11
    assert total_similarity(test_data) == 31
    print(f'Part 1 answer: {total_distance(real_data)}')  # 1222801
    print(f'Part 2 answer: {total_similarity(real_data)}')  # 22545250

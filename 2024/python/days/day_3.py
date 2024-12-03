import re

from helpers import get_file_data


def part1(data: bytes):
    matched = re.findall(rb'mul\((\d+),\s*(\d+)\)', data)

    return sum(int(a) * int(b) for a, b in matched)


def part2(data: bytes):
    return sum(part1(part) for part in data.split(b'do') if not part.startswith(b"n't()"))


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day3_test', split_lines=False)
    test_p2_data = get_file_data('2024/python/inputs/day3_p2_test', split_lines=False)
    real_data = get_file_data('2024/python/inputs/day3', split_lines=False)

    assert part1(test_data) == 161
    assert part2(test_p2_data) == 48
    print(f'Part 1 answer: {part1(real_data)}')  # 178886550
    print(f'Part 2 answer: {part2(real_data)}')  # 87163705

import time
from itertools import product
from typing import List
from helpers import get_file_data, ints


def solve(data: List[bytes], ops: str):
    total = 0
    data_size = len(data)

    for idx, line in enumerate(data):
        print(f'{idx}/{data_size}')
        wanted_str, nums_str = line.split(b': ')
        wanted = int(wanted_str)
        numbers = ints(nums_str.split())

        for comb in product(ops, repeat=len(numbers) - 1):
            res = numbers[0]
            for num, op in zip(numbers[1:], comb):
                match op:
                    case '|': res = int(f'{res}{num}')
                    case '+': res = res + num
                    case '*': res = res * num
            if res == wanted:
                total += wanted
                break

    return total


def part1(data: List[bytes]):
    return solve(data, '+*')


def part2(data: List[bytes]):
    return solve(data, '+*|')


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day7_test')
    real_data = get_file_data('2024/python/inputs/day7')

    assert part1(test_data) == 3749
    assert part2(test_data) == 11387
    start = time.time()
    print(f'Part 1 answer: {part1(real_data)}')  # 1153997401072
    print(f'P1 Done in: {time.time() - start:.2f} s')
    print(f'Part 2 answer: {part2(real_data)}')  # 97902809384118
    print(f'P2 Done in: {time.time() - start:.2f} s')

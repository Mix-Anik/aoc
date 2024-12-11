from helpers import get_file_data, ints
from functools import lru_cache


@lru_cache(maxsize=None)
def blink(stone: int, iteration: int):
    if iteration == 0:
        return 1

    stone_length = len(str(stone))
    if stone == 0:
        return blink(1, iteration-1)
    elif stone_length % 2 == 0:
        hl = stone_length // 2
        stone_str = str(stone)
        left, right = int(stone_str[:hl]), int(stone_str[hl:])
        return blink(left, iteration-1) + blink(right, iteration-1)

    return blink(stone * 2024, iteration-1)


def solve(data: str, iterations: int):
    stones = ints(data.split())

    return sum(blink(stone, iterations) for stone in stones)


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day11_test', split_lines=False, decode=True).strip()
    real_data = get_file_data('2024/python/inputs/day11', split_lines=False, decode=True).strip()

    assert solve(test_data, 25) == 55312
    print(f'Part 1 answer: {solve(real_data, 25)}')  # 197157
    print(f'Part 2 answer: {solve(real_data, 75)}')  # 234430066982597

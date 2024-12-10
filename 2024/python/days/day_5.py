from collections import defaultdict
from helpers import get_file_data


RULE_MAP = defaultdict(list)


class Page:
    def __init__(self, num: bytes):
        self.num = num

    def __lt__(self, other):
        return other.num in RULE_MAP.get(self.num, [])


def solve(data: bytes):
    rules, updates = data.split(b'\r\n\r\n')
    p1 = p2 = 0

    for rule in rules.split():
        a, b = rule.split(b'|')
        RULE_MAP[a].append(b)

    for update in updates.split():
        pages = update.split(b',')
        fixed = sorted(Page(p) for p in pages)
        incorrect = any(p in RULE_MAP.get(key_page, []) for idx, key_page in enumerate(pages) for p in pages[:idx])

        if incorrect:
            p2 += int(fixed[len(fixed) // 2].num)
        else:
            p1 += int(pages[len(pages) // 2])

    return p1, p2


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day5_test', split_lines=False)
    real_data = get_file_data('2024/python/inputs/day5', split_lines=False)

    part1, part2 = solve(test_data)
    assert part1 == 143
    assert part2 == 123
    part1, part2 = solve(real_data)
    print(f'Part 1 answer: {part1}')  # 5208
    print(f'Part 2 answer: {part2}')  # 6732

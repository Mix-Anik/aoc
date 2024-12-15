from helpers import get_file_data, ints


def solve_system(a, b, p):
    # Ax * a_presses + Bx * b_presses = PrizeX
    # Ay * a_presses + By * b_presses = PrizeY
    b_presses = (p[1] * a[0] - a[1] * p[0]) / (a[0] * b[1] - a[1] * b[0])
    a_presses = (p[0] - b[0] * b_presses) / a[0]

    return a_presses, b_presses


def solve(data: str, increment=0):
    data = data.replace('X+', '').replace('Y+', '').replace('X=', '').replace('Y=', '')
    claw_machines_setups = data.split('\n\n')
    total_tokens = 0

    for setup in claw_machines_setups:
        a, b, prize = [ints(x.split(':')[1].strip().split(', ')) for x in setup.split('\n')]
        prize[0] += increment
        prize[1] += increment
        a_amount, b_amount = solve_system(a, b, prize)

        if not (a_amount.is_integer() and b_amount.is_integer()):
            continue

        total_tokens += int(a_amount) * 3 + int(b_amount)

    return total_tokens


if __name__ == '__main__':
    test_data = get_file_data('2024/python/inputs/day13_test', split_lines=False, decode=True).strip()
    real_data = get_file_data('2024/python/inputs/day13', split_lines=False, decode=True).strip()

    assert solve(test_data) == 480
    print(f'Part 1 answer: {solve(real_data)}')  # 32041
    print(f'Part 2 answer: {solve(real_data, 10000000000000)}')  # 95843948914827

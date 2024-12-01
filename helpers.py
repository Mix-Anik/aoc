from pathlib import Path
from timeit import timeit
from typing import List


def get_file_data(file_name, split_lines=True, decode=False):
    file_abs_path = f'{Path(__file__).parent}/{file_name}.txt'
    encoding = 'UTF-8' if decode else None
    mode = 'r' if decode else 'rb'

    with open(file_abs_path, mode=mode, encoding=encoding) as file:
        if split_lines:
            return file.read().splitlines()

        return file.read()


def ints(lst: List) -> List[int]:
    return [int(x) for x in lst]


def benchmark(times=10000):
    def _decoratpr_wrapper(func):
        def _wrapper(*args, **kwargs):
            res = timeit(lambda: func(*args, **kwargs), number=times)
            print(f'Done in {res:.3f}s')
        return _wrapper
    return _decoratpr_wrapper

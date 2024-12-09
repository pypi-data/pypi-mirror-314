import time
from functools import wraps

import pytest


def timeit(min_seconds=0):
    def test_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            work_time = end_time - start_time
            if work_time > min_seconds:
                print(f"Время выполнения {func.__name__}: {work_time:.4f} секунд")
            return result

        return wrapper

    return test_decorator


@pytest.mark.parametrize("a, b, delay", [(1, 2, 1), (3, 4, 2)])  # Параметризуем тест
@timeit(min_seconds=1)  # Применяем декоратор
def test_slow_sum(a, b, delay):
    time.sleep(delay)
    assert a + b == (a + b)  # Проверяем, что сумма верна


@pytest.mark.parametrize("a, b, delay", [(2, 3, 4), (5, 6, 4)])  # Параметризуем тест
@timeit(min_seconds=3)  # Применяем декоратор
def test_slow_mul(a, b, delay):
    time.sleep(delay)
    assert a * b == (a * b)  # Проверяем, что произведение верно

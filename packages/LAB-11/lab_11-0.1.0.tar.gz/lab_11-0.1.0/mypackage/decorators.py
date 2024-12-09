import time  # Импортируем модуль time для работы с измерением времени (засекаем время выполнения)
from functools import wraps  # позволяет сохранить метаданные оригинальной функции


def timeit(min_seconds=0):  # декоратор принимает параметр min_sec, чтобы установить мин.t выполнения ф-ции
    def decorator(func):  # вложенный декоратор принимает функцию func
        @wraps(func)  # используется внутри декоратора перед внутренней обертывающей функцией
        def wrapper(*args, **kwargs):  # определяем обертку для вызова  декорируемой функции
            start_time = time.time()  # Начало замера времени
            result = func(*args, **kwargs)  # выполняем оригинальную функцию
            end_time = time.time()  # Запоминаем время выполненгия ф-ции
            work_time = end_time - start_time  # Вычисление времени выполнения ф-ции
            if work_time > min_seconds:  # проверяем, превышаетли время выполнения min_seconds
                print(
                    f"Время выполнения {func.__name__}: {work_time:.4f} секунд")  # Выводим время выполнения, если оно больше или равно min_seconds
            return result  # Возвращаем результат функции

        return wrapper  # Возвращаем обертку вместо оригинальной функции

    return decorator  # Возвращаем декоратор


@timeit(min_seconds=1)  # Применяем декоратор к ф-ции slow_sum c мин.временем вып. 1 сек
def slow_sum(a, b, *, delay):
    time.sleep(delay)  # Имитируем задержку выполнения ф-ции
    return a + b  # Возвращаем сумму a+b


@timeit(min_seconds=3)  # Применяем декоратор к ф-ции slow_sum c мин.временем вып. 1 сек
def slow_mul(a, b, *, delay):
    time.sleep(delay)  # Имитируем задержку выполнения ф-ции
    return a * b  # Возвращаем a*b


# Примеры вызова функции slow_sum, slow_mul
print(
    f'Вызов ф-ции slow_sum, c аргументами 1,1, задержкой 1, результат a + b = {slow_sum(1, 1, delay=2)}')  # ожидаем вывод времени, т.к 2>1
print()
print(
    f'Вызов ф-ции slow_mul, c аргументами 4,3, задержкой 1, результат a * b = {slow_mul(4, 3, delay=1)}')  # ожидаем отсутствие вывода времени, т.к. 1<3

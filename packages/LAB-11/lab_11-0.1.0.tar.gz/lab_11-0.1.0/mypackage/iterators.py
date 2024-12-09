class RangeIterator:
    def __init__(self, limit):  # метод инициализации при создании объекта
        self.current = 10  # атрибут экземпляра класса, который используется для отслеживания текущего значения итерации
        self.limit = limit  # Значение self.limit устанавливается в конструкторе __init__, когда создаётся экземпляр класса.Используется для определения границы итерации.

    def __iter__(self):  # метод, который возвращает объект-итератор
        return self

    def __next__(self):  # метод, который извлекает следующий элемент итератора
        if self.current >= self.limit:
            raise StopIteration  # когда итератор достигает предела, инициируем исключение StopIteration, которое автоматически обрабатывается в цикле for.
        current_value = self.current
        self.current += 1  # увеличивает значение атрибута current на 1
        return current_value


# использование итератора
iterator = RangeIterator(15)  # создание экземпляра с пределом 15
for number in iterator:  # итерация по числам
    print(number, end=', ')  # Вывод: 10, 11, 12, 13, 14

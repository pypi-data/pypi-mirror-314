import math  # Импортируем модуль math для математических операций


class ShowAccess:  # Определяем класс дескриптора
    def __init__(self):  # Метод инициализации
        self.value = None  # Инициализируем значение атрибута как None
        self.name = None

    def __get__(self, instance, owner):  # Метод вызывается при доступе к атрибуту
        print(f"Get {self.name} = {self.value}")  # Выводим сообщение о получении значения
        return self.value  # Возвращаем текущее значение атрибута

    def __set__(self, instance, value):  # Метод вызывается при изменении значения атрибута
        self.value = value  # Устанавливаем новое значение атрибута
        print(f"Set {self.name} = {self.value}")  # Выводим сообщение о присвоении значения

    def __delete__(self, instance):  # Метод вызывается при удалении атрибута
        print(f"Delete {self.name} = {self.value}")  # Выводим сообщение об удалении значения
        del self.value  # Удаляем значение атрибута

    def __set_name__(self, owner, name):  # Метод для установки имени атрибута (вызывается автоматически)
        self.name = name  # Сохраняем имя атрибута


class Circle:  # Определяем класс Circle
    radius = ShowAccess()  # Определяем атрибут radius с использованием дескриптора ShowAccess

    def __init__(self, radius):  # Метод инициализации класса Circle
        self.radius = radius  # Устанавливаем значение радиуса через дескриптор

    @property
    def area(self):  # Свойство для вычисления площади круга
        return round(math.pi * self.radius ** 2, 2)  # Возвращаем округлённое значение площади


# Тест
c = Circle(10)  # Создаём экземпляр Circle с радиусом 10
print(f'Area of circle = {c.area}')  # Доступ к свойству area, выводим площадь круга
del c.radius  # Удаляем атрибут radius через дескриптор

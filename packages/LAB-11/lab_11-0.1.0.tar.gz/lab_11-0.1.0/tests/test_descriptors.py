import math


class ShowAccess:
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        print(f"Get {self.name} = {self.value}")
        return self.value

    def __set__(self, instance, value):
        self.value = value
        print(f"Set {self.name} = {self.value}")

    def __delete__(self, instance):
        print(f"Delete {self.name} = {self.value}")
        del self.value

    def __set_name__(self, owner, name):
        self.name = name


class Circle:
    radius = ShowAccess()

    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return round(math.pi * self.radius ** 2, 2)


# Тест
c = Circle(100)
print(f'Area of circle = {c.area}')
del c.radius

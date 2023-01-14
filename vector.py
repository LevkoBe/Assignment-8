import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        number = max(abs(self.x), abs(self.y))
        if number == 0:
            return Vector(0, 0)
        return Vector(self.x / number, self.y / number)


a = Vector(0, 3)
b = Vector(4, 0)
c = a + b
print(a, b, c, a.magnitude(), b.magnitude(), c.magnitude())

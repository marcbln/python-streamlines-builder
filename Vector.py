import math


class Vector:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def normalize_(self) -> None:
        """
        the "_" at the end of the function name is to show that the vector gets modified (like "!" in ruby)
        """
        l = self.length()
        self.x /= l
        self.y /= l

    def normalized(self) -> "Vector":
        """ Returns NEW normalized vector """
        length = self.length()
        return Vector(self.x / length, self.y / length)

    def distanceTo(self, other: "Vector") -> float:
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def asIntTuple(self):
        return (int(round(self.x)), int(round(self.y)))

    def asTuple(self):
        return (self.x, self.y)

    def perpendicularCounterClockwise(self) -> "Vector":
        return Vector(self.y, -self.x)

    def perpendicularClockwise(self) -> "Vector":
        return Vector(-self.y, self.x)

    def __repr__(self) -> str:
        return "({:.2f}, {:.2f})".format(self.x, self.y)

    def __mul__(self, factor) -> "Vector":
        """ multiply with int/float """
        return Vector(self.x * factor, self.y * factor)

    def __truediv__(self, divisor) -> "Vector":
        """ divide with int/float """
        return self.__mul__(1.0 / divisor)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Vector") -> bool:
        return self.x == other.x and self.y == other.y

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def hasZeroLength(self, threshold: float = 1e-8):
        # to avoid floating point error
        return abs(self.x) < threshold and abs(self.y) < threshold

    def isNan(self) -> bool:
        return math.isnan(self.x) or math.isnan(self.y)

    __radd__ = __add__
    __rmul__ = __mul__

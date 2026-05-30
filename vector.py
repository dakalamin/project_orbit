import math


class Vec:
    @classmethod
    def zero(cls):
        return cls(0, 0)
    
    @classmethod
    def one(cls):
        return cls(1, 1)
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x: {self.x} y: {self.y}"
    
    # self + other
    def __add__(self, other: Vec):
        return Vec(
            self.x + other.x, 
            self.y + other.y
        )
    
    # self - other
    def __sub__(self, other: Vec):
        return Vec(
            self.x - other.x, 
            self.y - other.y
        )

    # self * a
    def __mul__(self, a: float):
        return Vec(
            self.x * a,
            self.y * a
        )

    # self / a
    def __truediv__(self, a: float):
        return Vec(
            self.x / a,
            self.y / a
        )

    # -self
    def __neg__(self):
        return self * -1

    # self += other
    def __iadd__(self, other: Vec):
        self.x += other.x
        self.y += other.y
        return self

    # self -= other
    def __isub__(self, other: Vec):
        self.x -= other.x
        self.y -= other.y
        return self

    # self *= a
    def __imul__(self, a: float):
        self.x *= a
        self.y *= a
        return self

    # self /= a 
    def __itruediv__(self, a: float):
        self.x /= a
        self.y /= a
        return self
    
    # self == other
    def __eq__(self, other: Vec):
        return self.x == other.x and self.y == other.y
    
    # self != other
    def __ne__(self, other: Vec):
        return not self == other
    
    def rotate(self, angle_radians: float):
        return Vec(
            math.cos(angle_radians) * self.x - math.sin(angle_radians) * self.y,
            math.sin(angle_radians) * self.x + math.cos(angle_radians) * self.y
        )

    @property
    def dist_sq(self):
        return math.pow(self.x, 2) + math.pow(self.y, 2)

    @property
    def dist(self):
        return math.sqrt(self.dist_sq)
    
    @property
    def norm(self):
        return self / self.dist
    
    def copy(self):
        return Vec(self.x, self.y)
    
    def to_tuple(self):
        return (self.x, self.y)

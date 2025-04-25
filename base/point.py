
import numpy as np


class Point2D(np.ndarray):
    def __new__(cls, x: float, y: float):
        obj = np.array([x, y]).view(cls)
        return obj

    def __eq__(self, other: 'Point2D'):
        return np.array_equal(self, other)

    def __hash__(self):
        return hash(tuple(self))

    def __str__(self):
        return f"({self[0]}, {self[1]})"

    def __add__(self, other: 'Point2D'):
        return np.add(self, other).view(Point2D)

    def __sub__(self, other: 'Point2D'):
        return np.subtract(self, other).view(Point2D)

    def __mul__(self, other: float):
        return np.multiply(self, other).view(Point2D)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

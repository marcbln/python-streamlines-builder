import math
from typing import List

from LookupGridCell import LookupGridCell
from Vector import Vector


class BoundingBox:
    """
    helper class
    """
    def __init__(self, x0: float, y0: float, w: float, h: float):
        self.topLeft = Vector(x0, y0)
        self.width = w
        self.height = h

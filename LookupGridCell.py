import math
from typing import List

from Vector import Vector


class LookupGridCell:
    """
    a cell is a bucket of points (of already generated streamlines) which are inside this cell
    Each cell contains a list of pointers to the sample points located with the cell.
    """
    def __init__(self):
        self.samplePoints: List[Vector] = [] # list of sample points located within the cell

    def addSamplePoint(self, point: Vector):
        # former "occupy()"
        self.samplePoints.append(point)

    def checkDistance(self, pt: Vector, minDistance: float) -> bool:
        """
        returns True if all points inside this cell have distance to passed pt >= minDistance, False otherwise
        """
        for sample in self.samplePoints:
            # print(f"-sample.distanceTo(pt): {sample.distanceTo(pt)}")
            if sample.distanceTo(pt) < minDistance:
                # print(f"######FALSE {pt}", sample.distanceTo(pt))
                return False

        # print(f"######TRUE {pt}, {minDistance})")
        return True

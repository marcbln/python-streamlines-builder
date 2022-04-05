import math
from typing import List

from BoundingBox import BoundingBox
from LookupGridCell import LookupGridCell
from Vector import Vector


class LookupGrid:

    def __init__(self, bbox: BoundingBox, dSep: float):
        self.bbox: BoundingBox = bbox
        self.dSep: float = dSep

        self.numCols: int = math.ceil(bbox.width / dSep)
        self.numRows: int = math.ceil(bbox.height / dSep)

        # 2d array LookupGridCell[numRows][numCols]:
        self.cells: List[List[LookupGridCell]] = [[LookupGridCell() for x in range(self.numCols)] for y in
                                                  range(self.numRows)]

    def gridX(self, x) -> int:
        return math.floor((x-self.bbox.topLeft.x) / self.dSep)

    def gridY(self, y) -> int:
        return math.floor((y-self.bbox.topLeft.y) / self.dSep)

    def addSamplePoint(self, point: Vector):
        # was occupyCoordinates()
        # unused, but could be used to build "currentStreamlineGrid" for checking for self-intersection
        self.findCell(point).addSamplePoint(point)

    def addStreamline(self, streamline: List[Vector]):
        # aka addSamplePoints()
        # add sample points of a full streamline to the cells
        for pt in streamline:
            self.findCell(pt).addSamplePoint(pt)

    def _assertInBounds(self, pt: Vector):
        """
        internal helper
        """
        if pt.x < self.bbox.topLeft.x or pt.x > self.bbox.topLeft.x + self.bbox.width - 1:
            raise Exception(f'x {pt.x} is out of bounds')
        if pt.y < self.bbox.topLeft.y or pt.y > self.bbox.topLeft.y + self.bbox.height - 1:
            raise Exception(f'y {pt.y} is out of bounds')

    def findCell(self, point: Vector) -> LookupGridCell:
        self._assertInBounds(point)
        gridX = self.gridX(point.x)
        gridY = self.gridY(point.y)

        return self.cells[gridY][gridX]


    def _isOutside(self, pt: Vector) -> bool:
        """
        internal helper
        """
        return pt.x < self.bbox.topLeft.x or pt.x > self.bbox.topLeft.x + self.bbox.width - 1 or \
               pt.y < self.bbox.topLeft.y or pt.y > self.bbox.topLeft.y + self.bbox.height - 1


    def isPointValid(self, pt: Vector, minDistance: float) -> bool:
        """
        1st) checks if pt is inside ouf bounds of the grid
        2nd) returns True if all points inside this grid have distance to passed pt >= minDistance, False otherwise
        """
        if self._isOutside(pt):
            return False

        # print("--")
        cx: int = self.gridX(pt.x) # TODO: make function _getGridXY (returning Tuple with idxCol, idxRow)
        cy: int = self.gridY(pt.y)
        for idxCol in [cx - 1, cx, cx + 1]:
            if idxCol < 0 or idxCol >= self.numCols:
                continue

            for idxRow in [cy - 1, cy, cy + 1]:
                if idxRow < 0 or idxRow >= self.numRows:
                    continue
                # print(f"--- minDistance: {minDistance}")
                if not self.cells[idxRow][idxCol].checkDistance(pt, minDistance):
                    # print("-------- isPointValid: True")
                    return False

        return True

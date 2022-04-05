import math
from typing import Callable, List, Union

from BoundingBox import BoundingBox
from LookupGrid import LookupGrid
from StreamlineIntegrator import StreamlineIntegrator
from Vector import Vector


class StreamlineGenerator:

    # defaults..
    DEFAULT_D_SEP = 20
    DEFAULT_D_TEST_FACTOR = 0.333 # dTest = dSep * DEFAULT_D_TEST_FACTOR
    DEFAULT_TIME_STEP = 1.0 # the approx. length of a streamline oof a single time step

    def __init__(self, flowFieldFunction: Callable, dSep: float=None, dTest: float=None, stepSize:float=DEFAULT_TIME_STEP):
        self._finishedStreamlineIndexes: List[int] = None
        self.d_sep = self.DEFAULT_D_SEP if dSep is None else dSep
        self.d_test = dTest if dTest is not None else dSep * self.DEFAULT_D_TEST_FACTOR # dTest is the the distance (to other streamlines) where streamline generation stops
        self._flowFieldFunction: Callable = flowFieldFunction
        self._streamlines: List[List[Vector]] = None
        self._lookupGrid: LookupGrid = None
        self._stepSize = stepSize


    def vectorFieldNormalized(self, coords: Vector) -> Union[Vector,None]:
        """
        the vector field, but every vector has same length of 1
        this is a callback passed to runge-kutta
        """
        p2: Vector = self._flowFieldFunction(coords)

        if p2 is None:
            return None

        if p2.isNan():
            return None # Not defined. e.g. Math.log(-1)

        # We need normalized field.
        l_squared = p2.x ** 2 + p2.y ** 2
        if l_squared == 0:
            return None # singularity
        l = math.sqrt(l_squared)

        return Vector(p2.x / l, p2.y / l)





    def _getSeedpoint(self, idxStreamline: int) -> Union[Vector, None]:
        """
        private helper
        """
        for pointOnStreamline in self._streamlines[idxStreamline]:
            #  make points orthogonal to streamline with distance = D_SEP / -D_SEP
            perpendicular = self.vectorFieldNormalized(pointOnStreamline).perpendicularClockwise()
            candidate = pointOnStreamline + perpendicular * self.d_sep
            if self._lookupGrid.isPointValid(candidate, self.d_sep):
                return candidate

            candidate = pointOnStreamline + perpendicular * (-self.d_sep)
            if self._lookupGrid.isPointValid(candidate, self.d_sep):
                return candidate

        return None


    def _findNextSeedPoint(self) -> Union[Vector, None]:
        for idxStreamline in reversed(range(len(self._streamlines))): # TODO: mark streamlines that have no seedpoint candidates and skip them

            if idxStreamline in self._finishedStreamlineIndexes:
                continue

            seedPoint = self._getSeedpoint(idxStreamline)

            if seedPoint is None:
                self._finishedStreamlineIndexes.append(idxStreamline)

            if seedPoint is not None:
                return seedPoint

        return None # no more seed points found - we are done


    def setStepSize(self, stepSize: float):
        """
        default stepSize is 1.0
        """
        self._stepSize = stepSize



    def buildStreamlines(self, bbox: BoundingBox, initialStreamline: Vector) -> List[List[Vector]]:
        """
        the main function
        """
        # ---- init objects
        self._lookupGrid = LookupGrid(bbox, self.d_sep)
        self._streamlines = []
        self._finishedStreamlineIndexes = []
        streamlineIntegrator = StreamlineIntegrator(self.vectorFieldNormalized, self._lookupGrid, self._stepSize, self.d_test)

        # ---- initial streamline
        seedPoint = initialStreamline
        while seedPoint is not None:
            print(f"streamlineIntegrator.buildStreamline...{seedPoint}")
            sl = streamlineIntegrator.buildStreamline(seedPoint)
            self._lookupGrid.addStreamline(sl)
            self._streamlines.append(sl)
            #print(f"streamline: {sl}\n---------------------------------\n")

            # ---- find next seed point
            seedPoint = self._findNextSeedPoint()
            print(f"next seed point: {seedPoint}")

        return self._streamlines
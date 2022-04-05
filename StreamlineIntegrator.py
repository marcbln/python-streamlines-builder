import math
from typing import List,Union
import numpy as np
import typing

from LookupGrid import LookupGrid
from Vector import Vector
from rk4 import rk4


def isSame(a: float, b: float) -> bool:
    # to avoid floating point error
    return abs(a - b) < 1e-4




class StreamlineIntegrator:
    """
    for "integrating" (building) a single streamline
    03/2022 created
    """

    STEP_SIZE_FACTOR_TERMINATION_CONDITION = 0.9 # this constant could be changed to a member variable, but currently not really needed


    # ---- status enums
    FORWARD = 1
    BACKWARD = 2
    DONE = 3



    def __init__(self,
                 vectorFieldNormalized: typing.Callable,
                 grid: LookupGrid,
                 stepSize: float,  # from config TODO: default to 1.0 and add method setStepSize()
                 # dSep: float,
                 dTest: float # needed to decide when to end streamline "integration"
    ):
        #self.vectorField: typing.Callable = vectorField
        self.vectorFieldNormalized: typing.Callable = vectorFieldNormalized
        self.grid: LookupGrid = grid
        self.stepSize: float = stepSize # from config
        self.streamlinePoints: List[Vector] = None

        # streamlinePoints: List[Vector] = None # aka theResult aka streamline aka points
        self.pos: Vector = None # TODO: remove. pass pos to the functions which need it
        # self.start: Vector = None
        #self.dSep = dSep # from config
        self.dTest = dTest # from config # needed to decide when to end streamline "integration"
        # self.state: int = None # FORWARD / BACKWARD / DONE



    def buildStreamline(self, start: Vector) -> List[Vector]:
        """
        the MAIN function
        """

        # ---- add first point
        self.streamlinePoints = [start] # aka theResult aka streamline aka points
        self.pos = start
        state = self.FORWARD # FORWARD / BACKWARD / DONE (TODO: rename?)

        # ---- add points to the streamline
        while state != self.DONE:
            # print(f".{state}", end='')
            # -- forward
            if state == self.FORWARD:
                point = self._grow(self.stepSize)
                if point is not None:
                    self.streamlinePoints.append(point)
                    self.pos = point
                else:
                    # Reset self.position to start, and grow backwards:
                    self.pos = start
                    state = self.BACKWARD

            # -- backward
            if state == self.BACKWARD:
                point = self._grow(-self.stepSize)
                if point is not None:
                    self.streamlinePoints.insert(0, point)
                    self.pos = point
                else:
                    state = self.DONE

        return self.streamlinePoints




    def _grow(self, stepSize: float) -> Union[Vector, None]:
        """
        private helper
        """
        #print("_growForward")
        velocity = rk4(self.pos, stepSize, self.vectorFieldNormalized)
        #print(f"gf:{velocity}", end="")
        if velocity is None or velocity.hasZeroLength(1e-8):
            # print(f"singulariy 1: {velocity}")
            return None # Hit the singularity.
        # print("-")

        candidate: Vector = self.pos + velocity

        # if self.grid.isOutside(candidate.x, candidate.y):
        #     # TODO: add clipped point
        #     return None

        # ---- did we hit our current streamlinePoints (hack to avoid infinite ping-pong)?
        for existingPt in self.streamlinePoints:
            if existingPt.distanceTo(candidate) <= abs(stepSize) * self.STEP_SIZE_FACTOR_TERMINATION_CONDITION:
                return None

        # ---- is point not too near to some of the previous existing streamlines, then it is valid point
        if self.grid.isPointValid(candidate, self.dTest):
            return candidate

        return None


    # def stepSizeCheck(self, distanceToCandidate: float) -> bool:
    #     # this is a callback function
    #     return distanceToCandidate < self.stepSize * 0.9
    #
    #
    # def checkDTest(self, distanceToCandidate: float) -> bool:
    #     # this is a callback function
    #     if isSame(distanceToCandidate, self.dTest):
    #         return False
    #     return distanceToCandidate < self.dTest
    #
    #
    # def checkDSep(self, distanceToCandidate: float) -> bool:
    #     # this is a callback function
    #     if isSame(distanceToCandidate, self.dSep):
    #         return False
    #     return distanceToCandidate < self.dSep



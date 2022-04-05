#!/usr/bin/env python3.7
import math
from typing import List, Union, Callable
import numpy as np

from pysvg.builders import ShapeBuilder
from pysvg.builders import StyleBuilder
from pysvg.structure import Svg

from BoundingBox import BoundingBox
from StreamlineGenerator import StreamlineGenerator
from Vector import Vector


"""
   
ALGORITHM
=========

Compute an initial streamline and put it into the queue
Let this initial streamline be the current streamline
bFinished = False   

REPEAT
    REPEAT
        Select a candidate seedpoint at d = d_sep apart from the current streamline
    UNTIL the candidate is valid OR there is no more available candidate
    IF a valid candidate has been selected THEN
        Compute a new streamline and put it into the queue
    ELSE
        IF there is no more available streamline in the queue THEN
            bFinished = True
        ELSE
            Let the next streamline in the queue be the current streamline   
        ENDIF
    ENDIF
UNTIL bFinished == True

"""




def toSvgPolylines(bbox: BoundingBox, streamlines: List[List[Vector]], pathDestFile: str):
    """
    write monochrome streamlines to a svg file for visualization
    pip3 install pysvg-py3
    """


    # ---- build svg
    mySVG = Svg(width=bbox.width, height=bbox.height, viewBox=f"{bbox.topLeft.x} {bbox.topLeft.y} {bbox.width} {bbox.height}")
    shapeBuilder = ShapeBuilder()
    styleBuilder = StyleBuilder()
    styleBuilder.setStroke('blue')
    styleBuilder.setFilling('none')
    styleBuilder.setStrokeWidth('1px')
    styleBuilder.setStrokeLineCap('round')

    # background
    mySVG.addElement(shapeBuilder.createRect(x=bbox.topLeft.x, y=bbox.topLeft.y, width="100%", height="100%", fill="white", stroke='none'))

    # streamlines
    for sl in streamlines:
        polyline = shapeBuilder.createPolyline(shapeBuilder.convertTupleArrayToPoints([pt.asTuple() for pt in sl]))
        polyline.set_style(styleBuilder.getStyle())
        mySVG.addElement(polyline)

    # save svg
    print(f"writing {pathDestFile} ...")
    mySVG.save(pathDestFile)


def toSvgWithVelocityColors(bbox: BoundingBox, streamlines: List[List[Vector]], field: Callable, pathDestFile: str):
    """
    write streamlines to a svg file for visualization with colors encoded velocity
    pip3 install pysvg-py3
    :param bbox:
    :param streamlines:
    :param field: the original vector field (not the normalized)
    :return:
    """

    # ---- get vector lengths (aka skalar velocity) over all streamline points
    lengths = [[field(pt).length() for pt in sl] for sl in streamlines]
    flattened = [val for sublist in lengths for val in sublist]
    minL = min(flattened)
    maxL = max(flattened)

    print(f"minL: {minL}, maxL: {maxL}")
    # ---- just in case .. eg if field function returns always Vector(1, 1)
    if minL == maxL:
        print("FAIL - all vectors have same lengths - no color encoding of vector lengths possible")
        return

    # we define colors as numpy arrays for easier arithmetic when building gradient colors (more colors would look nicer, but here it's just a test)
    color1 = np.array([0,70,135]) # dark blue
    color2 = np.array([250, 253, 200]) # lighy yellow
    color3 = np.array([166, 0, 33]) # dark red

    def _getColor(idxSl: int, idxPt: int) -> str:
        """
        internal helper, LERP of 3 colors
        """
        l = (lengths[idxSl][idxPt - 1] + lengths[idxSl][idxPt]) / 2.0
        # lerp
        l01 = (l - minL) / (maxL - minL) # [0..1]

        # simple linear gradient with 3 colors
        if l01 <= 0.5:
            ret = color2 * l01 * 2.0 + color1 * (0.5 - l01) * 2.0
        else:
            ret = color3 * (l01 - 0.5) * 2.0 + color2 * (1.0 - l01) * 2.0

        #print(l01, ret)

        return f"rgb({ret[0]},{ret[1]},{ret[2]})"
        # return "green"


    # ---- build svg
    mySVG = Svg(width=bbox.width, height=bbox.height, viewBox=f"{bbox.topLeft.x} {bbox.topLeft.y} {bbox.width} {bbox.height}")
    shapeBuilder = ShapeBuilder()
    styleBuilder = StyleBuilder()
    #styleBuilder.setStroke('blue')
    styleBuilder.setFilling('none')
    styleBuilder.setStrokeWidth('1px')
    styleBuilder.setStrokeLineCap('round')

    # background
    mySVG.addElement(shapeBuilder.createRect(x=bbox.topLeft.x, y=bbox.topLeft.y, width="100%", height="100%", fill="black", stroke='none'))

    # streamlines
    for idxSl, sl in enumerate(streamlines):
        for idxPt in range(1,len(sl)):
            styleBuilder.setStroke(_getColor(idxSl, idxPt))
            line = shapeBuilder.createLine(str(sl[idxPt-1].x), str(sl[idxPt-1].y), str(sl[idxPt].x), str(sl[idxPt].y))
            line.set_style(styleBuilder.getStyle())
            mySVG.addElement(line)

    # save svg
    # save svg
    print(f"writing {pathDestFile} ...")
    mySVG.save(pathDestFile)



#################### MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN ####################
#################### MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN ####################
#################### MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN ####################
#################### MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN ####################
#################### MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN ####################


# ---- some config constants ..
WIDTH = 400
HEIGHT = 300
BOUNDING_BOX = BoundingBox(-WIDTH/2, -HEIGHT/2, WIDTH, HEIGHT) # a bbox with (0,0) in the center
#BOUNDING_BOX = BoundingBox(0, 0, WIDTH, HEIGHT) # a bbox with (0,0) in the center
INITIAL_SEED_POINT = Vector(10, 10)

MY_TIME_STEP = 1.0
MY_D_SEP = 10
MY_D_TEST = 2





def exampleFlowFieldFunction(coords: Vector) -> Vector:
    """
    some fancy example function
    we pass this function as callback to the streamlines generator
    """
    # return Vector(1,1)
    # return Vector(coords.x, coords.y)
    # return Vector(coords.x / abs(coords.x + 0.000001), coords.y / abs(coords.y + 0.0000001))
    # return Vector(math.sin(coords.x)*0.3, math.sin(coords.y)*0.1 ) # this one jumps between 2 points infinitely .. TODO: use 2nd grid for current streamline
    # return Vector(math.sin(coords.x*0.03),
    #               math.sin(coords.y*0.01) * math.sin(coords.x*0.011212) * 10
    #               )
    return Vector(
        math.sqrt(coords.x*coords.x*0.01 + coords.y*coords.y*0.01)*(math.sin(coords.x*0.01) + math.cos(math.sqrt(coords.x*coords.x*0.01 + coords.y*coords.y*0.01))),
        math.sqrt(coords.x*coords.x*0.01 + coords.y*coords.y*0.01)
    )





# ---- generate the streamlines
theGenerator = StreamlineGenerator(exampleFlowFieldFunction, MY_D_SEP, MY_D_TEST)
theGenerator.setStepSize(MY_TIME_STEP)
streamlines = theGenerator.buildStreamlines(BOUNDING_BOX, INITIAL_SEED_POINT)
print(f"{len(theGenerator._streamlines)} streamlines generated.")

# ---- writes streamlines to .svg files (mono and with color encoded velocity)
toSvgPolylines(BOUNDING_BOX, theGenerator._streamlines, './demo-out/streamlines-mono.svg')
toSvgWithVelocityColors(BOUNDING_BOX, streamlines, exampleFlowFieldFunction, './demo-out/streamlines-color-velocity.svg')
from typing import Union, Callable

from Vector import Vector


def rk4(pos: Vector, stepSize: float, getVelocity: Callable) -> Union[Vector, None]:
    """
    Performs Runge-Kutta 4th order integration.
    returns velocity vector
    """
    k1 = getVelocity(pos)
    if not k1:
        return None

    k2 = getVelocity(pos + k1 * (stepSize * 0.5))
    if not k2:
        return None

    k3 = getVelocity(pos + k2 * (stepSize * 0.5))
    if not k3:
        return None

    k4 = getVelocity(pos + k3 * stepSize)
    if not k4:
        return None

    res = k1 * (stepSize / 6) + k2 * (stepSize / 3) + k3 * (stepSize / 3) + k4 * (stepSize / 6)

    return res

"""Math utility functions"""

from typing import Callable, List, Tuple, Optional

from math import sqrt, log, pow
from scipy import interpolate


def vertical_sigmoid(
    left: float = 0.0,
    right: float = 1.0,
    center: float = 0.0,
    curvature: float = 1.0,
) -> Callable[[float], float]:
    """
    Returns a vertical sigmoid function with asymptotes at `left` and `right`,
    centered at `center`.

    As `curvature` increases, the sigmoid approaches a step function.
    """

    def evaluate(x: float) -> float:
        return center + log((x - left) / (right - x)) / curvature

    return evaluate


def spline_interpolation(
    x: List[float], y: List[float]
) -> Callable[[float], float]:
    """
    Returns a spline interpolation function for the given x and y values.
    """
    tck = interpolate.splrep(x, y, k=2)
    return lambda xx: interpolate.splev(xx, tck).item()


def steep_circular_curve(
    x: List[float], y: List[float]
) -> Callable[[float], float]:
    r"""
    Returns a steep circular curve function for the given x and y values.

    See https://www.desmos.com/calculator/hjactjjo2n

    x < x2: y = a - b \sqrt{ 1 - ((x - d)/c)^2 }

    with the constraints:
    - pass through x1, y1; x2, y2;
    - left side of curve (slope -infty) at x1
    - bottom of curve (slope 0) at x2

    we find that:
    > a = y1
    > b = y1 - y2
    > c = x2 - x1
    > d = x2

    x > x2: y = a + b \sqrt{ 1 - ((x - d)/c)^2 }

    we find that:
    > a = y3
    > b = y2 - y3
    > c = x3 - x2
    > d = x2
    """
    x1, x2, x3 = x
    y1, y2, y3 = y

    def evaluate(x: float) -> float:
        if x < x2:
            return y1 - (y1 - y2) * sqrt(1 - ((x - x2) / (x2 - x1)) ** 2)
        if x > x2:
            return y3 + (y2 - y3) * sqrt(1 - ((x - x2) / (x3 - x2)) ** 2)
        return y2

    return evaluate


def flat_circular_curve(
    x: List[float], y: List[float]
) -> Callable[[float], float]:
    """
    Returns a flat circular curve function for the given x and y values.

    Inverse of steep circular for the two sides.
    """
    x1, x2, x3 = x
    y1, y2, y3 = y

    def evaluate(x: float) -> float:
        if x < x2:
            return y2 + (y1 - y2) * sqrt(1 - ((x - x1) / (x2 - x1)) ** 2)
        if x > x2:
            return y2 - (y2 - y3) * sqrt(1 - ((x - x3) / (x3 - x2)) ** 2)
        return y2

    return evaluate


def concave_curve(
    base: Tuple[float] = (0, 0),
    fixed: Tuple[float] = (1, 1),
    asy: float = 1,
    preval: float = 0,
):
    """
    A concave mapping for `num` which starts at `base`, passes thru `fixed`,
    and asymptotes to `asy`. An input to `num` which is less than `base` will
    return `preval`.

    Based off of a sum of power series, k + k^2 + ... which sums to
    (k / (1-k))(1 - k^x). We modify this to add a scaling factor k for more
    flexibility:

    (k / (1-k))(1 - k^(Cx))

    returns the function itself.
    """
    basex, basey = base
    fixedx, fixedy = fixed
    addx, addy = fixedx - basex, fixedy - basey

    trueasy = asy - basey

    # figure out k
    k = trueasy / (trueasy + 1.0)

    # Note now that (k / (1-k)) = trueasy. Figure out C
    C = log(1 - addy / trueasy) / (addx * log(k))

    def evaluate(x: float) -> float:
        if x < basex:
            return preval
        return basey + trueasy * (1 - pow(k, C * (x - basex)))

    return evaluate


def curve_function(
    curve_type: str = "spline",
    x: List[float] = None,
    y: List[float] = None,
    asy: Optional[float] = None,
    preval: Optional[float] = None,
) -> Callable[[float], float]:
    """
    Returns a mathematical curve function based on the specified type.

    Args:
        curve_type (str): The type of curve to create ("spline",
          "steep_circular", "flat_circular").
        x (List[float]): The x-coordinates for the curve.
        y (List[float]): The y-coordinates for the curve.

    Returns:
        Callable[[float], float]: The corresponding curve function.
    """
    if curve_type == "spline":
        return spline_interpolation(x, y)
    if curve_type == "steep_circular":
        return steep_circular_curve(x, y)
    if curve_type == "flat_circular":
        return flat_circular_curve(x, y)
    if curve_type == "concave":
        return concave_curve(x, y, asy, preval)
    raise ValueError("Unsupported curve type")

import unittest
from unittest.mock import patch
from math import sqrt, log
from src.inferent.utils import (
    vertical_sigmoid,
    spline_interpolation,
    steep_circular_curve,
    flat_circular_curve,
    concave_curve,
    curve_function,
)


class TestMath(unittest.TestCase):

    def test_vertical_sigmoid(self):
        sigmoid = vertical_sigmoid(
            left=0.0, right=1.0, center=0.5, curvature=1.0
        )
        self.assertAlmostEqual(sigmoid(0.5), 0.5)

    @patch("src.inferent.utils.math.interpolate.splrep", autospec=True)
    @patch("src.inferent.utils.math.interpolate.splev", autospec=True)
    def test_spline_interpolation(self, mock_splev, mock_splrep):
        x = [0.0, 0.5, 1.0]
        y = [0.0, 0.5, 1.0]
        mock_splrep.return_value = "tck"
        mock_splev.return_value.item.return_value = 0.5

        spline = spline_interpolation(x, y)
        self.assertAlmostEqual(spline(0.5), 0.5)
        mock_splrep.assert_called_once_with(x, y, k=2)
        mock_splev.assert_called_once_with(0.5, "tck")

    def test_steep_circular_curve(self):
        x = [0.0, 0.5, 1.0]
        y = [1.0, 0.5, 0.0]
        curve = steep_circular_curve(x, y)
        self.assertAlmostEqual(curve(0.5), 0.5)

    def test_flat_circular_curve(self):
        x = [0.0, 0.5, 1.0]
        y = [1.0, 0.5, 0.0]
        curve = flat_circular_curve(x, y)
        self.assertAlmostEqual(curve(0.5), 0.5)

    def test_concave_curve(self):
        concave = concave_curve(base=(0, 0), fixed=(1, 1), asy=1.5, preval=-1)
        self.assertAlmostEqual(concave(0.5), 0.6339745962155612)
        self.assertAlmostEqual(concave(-1), -1)

    @patch("src.inferent.utils.math.spline_interpolation", autospec=True)
    def test_curve_function_spline(self, mock_spline_interpolation):
        x = [0.0, 0.5, 1.0]
        y = [0.0, 0.5, 1.0]
        mock_spline_interpolation.return_value = lambda xx: xx

        curve = curve_function(curve_type="spline", x=x, y=y)
        self.assertAlmostEqual(curve(0.5), 0.5)
        mock_spline_interpolation.assert_called_once_with(x, y)

    @patch("src.inferent.utils.math.steep_circular_curve", autospec=True)
    def test_curve_function_steep_circular(self, mock_steep_circular_curve):
        x = [0.0, 0.5, 1.0]
        y = [1.0, 0.5, 0.0]
        mock_steep_circular_curve.return_value = lambda xx: xx

        curve = curve_function(curve_type="steep_circular", x=x, y=y)
        self.assertAlmostEqual(curve(0.5), 0.5)
        mock_steep_circular_curve.assert_called_once_with(x, y)

    @patch("src.inferent.utils.math.flat_circular_curve", autospec=True)
    def test_curve_function_flat_circular(self, mock_flat_circular_curve):
        x = [0.0, 0.5, 1.0]
        y = [1.0, 0.5, 0.0]
        mock_flat_circular_curve.return_value = lambda xx: xx

        curve = curve_function(curve_type="flat_circular", x=x, y=y)
        self.assertAlmostEqual(curve(0.5), 0.5)
        mock_flat_circular_curve.assert_called_once_with(x, y)

    @patch("src.inferent.utils.math.concave_curve", autospec=True)
    def test_curve_function_concave(self, mock_concave_curve):
        x = [0.0, 0.5, 1.0]
        y = [1.0, 0.5, 0.0]
        mock_concave_curve.return_value = lambda xx: xx

        curve = curve_function(curve_type="concave", x=x, y=y)
        self.assertAlmostEqual(curve(0.5), 0.5)
        mock_concave_curve.assert_called_once_with(x, y, None, None)

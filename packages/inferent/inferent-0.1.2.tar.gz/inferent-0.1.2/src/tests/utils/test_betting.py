import unittest
from unittest.mock import patch, call

import math
import numpy as np

from src.inferent.utils import (
    convert_odds_to_percent,
    convert_odds_from_percent,
    convert_odds,
    exp_wealth_gradient,
    optimal_kelly,
)


class BettingTest(unittest.TestCase):
    def test_convert_odds_to_percent(self):
        self.assertAlmostEqual(convert_odds_to_percent(1.0, "percent"), 1.0)
        self.assertAlmostEqual(convert_odds_to_percent(100, "american"), 0.5)
        self.assertAlmostEqual(convert_odds_to_percent(100, "decimal"), 0.01)

        self.assertAlmostEqual(convert_odds_to_percent(-100, "american"), 0.5)
        self.assertAlmostEqual(convert_odds_to_percent(-300, "american"), 0.75)

        self.assertAlmostEqual(convert_odds_to_percent(0, "percent"), 0)
        self.assertAlmostEqual(convert_odds_to_percent(0, "american"), 1.0)
        self.assertAlmostEqual(convert_odds_to_percent(1, "decimal"), 1.0)

        self.assertAlmostEqual(convert_odds_to_percent(0.5, "percent"), 0.5)
        self.assertAlmostEqual(convert_odds_to_percent(300, "american"), 0.25)
        self.assertAlmostEqual(convert_odds_to_percent(50, "decimal"), 0.02)

    def test_convert_odds_from_percent(self):
        self.assertAlmostEqual(convert_odds_from_percent(1, "percent"), 1)
        self.assertAlmostEqual(
            convert_odds_from_percent(1, "american"), float("-inf")
        )
        self.assertAlmostEqual(convert_odds_from_percent(1, "decimal"), 1)

        self.assertAlmostEqual(convert_odds_from_percent(0, "percent"), 0)
        self.assertAlmostEqual(
            convert_odds_from_percent(0, "american"), float("inf")
        )
        self.assertAlmostEqual(
            convert_odds_from_percent(0, "decimal"), float("inf")
        )

        self.assertAlmostEqual(convert_odds_from_percent(0.5, "percent"), 0.5)
        self.assertAlmostEqual(convert_odds_from_percent(0.5, "american"), 100)
        self.assertAlmostEqual(convert_odds_from_percent(0.5, "decimal"), 2)

        self.assertAlmostEqual(convert_odds_from_percent(0.8, "american"), -400)

    def test_convert_odds(self):
        self.assertAlmostEqual(convert_odds(100, "percent", "american"), 0.5)
        self.assertAlmostEqual(convert_odds(100, "percent", "decimal"), 0.01)
        self.assertAlmostEqual(convert_odds(0.75, "american", "percent"), -300)
        self.assertAlmostEqual(convert_odds(4, "american", "decimal"), 300)
        self.assertAlmostEqual(convert_odds(0.25, "decimal", "percent"), 4)
        self.assertAlmostEqual(convert_odds(200, "decimal", "american"), 3)

    def test_exp_wealth_gradient(self):
        # Test with simple example
        probabilities = [0.5, 0.6]
        ptl = [1.5, 2.15]
        weights = [0.1, 0.2]
        actual_result = exp_wealth_gradient(probabilities, ptl, weights)
        self.assertAlmostEqual(actual_result[0], 0.1411875)
        np.testing.assert_almost_equal(
            actual_result[1], np.array([0.0893215, 0.3969497])
        )

    @patch("src.inferent.utils.betting.exp_wealth_gradient", autospec=True)
    def test_optimal_kelly(self, mock_exp_wealth_gradient):
        # Set up mock data
        probabilities = [0.6, 0.7]
        payoffs = [1.6, 2.1]
        learning_rate = 0.001
        eps = 0.000000001

        # Set up mock return values for exp_wealth_gradient
        mock_exp_wealth_gradient.return_value = 0.1, np.array([0.4, 0.4])

        # Call the function being tested
        result, weights = optimal_kelly(
            probabilities, payoffs, learning_rate, eps
        )

        # Check that the function made the expected call to exp_wealth_gradient
        np.testing.assert_almost_equal(
            mock_exp_wealth_gradient.call_args_list[0][0],
            [[0.6, 0.7], [0.6, 1.1], [0.0, 0.0]],
        )
        np.testing.assert_almost_equal(
            mock_exp_wealth_gradient.call_args_list[1][0],
            [[0.6, 0.7], [0.6, 1.1], [0.0004, 0.0004]],
        )

        # Check that the function returned the expected result
        self.assertAlmostEqual(result, 0.1)
        np.testing.assert_almost_equal(weights, [0.0008, 0.0008])

    @patch("src.inferent.utils.betting.exp_wealth_gradient", autospec=True)
    def test_optimal_kelly_update_adjust(self, mock_exp_wealth_gradient):
        # Set up mock data
        probabilities = [0.6, 0.7]
        payoffs = [1.6, 2.1]
        learning_rate = 2
        eps = 0.000000001

        # Set up mock return values for exp_wealth_gradient
        mock_exp_wealth_gradient.return_value = 0.1, np.array([0.4, 0.4])

        # Call the function being tested
        result, weights = optimal_kelly(
            probabilities, payoffs, learning_rate, eps
        )

        # Check that the function made the expected call to exp_wealth_gradient
        np.testing.assert_almost_equal(
            mock_exp_wealth_gradient.call_args_list[0][0],
            [[0.6, 0.7], [0.6, 1.1], [0.0, 0.0]],
        )
        # Here, we don't adjust to [0.8, 0.8] because it would sum past 1.0.
        np.testing.assert_almost_equal(
            mock_exp_wealth_gradient.call_args_list[1][0],
            [[0.6, 0.7], [0.6, 1.1], [0.25, 0.25]],
        )

        # Check that the function returned the expected result
        self.assertAlmostEqual(result, 0.1)
        np.testing.assert_almost_equal(weights, [0.375, 0.375])


if __name__ == "__main__":
    unittest.main()

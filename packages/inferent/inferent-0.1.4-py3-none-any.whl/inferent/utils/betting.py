"""Betting utilities"""

import itertools
import logging
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)
EPSILON = 1e-8


def convert_odds_to_percent(odds: float, from_type: str = "percent") -> float:
    """
    Convert odds to a percentage probability.

    Args:
        odds (float): The odds value to convert.
        from_type (str): The format of the input odds ("percent", "american",
          "decimal").

    Returns:
        float: The converted percentage probability.

    Raises:
        ValueError: If an invalid from_type is provided.
    """
    if from_type == "percent":
        return odds
    if from_type == "american":
        return (
            100.0 / (odds + 100.0) if odds >= 0 else (-odds) / (-odds + 100.0)
        )
    if from_type == "decimal":
        return 1 / odds
    raise ValueError("Invalid odds type")


def convert_odds_from_percent(
    probability: float, to_type: str = "decimal"
) -> float:
    """
    Convert a percentage probability to specified odds format.

    Args:
        probability (float): The probability value to convert.
        to_type (str): The desired odds format ("percent", "american",
          "decimal").

    Returns:
        float: The converted odds.

    Raises:
        ValueError: If an invalid to_type is provided.
    """
    if to_type == "percent":
        return probability
    if to_type == "american":
        if probability == 0:
            return float("inf")
        if probability == 1:
            return float("-inf")
        if probability <= 0.5:
            return 100.0 / probability - 100.0
        return (-100.0 * probability) / (1.0 - probability)
    if to_type == "decimal":
        return 1.0 / probability if probability != 0.0 else float("inf")
    raise ValueError("Invalid target type")


def convert_odds(
    odds: float, to_type: str = "percent", from_type: str = "american"
) -> float:
    """
    Convert odds from one format to another.

    Args:
        odds (float): The odds value to convert.
        to_type (str): The desired format of the converted odds.
        from_type (str): The format of the input odds.

    Returns:
        float: The converted odds.
    """
    percent = convert_odds_to_percent(odds, from_type)
    return convert_odds_from_percent(percent, to_type)


def exp_wealth_gradient(
    probabilities: npt.NDArray[float],
    profit_to_loss: npt.NDArray[float],
    weights: npt.NDArray[float],
) -> Tuple[float, npt.NDArray[float]]:
    """
    Calculate the expected logarithmic wealth and its gradient.

    Args:
        probabilities: Success probabilities of each event.
        profit_to_loss: Profit-to-loss ratios for each event.
        weights: Investment weights for each event.

    Returns:
        The expected log wealth and its gradient.
    """
    num_events = len(probabilities)
    assert (
        len(profit_to_loss) == num_events
    ), "Profit-to-loss array has size mismatch with probabilities array"
    assert (
        len(weights) == num_events
    ), "weights array has size mismatch with probabilities array"

    # A boolean mask of all possible combinations of events occurring or not
    # occurring. For example, if num_events = 3, this would be
    # [[True True True], [True True False], [True False True], ...]
    combo_mask = np.fromiter(
        itertools.product([True, False], repeat=num_events), (bool, num_events)
    )

    # An array of length len(combo_mask) with the aggregate multiplicative
    # probability for each combination
    combo_prob = np.where(
        combo_mask, probabilities, [1.0 - p for p in probabilities]
    ).prod(axis=1)

    # An array of length len(combo_mask) with the wealth after the event
    # combination, given an initial investment base of 1.0 + epsilon (to avoid
    # log(0) errors)
    combo_wealth = np.where(
        combo_mask, np.multiply(weights, profit_to_loss), np.negative(weights)
    ).sum(axis=1, initial=1 + EPSILON)

    # For a success event, the gradient is the profit_to_loss; for a failed
    # event, the gradient is simply -1.
    combo_gradient = np.where(combo_mask, profit_to_loss, -1)

    # Expectation of log wealth
    exp_log_wealth = (combo_prob * np.log(combo_wealth)).sum()
    # Weighted summed gradient; transpose for numpy broadcasting rules
    gradient = (combo_prob.T * combo_gradient.T / combo_wealth.T).T.sum(axis=0)

    return exp_log_wealth, gradient


def optimal_kelly(
    probabilities: List[float],
    payoffs: List[float],
    learning_rate: float = 0.001,
    eps: float = 1e-10,
) -> Tuple[float, List[float]]:
    """
    Calculate the optimal betting weights using the Kelly Criterion.

    We want to maximize expected log wealth, so we use gradient ascent.

    Args:
        probabilities: Predicted probabilities of winning.
        payoffs: Payoffs for wagering $1.
        learning_rate: Learning rate.
        eps: Epsilon for stopping criterion.

    Returns:
        The maximum expected log wealth and optimal weights.
    """
    profit_to_loss = np.array([payoff - 1.0 for payoff in payoffs])
    weights = np.array([0.0] * len(probabilities))
    probabilities = np.array(probabilities)
    expected_wealth = None
    prev_expected_wealth = None  # For comparison

    def update_weights(weights, gradient, learning_rate) -> List[float]:
        """Update weights based on gradient and learning rate."""
        updated_weights = weights + gradient * learning_rate

        # Weights cannot sum to more than 1, otherwise we have negative logs
        if sum(updated_weights) >= 1.0:
            logger.warning(
                "Weights sum to >= 1. Consider using a lower learning rate."
            )
            # Don't update weights to sum to 1.0 due to dangerous logs
            slack = (1.0 - sum(weights)) / 2.0
            assert slack > 0, "No room for updating."
            adj_rate = slack / sum(gradient)
            updated_weights = weights + gradient * adj_rate

        return np.clip(updated_weights, 0.0, 1.0)

    while (
        prev_expected_wealth is None
        or abs(expected_wealth - prev_expected_wealth) > eps
    ):
        prev_expected_wealth = expected_wealth  # save down copy of prev iter
        expected_wealth, gradient = exp_wealth_gradient(
            probabilities, profit_to_loss, weights
        )
        weights = update_weights(weights, gradient, learning_rate)

    return expected_wealth, weights.tolist()

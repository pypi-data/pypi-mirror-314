"""Module that contains group splitting functions"""

import hashlib
from bisect import bisect
from itertools import accumulate
from math import floor as _floor
from math import isfinite
from random import choices
from typing import TypeVar

T = TypeVar("T")


def deterministic_proba(input_string: str) -> float:
    """Generates a deterministic number in the range [0.0, 1.0) based on
    the input string. When given different strings, it returns floats in [0.0, 1.0)
    following a uniform distribution.

    Args:
        input_string: The string to derive a float from
    Returns:
        float: A number in the range [0.0, 1.0), picked uniformly
        from the space of all possible strings
    """
    digest = hashlib.md5(input_string.encode("ascii")).hexdigest()
    max_int = 0x100000000
    high_bits = int(digest[:8], 16)  # make an int of the highest 8 hex chars
    return (
        high_bits / max_int
    )  # divide by 1 over the fully packed 4 byte hex chars (FFFFFFFF)


def deterministic_choice(
    input_id: str | None,
    population: list[T],
    weights: list[float] | None = None,
    *,
    cum_weights: list[float] | None = None,
) -> T:
    """Functions similarly to random.choices, but uses a deterministic hash function
    instead of a random number generator. The implementation closely follows the
    random.choices implementation.

    As a convenience feature, if no input_id is provided, the function falls back to the
    classic choices call.

    Note: Since this function is deterministic, we can only sensibly choose 1
    item with replacement from the population (all other items would be identical
    to the first). Therefore, the k parameter is fixed at 1, and we return a single item
    rather than a collection like in random.choices.

    Args:
        input_id: If None, returns the classic random.choices result. Otherwise,
            computes a deterministic choice based on the input_id. Items are chosen
            proportionally to their weights and uniformly across all possible input_ids.
        population: List of items to choose from
        weights: Optional weights to assign to each item in the population
        cum_weights: Optional cumulative weights (cannot be used with weights parameter)
    """

    n = len(population)
    if input_id is None:
        return choices(
            population=population, weights=weights, cum_weights=cum_weights, k=1
        )[0]

    if cum_weights is None:
        if weights is None:
            return population[_floor(deterministic_proba(input_id) * n)]

        cum_weights = list(accumulate(weights))
    elif weights is not None:
        raise TypeError("Cannot specify both weights and cumulative weights")

    if len(cum_weights) != n:
        raise ValueError("The number of weights does not match the population")

    total = cum_weights[-1] + 0.0  # convert to float
    if total <= 0.0:
        raise ValueError("Total of weights must be greater than zero")

    if not isfinite(total):
        raise ValueError("Total of weights must be finite")
    hi = n - 1
    return population[bisect(cum_weights, deterministic_proba(input_id) * total, 0, hi)]

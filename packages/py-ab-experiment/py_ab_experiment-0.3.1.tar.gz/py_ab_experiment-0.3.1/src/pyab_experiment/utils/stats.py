"""Binomial CI estimates"""

from math import log, pi


def probit(alpha: float = 0.5) -> float:
    """Compute the probit of a given value.

    The probit function is the inverse of the cumulative distribution function
    (CDF) of the standard normal distribution. It maps a probability (between 0
    and 1) to a corresponding value  on the real number line.

    Args:
        alpha (float): The probability value for which to compute the probit.
            Default is 0.5, which corresponds to the median of the standard
            normal distribution.

    Returns:
        float: The probit value corresponding to the input probability.

    Note:
        See `https://en.wikipedia.org/wiki/Probit for the approximation`_
        of using the logit function.

    Examples:
        >>> probit(0.5)
        0.0
        >>> probit(0.975)
        1.959963984540054
    """

    # our version of mypy doesn't have proper types on pow
    # ignore for now until we upgrade
    # see https://github.com/python/typeshed/issues/7733
    return (pi / 8) ** 0.5 * abs(log(alpha / (1 - alpha)))  # type: ignore


def confidence_interval(
    n: int = 10, p: float = 0.5, confidence: float = 0.95, method: str = "agresti-coull"
) -> tuple[float, float]:
    """Return the mean and the confidence interval of Bernoulli trials.
    See `https://en.wikipedia.org/wiki/Binomial_distribution#Confidence_intervals`_
    """
    alpha = 1 - confidence
    z = probit(alpha / 2)

    est_succ = p * n
    if method.lower() == "agresti-coull":
        n_prime = n + z**2
        p_prime = 1 / n_prime * (est_succ + (1 / 2) * z**2)
        interval = z * (p_prime * (1 - p_prime) / n_prime) ** 0.5
        return (p_prime - interval, p_prime + interval)
    elif method.lower() == "wald":
        interval = z * ((p * (1 - p)) / n) ** 0.5
        return p - interval, p + interval
    else:
        raise NotImplementedError(f"The method '{method}' is not implemented")

"""Classify sentiment probability scores into sentiment classifications."""

NEGATIVE_THRESHOLD = -0.2
POSITIVE_THRESHOLD = 0.2


def classify_sentiment(probability: float) -> str:
    """
    Converts a sentiment probability score into a classification.

    Parameters
    ----------
    probability : float
        The sentiment probability score.

    Returns
    -------
    str
        The sentiment classification.

    Raises
    ------
    ValueError
        If the probability is not a float.
    """
    try:
        probability = float(probability)
    except ValueError:
        raise ValueError("The probability must be a float.")
    if probability < NEGATIVE_THRESHOLD:
        return "Negative"
    elif NEGATIVE_THRESHOLD <= probability <= POSITIVE_THRESHOLD:
        return "Neutral"
    return "Positive"

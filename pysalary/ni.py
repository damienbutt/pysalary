type NiRates = dict[str, dict[str, float]]

ni_rates: NiRates = {
    "rates": {
        "primary": 0.08,
        "upper": 0.02,
    },
    "thresholds": {
        "primary": 1048.00 * 12,
        "uel": 4189.00 * 12,
    },
}


def calculate_ni(salary: float, rates: NiRates = ni_rates) -> float:
    """
    Calculate the National Insurance contributions on a given salary.
    """
    threshold = rates.get("thresholds")
    rate = rates.get("rates")

    if threshold is None:
        raise ValueError("Invalid NI thresholds")

    if rate is None:
        raise ValueError("Invalid NI rates")

    primary_threshold = threshold.get("primary")
    upper_earnings_limit = threshold.get("uel")

    primary_rate = rate.get("primary")
    upper_rate = rate.get("upper")

    # Salary is less than the primary threshold
    if salary <= primary_threshold:
        return 0.00

    # Salary is greater than the primary threshold but less than or equal to the upper earnings limit
    if salary <= upper_earnings_limit:
        return (salary - primary_threshold) * primary_rate

    primary = (upper_earnings_limit - primary_threshold) * primary_rate
    upper = (salary - upper_earnings_limit) * upper_rate

    return primary + upper

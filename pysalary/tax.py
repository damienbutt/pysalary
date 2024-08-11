type TaxRates = dict[str, dict[str, float]]

tax_rates: TaxRates = {
    "rates": {
        "basic": 0.20,
        "higher": 0.40,
        "additional": 0.45,
    },
    "thresholds": {
        "allowance": 12_570.00,
        "allowance_limit": 100_000.00,
        "basic": 37_700.00,
        "higher": 125_140.00,
    },
}


def calculate_tax(salary: float, rates: TaxRates = tax_rates) -> dict[str, float]:
    """
    Calculate the tax on a given salary.
    """
    threshold = rates.get("thresholds")
    rate = rates.get("rates")

    if threshold is None:
        raise ValueError("Invalid tax thresholds")

    if rate is None:
        raise ValueError("Invalid tax rates")

    allowance = threshold.get("allowance")
    allowance_limit = threshold.get("allowance_limit")
    basic_threshold = threshold.get("basic")
    higher_threshold = threshold.get("higher")

    basic_rate = rate.get("basic")
    higher_rate = rate.get("higher")
    additional_rate = rate.get("additional")

    # Salary is less than or equal to the personal allowance
    if salary <= allowance:
        return {
            "total": 0,
            "allowance": allowance,
        }

    # Salary is greater than the personal allowance but less then or equal to the basic rate threshold
    if salary <= basic_threshold:
        return {
            "total": (salary - allowance) * basic_rate,
            "allowance": allowance,
        }

    # Salary is greater than the basic rate threshold but less then or equal to the higher rate threshold,
    # and less than or equal to the allowance limit
    if salary <= allowance_limit:
        basic = (basic_threshold - allowance) * basic_rate
        higher = (salary - basic_threshold) * higher_rate

        return {
            "total": basic + higher,
            "allowance": allowance,
        }

    # Salary is greater than the basic rate threshold but less then or equal to the higher rate threshold,
    # and over the allowance limit
    if salary <= higher_threshold:
        # Allowance is reduced by £1 for every £2 earned over £100,000
        allowance -= (salary - allowance_limit) / 2

        basic = (basic_threshold - allowance) * basic_rate
        higher = (salary - basic_threshold) * higher_rate

        return {
            "total": basic + higher,
            "allowance": allowance,
        }

    # Salary is over the higher rate threshold
    # Allowance is reduced to zero for salaries over £125,140
    allowance = 0.00

    basic = (basic_threshold - allowance) * basic_rate
    higher = (higher_threshold - basic_threshold) * higher_rate
    additional = (salary - higher_threshold) * additional_rate

    return {
        "total": basic + higher + additional,
        "allowance": allowance,
    }

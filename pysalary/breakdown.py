from .tax import calculate_tax
from .ni import calculate_ni


def get_breakdown(salary: float, currency: str = "£") -> dict[str, float]:
    """
    Calculate the tax and NI contributions on a given salary.
    """
    try:
        total_ni = calculate_ni(salary)
    except ValueError as e:
        raise ValueError(e)

    try:
        tax_result = calculate_tax(salary)
    except ValueError as e:
        raise ValueError(e)

    total_tax = tax_result.get("total")
    allowance = tax_result.get("allowance")

    taxable_income = salary - allowance
    total_deductions = total_tax + total_ni
    yearly_net_income = salary - total_deductions
    monthly_net_income = yearly_net_income / 12
    weekly_net_income = (yearly_net_income / 365.25) * 7
    daily_net_income = yearly_net_income / 365.25
    hourly_net_income = (yearly_net_income / 365.25) / 8

    return {
        "Personal Allowance": allowance,
        "Total NI Payable": total_ni,
        "Taxable Income": taxable_income,
        "Total Tax Payable": total_tax,
        "Total Deductions": total_deductions,
        "Yearly Net Income": yearly_net_income,
        "Monthly Net Income": monthly_net_income,
        "Weekly Net Income": weekly_net_income,
        "Daily Net Income": daily_net_income,
        "Hourly Net Income": hourly_net_income,
    }

#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table
from rich import print
from typing import Dict

tax_rates: Dict[str, Dict[str, float]] = {
    "rates": {
        "basic": 0.20,
        "higher": 0.40,
        "additional": 0.45,
    },
    "thresholds": {
        "allowance": 12_570,
        "allowance_limit": 100_000,
        "basic": 37_700,
        "higher": 125_140,
    },
}


ni_rates: Dict[str, Dict[str, float]] = {
    "rates": {
        "primary": 0.08,
        "upper": 0.02,
    },
    "thresholds": {
        "lel": 123 * 52,
        "primary": 242 * 52,
        "uel": 967 * 52,
    },
}


def calculate_tax(
    salary: float, rates: Dict[str, Dict[str, float]] = tax_rates
) -> Dict[str, float]:
    """
    Calculate the tax on a given salary.
    """
    threshold: Dict[str, float] = rates.get("thresholds")
    rate: Dict[str, float] = rates.get("rates")

    if threshold is None:
        raise ValueError("Invalid tax thresholds")

    if rate is None:
        raise ValueError("Invalid tax rates")

    allowance: float = threshold.get("allowance")

    if salary <= allowance:
        return {
            "total": 0,
            "allowance": allowance,
        }

    if salary <= threshold.get("basic"):
        return {
            "total": (salary - allowance) * rate.get("basic"),
            "allowance": allowance,
        }

    if salary <= threshold.get("allowance_limit"):
        basic: float = (threshold.get("basic") - allowance) * rate.get("basic")
        higher: float = (salary - threshold.get("basic")) * rate.get("higher")

        return {
            "total": basic + higher,
            "allowance": allowance,
        }

    if salary <= threshold.get("higher"):
        # Allowance is reduced by £1 for every £2 earned over £100,000
        allowance -= (salary - threshold.get("allowance_limit")) / 2

        basic: float = (threshold.get("basic") - allowance) * rate.get("basic")
        higher: float = (salary - threshold.get("basic")) * rate.get("higher")

        return {
            "total": basic + higher,
            "allowance": allowance,
        }

    # Allowance is reduced to zero for salaries over £125,140
    allowance = 0

    basic: float = (threshold.get("basic") - allowance) * rate.get("basic")
    higher: float = (threshold.get("higher") - threshold.get("basic")) * rate.get(
        "higher"
    )
    additional: float = (salary - threshold.get("higher")) * rate.get("additional")

    return {
        "total": basic + higher + additional,
        "allowance": allowance,
    }


def calculate_ni(salary: float, rates: Dict[str, Dict[str, float]] = ni_rates) -> float:
    """
    Calculate the National Insurance contributions on a given salary.
    """
    threshold: Dict[str, float] = rates.get("thresholds")
    rate: Dict[str, float] = rates.get("rates")

    if threshold is None:
        raise ValueError("Invalid NI thresholds")

    if rate is None:
        raise ValueError("Invalid NI rates")

    if salary <= threshold.get("primary"):
        return 0

    if salary <= threshold.get("uel"):
        return (salary - threshold.get("primary")) * rate.get("primary")

    primary: float = (threshold.get("uel") - threshold.get("primary")) * rate.get(
        "primary"
    )
    upper: float = (salary - threshold.get("uel")) * rate.get("upper")

    return primary + upper


def get_breakdown(salary: float, currency: str = "£") -> Dict[str, float]:
    """
    Calculate the tax and NI contributions on a given salary.
    """
    try:
        tax: float = calculate_tax(salary)
    except ValueError as e:
        raise ValueError(e)

    try:
        total_ni: float = calculate_ni(salary)
    except ValueError as e:
        raise ValueError(e)

    total_tax: float = tax.get("total")
    allowance: float = tax.get("allowance")
    taxable_income: float = salary - allowance

    total_deductions: float = total_tax + total_ni
    yearly_net_income: float = salary - total_deductions
    monthly_net_income: float = yearly_net_income / 12
    weekly_net_income: float = yearly_net_income / 52
    daily_net_income: float = yearly_net_income / (52 * 5)

    return {
        "Personal Allowance": allowance,
        "Taxable Income": taxable_income,
        "Total Tax Payable": total_tax,
        "Total NI Payable": total_ni,
        "Total Deductions": total_deductions,
        "Yearly Net Income": yearly_net_income,
        "Monthly Net Income": monthly_net_income,
        "Weekly Net Income": weekly_net_income,
        "Daily Net Income": daily_net_income,
    }


if __name__ == "__main__":
    try:
        salary: float = float(input("Enter your yearly salary: "))
    except ValueError:
        print("Please enter a valid number. Eg. 25000")
        exit(1)
    except KeyboardInterrupt:
        exit(0)

    try:
        breakdown: Dict[str, float] = get_breakdown(salary)
    except ValueError as e:
        print(f"[bold red]Error: {e}[/bold red]")
        exit(1)

    console = Console()
    table = Table(title="Salary Breakdown")

    table.add_column("Salary", justify="right", style="cyan")
    table.add_column(f"£{salary:,.2f}", justify="right", style="magenta")

    for key, value in breakdown.items():
        table.add_row(key, f"£{value:,.2f}")

    console.print()
    console.print(table)

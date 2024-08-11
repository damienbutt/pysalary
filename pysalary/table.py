from rich.table import Table


def get_table(salary: float, breakdown: dict[str, float]) -> Table:
    table = Table(title="Salary Breakdown")

    table.add_column("Salary", justify="right", style="cyan")
    table.add_column(f"£{salary:,.2f}", justify="right", style="magenta")

    for key, value in breakdown.items():
        table.add_row(key, f"£{value:,.2f}")

    return table

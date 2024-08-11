#!/usr/bin/env python3

from rich.console import Console
from rich import print
from .breakdown import get_breakdown
from .table import get_table
import click


@click.command(
    "pysalary",
    help="Breakdown your salary and view you tax deductions and take home pay in a tabular format",
)
@click.option(
    "--salary",
    "-s",
    type=float,
    help="Your yearly salary",
    prompt="Enter your yearly salary",
)
@click.version_option(message="%(version)s")
def main(salary: float) -> None:
    try:
        breakdown = get_breakdown(salary)
    except ValueError as e:
        print(f"[bold red]Error: {e}[/bold red]")
        exit(1)

    console = Console()
    console.print()
    console.print(get_table(salary, breakdown))


if __name__ == "__main__":
    main()

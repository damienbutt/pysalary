#!/usr/bin/env python3

from rich.console import Console
from rich import print
from .breakdown import get_breakdown
from .table import get_table
import click


@click.command("pysalary")
@click.option(
    "--salary",
    "-s",
    type=float,
    prompt="Enter your yearly salary",
    help="Your yearly salary",
)
def main() -> None:
    while True:
        try:
            salary = float(input("Enter your yearly salary: "))
            break
        except ValueError:
            print("Please enter a valid number. Eg. 25000")
        except KeyboardInterrupt:
            exit(0)

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

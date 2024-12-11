import os
from datetime import datetime

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from .create_random_dog import create_random_dog
from .fetch_and_listify_csv_dog_data import fetch_and_listify_csv_dog_data
from .find_dog_by import find_dog_by
from .get_dog_statistics import get_dog_statistics


load_dotenv()
console: Console = Console()

DOG_DATA_URL: str = os.getenv(
    "DOG_DATA_URL",
    "https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen_od1002/download/KUL100OD1002.csv",
)
CURRENT_YEAR: str = str(datetime.now().year)

try:
    dog_data: list[dict[str, str]] = fetch_and_listify_csv_dog_data(DOG_DATA_URL)
except RuntimeError as error:
    console.print(
        Panel(
            f"❌ [bold red]Error loading dog data:[/bold red] {error}",
            title="Data Error",
            style="bold red",
        )
    )
    dog_data = []


@click.group(help="A CLI tool to search Zurich's dog registry.")
@click.option(
    "-y",
    "--year",
    type=str,
    default=CURRENT_YEAR,
    help="Filter by year of birth or pass in 'all' to see all years (optional).",
)
@click.pass_context
def wuff(context: click.Context, year: str):
    context.ensure_object(dict)
    if year.lower() == "all":
        filtered_data = dog_data
    else:
        filtered_data = [dog for dog in dog_data if dog.get("GebDatHundJahr") == year]
    context.obj["dog_data"] = filtered_data
    context.obj["year"] = year


@wuff.command(
    help=(
        "Find dogs by name in the database. For example: wuff.py find Lisa.\n"
        "You can also specify a year using the --year option in the format YYYY, "
        "e.g., 1998, or pass 'all' to include all years."
    )
)
@click.argument("name", type=str)
@click.pass_context
def find(context: click.Context, name: str) -> None:
    find_dog_by(name, context.obj["dog_data"], context.obj["year"])


@wuff.command(help="Show statistics about the dog database.")
@click.pass_context
def stats(context: click.Context) -> None:
    get_dog_statistics(context.obj["dog_data"])


@wuff.command(help="Create a random dog profile with a media file.")
@click.option(
    "-o",
    "--output-dir",
    default=".",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    help="Specify the output directory for the downloaded media file. Defaults to the current directory.",
)
@click.pass_context
def create(context: click.Context, output_dir: str) -> None:
    create_random_dog(context.obj["dog_data"], output_dir)


if __name__ == "__main__":
    try:
        wuff()
    except Exception as error:
        console.print(
            Panel(
                f"❌ [bold red]An unexpected error occurred in the application:[/bold red] {error}",
                title="Application Error",
                style="bold red",
            )
        )

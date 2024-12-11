import click
from rich.console import Console
from rich.panel import Panel

from .display_dog_data_as_table import display_dog_data_as_table
from .find_helper_functions import filter_dog_data
from .custom_types import FinalRowConfig


def find_dog_by(name: str, dog_data: list[dict[str, str]], year: str) -> None:
    console: Console = Console()

    if not name.strip():
        console.print(
            Panel(
                "❌ [bold red]The dog name cannot be an empty string.[/bold red]",
                style="bold red",
            )
        )
        return

    try:
        match_type: str = click.prompt(
            f"Do you want to search strictly for dogs named {name}? "
            "Strict search will match exact names, while substring search will include all names containing the name.",
            type=str,
            default="no",
            show_choices=True,
        )

        filtered_dog_data, title, final_row_message = filter_dog_data(
            name, dog_data, year, match_type
        )

        if not filtered_dog_data:
            console.print(
                Panel(
                    f"❌ [bold red]No dogs found matching '{name}' for the year {year}.[/bold red]",
                    style="bold red",
                )
            )
            return

        amount_of_same_named_dogs: int = len(filtered_dog_data)

        final_row_config: FinalRowConfig = {
            "add_final_row": True,
            "final_row_text": final_row_message,
            "name": name,
            "dog_count": str(amount_of_same_named_dogs),
        }

        display_dog_data_as_table(
            filtered_dog_data, title=title, final_row_config=final_row_config
        )
    except RuntimeError as error:
        console.print(
            Panel(
                f"❌ [bold red]An unexpected error occurred:[/bold red] {error}",
                style="bold red",
            )
        )

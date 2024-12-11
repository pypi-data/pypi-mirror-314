from typing import Optional

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .custom_types import FinalRowConfig
from .display_helper_functions import (
    populate_find_table,
    populate_create_table,
    populate_stats_table,
    print_table_with_padding,
)


def display_dog_data_as_table(
    data: list[dict[str, str]],
    title: str = "Dog Table",
    mode: str = "find",
    no_data_message: str = "❌ No data found",
    final_row_config: Optional[FinalRowConfig] = None,
) -> None:
    console: Console = Console()

    if not data:
        console.print(
            Panel(no_data_message, title="🚫 No Data", style="bold red", expand=False)
        )
        return
    try:
        table: Table = Table(
            title=title,
            box=box.ROUNDED,
            border_style="bright_blue",
            title_style="bold yellow",
        )

        if not data:
            console.print(
                Panel(
                    no_data_message, title="🚫 No Data", style="bold red", expand=False
                )
            )
            return

        if mode == "find":
            populate_find_table(table, data)

        elif mode == "stats":
            populate_stats_table(table, data)

        elif mode == "create":
            populate_create_table(table, data)

        else:
            raise ValueError(f"Unsupported mode: {mode}")

        if final_row_config and final_row_config.get("add_final_row", False):
            final_row_text: str = final_row_config.get("final_row_text", "")
            table.add_row(
                final_row_text.format(
                    name=final_row_config.get("name", ""),
                    count=final_row_config.get("dog_count", "0"),
                ),
                style="bold white on black",
            )

        print_table_with_padding(console, table)

    except Exception as error:
        console.print(
            Panel(
                f"❌ [bold red]An unexpected error occurred while displaying the table:[/bold red] {error}",
                style="bold red",
            )
        )

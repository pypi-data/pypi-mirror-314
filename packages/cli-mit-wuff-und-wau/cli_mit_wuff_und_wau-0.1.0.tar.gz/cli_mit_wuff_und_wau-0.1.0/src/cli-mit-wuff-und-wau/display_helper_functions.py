from rich.console import Console
from rich.table import Table


def populate_find_table(table: Table, data: list[dict[str, str]]) -> None:
    table.add_column("🐕 Name", header_style="bold cyan", style="cyan")
    table.add_column("📅 Year", header_style="bold green", style="green")
    table.add_column(
        "👶 Assigned at Birth", header_style="bold magenta", style="magenta"
    )

    for row in data:
        name = row.get("HundenameText", "Unknown")
        year = row.get("GebDatHundJahr", "Unknown")
        sex = row.get("SexHundCd", "Unknown")

        if sex == "1":
            assigned_at_birth = "[bold blue]Assigned Male at Birth[/bold blue]"
            row_style = "on blue"
        elif sex == "2":
            assigned_at_birth = "[bold magenta]Assigned Female at Birth[/bold magenta]"
            row_style = "on magenta"
        else:
            assigned_at_birth = "[bold red]Unknown[/bold red]"
            row_style = "on grey15"

        table.add_row(name, year, assigned_at_birth, style=row_style)


def get_stats_row_style(statistic: str) -> str:
    """Get style for statistics rows."""
    if statistic == "Total Dogs":
        return "on cyan"
    elif statistic == "Top 1 Most Common Name":
        return "on green"
    elif statistic == "Shortest Name":
        return "on magenta"
    elif statistic == "Longest Name":
        return "on yellow"
    elif statistic.startswith("Top 1 Male"):
        return "on blue"
    elif statistic.startswith("Top 1 Female"):
        return "on magenta"
    else:
        return "on black"


def populate_stats_table(table: Table, data: list[dict[str, str]]) -> None:
    table.add_column("📊 Statistic", header_style="bold blue", style="blue")
    table.add_column("🔢 Value", header_style="bold green", style="green")

    for row in data:
        statistic = row.get("Statistic", "Unknown")
        value = row.get("Value", "Unknown")
        style = get_stats_row_style(statistic)
        table.add_row(statistic, value, style=style)


def populate_create_table(table: Table, data: list[dict[str, str]]) -> None:
    table.add_column(
        "📝 Attribute", header_style="bold yellow", style="yellow", justify="left"
    )
    table.add_column(
        "📥 Value", header_style="bold green", style="green", justify="center"
    )

    for row in data:
        attribute = row.get("Attribute", "Unknown")
        val = row.get("Value", "Unknown")
        table.add_row(attribute, val, style="on black")


def print_table_with_padding(console: Console, table: Table) -> None:
    console.print("\n" * 3)
    console.print(table, justify="center")
    console.print("\n" * 3)

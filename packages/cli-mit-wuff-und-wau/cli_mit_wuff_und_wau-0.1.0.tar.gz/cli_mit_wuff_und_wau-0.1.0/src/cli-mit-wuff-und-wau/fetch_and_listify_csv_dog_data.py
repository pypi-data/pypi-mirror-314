import csv
import requests
from rich.console import Console
from rich.panel import Panel


def fetch_and_listify_csv_dog_data(url: str) -> list[dict[str, str]]:
    console: Console = Console()
    try:
        adjusted_data_two_dogs_in_row: list[dict[str, str]] = []

        res: requests.Response = requests.get(url)
        res.encoding = "utf-8-sig"

        csv_file: list[str] = res.text.splitlines()
        data: csv.DictReader[str] = csv.DictReader(csv_file)

        dog_data_list: list[dict[str, str]] = [row for row in data]

        for row in dog_data_list:
            filtered_row: dict[str, str] = {
                "Stichtag": row.get("Stichtag", ""),
                "HundenameText": row.get("HundenameText", ""),
                "GebDatHundJahr": row.get("GebDatHundJahr", ""),
                "SexHundCd": row.get("SexHundCd", ""),
            }

            count: int = int(row.get("AnzHunde", 1))
            for _ in range(count):
                adjusted_data_two_dogs_in_row.append(filtered_row)

        return adjusted_data_two_dogs_in_row

    except requests.exceptions.RequestException as error:
        console.print(
            Panel(
                f"❌ [bold red]Error fetching data from URL:[/bold red] {error}",
                title="Fetch Error",
                style="bold red",
            )
        )
        return []

    except csv.Error as error:
        console.print(
            Panel(
                f"❌ [bold red]Error parsing the CSV file:[/bold red] {error}",
                title="CSV Parse Error",
                style="bold red",
            )
        )
        return []

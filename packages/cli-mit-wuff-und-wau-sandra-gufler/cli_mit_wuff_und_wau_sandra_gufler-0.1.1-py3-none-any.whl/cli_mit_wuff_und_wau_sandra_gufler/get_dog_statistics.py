from rich.console import Console
from rich.panel import Panel

from .display_dog_data_as_table import display_dog_data_as_table
from .statistics_helper_functions import get_statistics_for_table


def get_dog_statistics(raw_dog_data: list[dict[str, str]]) -> None:
    console: Console = Console()

    if not raw_dog_data:
        console.print(
            Panel(
                "❌ [bold red]No dog data available for statistics.[/bold red]",
                title="No Data",
                style="bold red",
            )
        )
        return
    try:
        adjusted_data: list[dict[str, str]] = []
        title: str = "Dog Statistics"

        for row in raw_dog_data:
            count = int(row.get("AnzHunde", 1))
            for _ in range(count):
                new_row: dict[str, str] = row.copy()
                new_row["AnzHunde"] = "1"
                adjusted_data.append(new_row)

        statistics_data = get_statistics_for_table(adjusted_data)

        display_dog_data_as_table(statistics_data, title=title, mode="stats")

    except Exception as error:
        console.print(
            Panel(
                f"❌ [bold red]An unexpected error occurred:[/bold red] {error}",
                title="Error",
                style="bold red",
            )
        )

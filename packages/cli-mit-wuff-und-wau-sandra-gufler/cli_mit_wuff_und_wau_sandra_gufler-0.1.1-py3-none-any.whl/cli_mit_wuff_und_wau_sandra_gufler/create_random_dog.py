import os
import subprocess

from rich.panel import Panel
from rich.console import Console

from .display_dog_data_as_table import display_dog_data_as_table
from .create_helper_functions import (
    get_random_dog_from_csv,
    sanitize_dog_name,
    fetch_random_dog_image_url,
    download_and_resize_dog_image,
)


def create_random_dog(dog_data: list[dict[str, str]], output_dir: str = ".") -> None:
    console: Console = Console()
    if not dog_data:
        console.print(
            Panel("❌ [bold red]No dog data provided.[/bold red]", style="bold red")
        )
        return

    try:
        random_dog: dict[str, str] = get_random_dog_from_csv(dog_data)
        random_dog_name: str = random_dog["HundenameText"]
        birth_year: str = random_dog.get("GebDatHundJahr", "Unknown")
        assigned_sex: str = (
            "Assigned Male at Birth"
            if random_dog["SexHundCd"] == "1"
            else "Assigned Female at Birth"
        )

        sanitized_name: str = sanitize_dog_name(random_dog_name)
        file_dog_name_with_birth_year: str = f"{sanitized_name}_{birth_year}"

        random_dog_image_url: str = fetch_random_dog_image_url()

        file_extension: str = random_dog_image_url.split(".")[-1]
        file_name: str = f"{file_dog_name_with_birth_year}.{file_extension}"
        output_path: str = os.path.join(output_dir, file_name)

        download_and_resize_dog_image(random_dog_image_url, output_path)

        dog_data_to_display: list[dict[str, str]] = [
            {"Attribute": "Name", "Value": random_dog_name},
            {"Attribute": "Assigned Sex", "Value": assigned_sex},
            {"Attribute": "Year of Birth", "Value": birth_year},
            {"Attribute": "Image Saved At", "Value": output_path},
        ]

        display_dog_data_as_table(
            data=dog_data_to_display,
            title=f"Here is your new dog: {random_dog_name} - Born in {birth_year}",
            mode="create",
        )

        subprocess.run(["open", output_path])

    except Exception as error:
        console.print(
            Panel(
                f"❌ [bold red]An unexpected error occurred:[/bold red] {error}",
                style="bold red",
            )
        )

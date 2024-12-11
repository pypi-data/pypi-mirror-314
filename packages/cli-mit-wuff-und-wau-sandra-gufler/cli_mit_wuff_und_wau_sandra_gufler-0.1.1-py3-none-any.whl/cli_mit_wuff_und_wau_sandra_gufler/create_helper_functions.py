import os
import shutil

import random
import string

import requests
from dotenv import load_dotenv

from PIL import Image
from rich.console import Console
from rich.panel import Panel

load_dotenv()

RANDOM_DOG_API_random_dog_image_url: str = os.getenv(
    "RANDOM_DOG_API_random_dog_image_url", "https://random.dog/woof.json"
)

console: Console = Console()


def get_random_dog_from_csv(dog_data: list[dict[str, str]]) -> dict[str, str]:
    random_sex: str = random.choice(["1", "2"])
    filtered_dogs: list[dict[str, str]] = [
        dog for dog in dog_data if dog["SexHundCd"] == random_sex
    ]

    return random.choice(filtered_dogs)


def sanitize_dog_name(dog_name: str) -> str:
    allowed_characters: str = f"-_.() {string.ascii_letters}{string.digits}"
    sanitized_name: str = "".join(
        char if char in allowed_characters else "_" for char in dog_name
    )

    return sanitized_name.replace(" ", "_")


def fetch_random_dog_image_url() -> str:
    try:
        response: requests.Response = requests.get(RANDOM_DOG_API_random_dog_image_url)
        response.raise_for_status()

        res: dict[str, str] = response.json()
        random_dog_image_url: str = res.get("url", "")

        if random_dog_image_url.endswith(".jpg"):
            return random_dog_image_url
        else:
            return fetch_random_dog_image_url()

    except requests.RequestException as error:
        console.print(
            Panel(
                f"❌ [bold red]Error fetching media URL:[/bold red] {error}",
                style="bold red",
            )
        )
        raise


def download_and_resize_dog_image(
    dog_image_url: str, output_path: str, resize_width: int = 300
) -> None:
    try:
        response: requests.Response = requests.get(
            dog_image_url, stream=True, timeout=2
        )
        response.raise_for_status()

        with open(output_path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)

        with Image.open(output_path) as image:
            aspect_ratio: float = image.height / image.width
            resize_height: int = int(resize_width * aspect_ratio)
            resized_image: Image.Image = image.resize((resize_width, resize_height))
            resized_image.save(output_path)

    except requests.RequestException as error:
        console.print(
            Panel(
                f"❌ [bold red]Failed to download image from {dog_image_url}:[/bold red] {error}",
                style="bold red",
            )
        )
        raise
    except IOError as error:
        console.print(
            Panel(
                f"❌ [bold red]Error saving or processing the image at {output_path}:[/bold red] {error}",
                style="bold red",
            )
        )
        raise

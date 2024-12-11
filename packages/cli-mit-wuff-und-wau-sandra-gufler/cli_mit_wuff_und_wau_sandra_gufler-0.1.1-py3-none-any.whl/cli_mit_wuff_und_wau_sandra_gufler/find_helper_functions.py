def filter_dog_data(
    name: str, dog_data: list[dict[str, str]], year: str, match_type: str
) -> tuple[list[dict[str, str]], str, str]:
    if match_type.lower() == "yes":
        filtered_dog_data = [
            entry
            for entry in dog_data
            if "HundenameText" in entry
            and name.lower() == entry["HundenameText"].lower()
        ]
        title = f"Strict Match: Search Results for {name} - year {year}"
        final_row_message = f"Total of dogs that are named {name}: {{count}}"
    else:
        filtered_dog_data = [
            entry
            for entry in dog_data
            if "HundenameText" in entry
            and name.lower() in entry["HundenameText"].lower()
        ]
        title = f"Substring Match: Search Results that contain the string {name} - year {year}"
        final_row_message = f"Total of dogs that contain {name}: {{count}}"

    return filtered_dog_data, title, final_row_message

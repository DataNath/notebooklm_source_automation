from pathlib import Path as p
import sys, os

def create_source_list(source_type) -> list:

    root_directory = p(__file__).parents[1]

    file_name = root_directory / "sources" / f"{source_type}_links.csv"

    if not file_name.exists():
        raise ValueError(
            f"{source_type}_links.csv doesn't exist or is in the wrong location."
        )

    urls = []

    with open(str(file_name), mode="r", encoding="utf-8", newline="") as contents:
        next(contents)

        blank_lines = 0
        for i in contents:

            link = i.strip()
            if link:
                urls.append(link)
            else:
                blank_lines += 1

        if len(urls) == 0:
            raise ValueError(f"Error: {source_type}_links.csv does not contain any records.")

        if blank_lines > 0:
            print(f"\nNote: {blank_lines} empty records from your {source_type}_csv file skipped.")

    return urls

if __name__ == "__main__":
    create_source_list("website")

import sys, os

def create_source_list(source_type) -> list:

    file_name = f"./sources/{source_type}_links.csv"

    if not os.path.exists(file_name):
        raise ValueError(
            f"{source_type}_links.csv doesn't exist or is in the wrong location."
        )

    urls = []

    with open(file_name, mode="r", encoding="utf-8") as contents:
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

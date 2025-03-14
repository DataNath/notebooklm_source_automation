import sys

def file_handler(source_type):

    urls = []

    with open(f"./sources/{source_type}_links.csv", mode="r", encoding="utf-8") as contents:
        next(contents)

        blank_lines = 0
        for i in contents:

            link = i.strip()
            if link:
                urls.append(link)
            else:
                blank_lines += 1
        
        if len(urls) == 0:
            print(f"Error: {source_type}_links.csv does not contain any records.")

        if blank_lines > 0:
            print(f"\nNote: {blank_lines} empty records from your {source_type}_csv file skipped.")

    return urls

file_handler("youtube")
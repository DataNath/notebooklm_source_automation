from playwright.sync_api import sync_playwright, expect
import re

# Create a list of urls, taken from links.csv

def add_link_sources(source_type: str, page) -> None:

    urls = []

    with open(f"sources/{source_type}_links.csv", mode="r", encoding="utf-8") as contents:
        next(contents)

        blank_lines = 0
        for i in contents:
            link = i.strip()
            if link:
                urls.append(link)
            else:
                blank_lines += 1

        if blank_lines > 0:
            print(f"\nNote: {blank_lines} empty records from your {source_type}_csv file skipped.")

    url_count = len(urls)
    is_first = 0
    is_last = url_count - 1

    print(f"\nAttempting to add {url_count} sources from provided {source_type}_links.csv file...\n")

    page.goto("https://notebooklm.google.com/")

    for i, u in enumerate(urls):

        if i == is_first:

            new_notebook_button = page.get_by_role("button", name="Create new notebook")
            new_notebook_button.wait_for(state="attached")
            new_notebook_button.click()

        link_button = page.locator(
            "span.mdc-evolution-chip__text-label", has_text=re.compile(f"{source_type}",re.I)
        )
        link_button.wait_for(state="attached")
        link_button.click()

        link_url_input = page.locator("[formcontrolname='newUrl']")
        link_url_input.wait_for(state="attached")
        link_url_input.fill(u)
        page.keyboard.press("Enter")

        source_container = page.locator("div.single-source-container").last
        source_container.wait_for(state="attached")

        loading_spinner = source_container.locator(".mat-mdc-progress-spinner")
        loading_spinner.wait_for(state="detached")

        checkbox = source_container.locator(
            "input.mdc-checkbox__native-control.mdc-checkbox--selected"
        )
        checkbox.wait_for(state="attached")
        expect(checkbox).not_to_have_attribute("ariaLabel", u)

        page.wait_for_timeout(1200)

        if i < is_last:

            add_source_button = page.get_by_role("button", name="Add source")
            add_source_button.wait_for(state="attached")
            add_source_button.click()

        print(f"Source {i+1}/{url_count} ({u}) added.")

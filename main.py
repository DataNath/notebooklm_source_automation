from playwright.sync_api import sync_playwright, expect
import time

start = time.time()

notebook_name = input("Set a name for your new notebook: ")

# Create a list of urls, taken from links.csv

urls = []

with open("links.csv", mode="r", encoding="utf-8") as contents:
    next(contents)

    for i in contents:
        link = i.strip()
        urls.append(link)

url_count = len(urls)
is_first = 0
is_last = url_count - 1

print(f"\nAttempting to add {url_count} sources from provided links.csv file...\n")

# Initialise browser session

with sync_playwright() as sp:
    browser = sp.chromium.launch(headless=False, channel="chrome")
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()

    page.goto("https://notebooklm.google.com/")

    for i, u in enumerate(urls):

        if i == is_first:

            new_notebook_button = page.get_by_role("button", name="Create new notebook")
            new_notebook_button.wait_for(state="visible")
            new_notebook_button.click()

        website_button = page.locator("span.mdc-evolution-chip__text-label", has_text="Website")
        website_button.wait_for(state="visible")
        website_button.click()

        website_url_input = page.locator("[formcontrolname='newUrl']")
        website_url_input.wait_for(state="visible")
        website_url_input.fill(u)
        page.keyboard.press("Enter")

        checkbox_container = page.locator(
            "div.single-source-container"
        ).last
        checkbox_container.wait_for(state="visible")

        loading_spinner = checkbox_container.locator(".mat-mdc-progress-spinner")

        loading_spinner.wait_for(state="detached")

        checkbox = checkbox_container.locator(
            "input.mdc-checkbox__native-control.mdc-checkbox--selected"
        )
        checkbox.wait_for(state="visible")
        expect(checkbox).not_to_have_attribute("ariaLabel", u)

        page.wait_for_timeout(1000)

        if i < is_last:

            add_source_button = page.get_by_label("Add source")
            add_source_button.wait_for(state="visible")
            add_source_button.click()

        print(f"Source {i+1}/{url_count} ({u}) added.")

    print("\nFinished adding sources.\n")

    title_box = page.locator(".title-input")
    title_box.click()
    page.keyboard.press("Control+A")
    title_box.fill(notebook_name)

    print("Title updated!\n")


    browser.close()

end = time.time()

elapsed = round(end - start)
print(f"Time elapsed: {elapsed} seconds.")

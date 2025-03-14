from playwright.sync_api import sync_playwright, expect
import time

start = time.time()

notebook_name = input("Set a name for your new notebook: ")

# Create a list of urls, taken from links.csv

urls = []

with open("sources/links.csv", mode="r", encoding="utf-8") as contents:
    next(contents)

    for i in contents:
        link = i.strip()
        urls.append(link)

url_count = len(urls)
is_first = 0
is_last = url_count - 1

print(f"Attempting to add {url_count} sources from provided links.csv file...\n")

# Initialise browser session

with sync_playwright() as sp:
    browser = sp.chromium.launch(headless=True, channel="chrome")
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()

    page.goto("https://notebooklm.google.com/")

    for i, u in enumerate(urls):

        if i == is_first:

            new_notebook_button = page.get_by_role("button", name="Create new notebook")
            new_notebook_button.wait_for(state="attached")
            new_notebook_button.click()

        website_button = page.locator("span.mdc-evolution-chip__text-label", has_text="Website")
        website_button.wait_for(state="attached")
        website_button.click()

        website_url_input = page.locator("[formcontrolname='newUrl']")
        website_url_input.wait_for(state="attached")
        website_url_input.fill(u)
        page.keyboard.press("Enter")

        checkbox_container = page.locator(
            "div.single-source-container"
        ).last
        checkbox_container.wait_for(state="attached")

        loading_spinner = checkbox_container.locator(".mat-mdc-progress-spinner")

        loading_spinner.wait_for(state="detached")

        checkbox = checkbox_container.locator(
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

    print("\nFinished adding sources.\n")

    title_box = page.locator(".title-input")
    title_box.click()
    page.keyboard.press("Control+A")
    title_box.fill(notebook_name)
    title_box.press("Enter")

    page.wait_for_timeout(1000)

    print("Title updated!\n")

    browser.close()

end = time.time()

elapsed = round(end - start)

if elapsed > 59:
    minutes = elapsed // 60
    seconds = elapsed % 60

    print(f"Time elapsed: {minutes} minutes and {seconds} seconds.")

else:
    print(f"Time elapsed: {elapsed} seconds.")

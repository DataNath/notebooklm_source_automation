from playwright.sync_api import sync_playwright, expect
from functions import add_link_sources, file_handler
import time, sys

source_type = input("Enter a source type (Website or YouTube): ").strip().lower()

notebook_name = input("Set a name for your new notebook: ")

start = time.time()

method_dict = {
    "website": add_link_sources,
    "youtube": add_link_sources
}

method = method_dict.get(source_type)
if not method:
    print(f"{source_type} is not a supported source type!")
    sys.exit()
elif method in ("website", "youtube"):
    file_handler(source_type)

# Initialise browser session

with sync_playwright() as sp:
    browser = sp.chromium.launch(headless=False, channel="chrome")
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()

    page.goto("https://notebooklm.google.com/")
    page.wait_for_load_state()

    method(source_type, page)

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

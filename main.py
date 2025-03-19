from playwright.sync_api import sync_playwright, expect
from functions import add_link_sources, create_source_list
from pathlib import Path as p
import time, sys

source_type_raw = input("Enter a source type (Website or YouTube): ")
source_type = source_type_raw.strip().lower()

notebook_name = input("Set a name for your new notebook: ")

start = time.time()

method_dict = {
    "website": add_link_sources,
    "youtube": add_link_sources
}

method = method_dict.get(source_type)

try:
    if not method:
        print(f"{source_type_raw} is not a supported source type!")
        sys.exit()

    urls = create_source_list(source_type)
    
except ValueError as e:
    print(e)
    sys.exit()

# Initialise browser session

with sync_playwright() as sp:
    login_state_path = p(__file__).parent / "state.json"

    browser = sp.chromium.launch(headless=True, channel="chrome")
    context = browser.new_context(storage_state=str(login_state_path))
    page = context.new_page()

    page.goto("https://notebooklm.google.com/")
    page.wait_for_load_state()

    method(source_type, urls, page)

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
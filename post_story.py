import os
import json
import time
import random
from datetime import datetime
from playwright.sync_api import sync_playwright

COOKIES = json.loads(os.environ["IG_COOKIES"])
STORIES = ["stories/1.png", "stories/2.png", "stories/3.png", "stories/4.png", "stories/5.png"]

day_index = datetime.now().timetuple().tm_yday % len(STORIES)
image_path = STORIES[day_index]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(COOKIES)
    page = context.new_page()

    page.goto("https://www.instagram.com/")
    time.sleep(3)

    # Upload story
    page.goto("https://www.instagram.com/")
    time.sleep(2)

    with page.expect_file_chooser() as fc_info:
        page.click("svg[aria-label='New post']")
        time.sleep(1)
    file_chooser = fc_info.value
    file_chooser.set_files(image_path)
    time.sleep(3)

    print(f"Posted {image_path}")
    browser.close()
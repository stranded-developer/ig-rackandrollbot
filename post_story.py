import os
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

COOKIES = json.loads(os.environ["IG_COOKIES"])
STORIES = ["stories/1.png", "stories/2.png", "stories/3.png", "stories/4.png", "stories/5.png"]

day_index = datetime.now().timetuple().tm_yday % len(STORIES)
image_path = STORIES[day_index]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    context.add_cookies(COOKIES)
    page = context.new_page()
    
    page.goto("https://www.instagram.com/")
    time.sleep(4)

    page.screenshot(path="debug.png")

    # Click the + Create button on left sidebar
    try:
        with page.expect_file_chooser(timeout=15000) as fc_info:
            page.click("svg[aria-label='New post']", timeout=10000)
        file_chooser = fc_info.value
        file_chooser.set_files(image_path)
        time.sleep(5)
        page.screenshot(path="after_upload.png")

        # Look for Story option in the menu
        try:
            page.click("text=Story", timeout=8000)
            time.sleep(3)
            page.screenshot(path="story_selected.png")
        except:
            pass

        # Click Add to story / Share
        for btn_text in ["Add to story", "Share to story", "Share"]:
            try:
                page.click(f"text={btn_text}", timeout=5000)
                time.sleep(3)
                print(f"Clicked {btn_text}")
                break
            except:
                pass

        page.screenshot(path="final.png")
        print(f"Posted {image_path}")
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="error.png")
    
    browser.close()
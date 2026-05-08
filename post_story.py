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
    # Use desktop viewport instead of mobile
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    context.add_cookies(COOKIES)
    page = context.new_page()
    
    page.goto("https://www.instagram.com/")
    time.sleep(4)

    # Dismiss popups
    page.mouse.click(195, 538)
    time.sleep(2)
    page.mouse.click(195, 502)
    time.sleep(2)

    page.screenshot(path="debug.png")

    # Click Your story on desktop
    try:
        with page.expect_file_chooser(timeout=15000) as fc_info:
            page.click("button[aria-label='Add to story']", timeout=10000)
        file_chooser = fc_info.value
        file_chooser.set_files(image_path)
        time.sleep(5)
        page.screenshot(path="after_upload.png")

        # Click Share/Add to story button
        try:
            page.click("button:has-text('Add to story')", timeout=8000)
            time.sleep(3)
        except:
            try:
                page.click("button:has-text('Share')", timeout=8000)
                time.sleep(3)
            except:
                pass

        page.screenshot(path="final.png")
        print(f"Posted {image_path}")
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="error.png")
    
    browser.close()
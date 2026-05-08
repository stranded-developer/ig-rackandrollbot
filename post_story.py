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
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    )
    context.add_cookies(COOKIES)
    page = context.new_page()
    
    page.goto("https://www.instagram.com/")
    time.sleep(4)

    # Dismiss first popup (messaging) - click OK by coordinates
    page.mouse.click(194, 437)
    time.sleep(2)

    # Dismiss second popup (save login info) - click Not Now
    try:
        page.click("text=Not now", timeout=5000)
        time.sleep(2)
        print("Dismissed save login popup")
    except:
        pass

    page.screenshot(path="debug.png")

    # Click "Your story" + button
    try:
        with page.expect_file_chooser(timeout=15000) as fc_info:
            page.mouse.click(57, 100)  # Your story circle
        file_chooser = fc_info.value
        file_chooser.set_files(image_path)
        time.sleep(5)
        page.screenshot(path="after_upload.png")

        # Tap "Add to story" or share button
        try:
            page.click("text=Add to story", timeout=8000)
            time.sleep(3)
        except:
            pass

        page.screenshot(path="final.png")
        print(f"Posted {image_path}")
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="error.png")
    
    browser.close()
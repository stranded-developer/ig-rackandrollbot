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
    
    # Dismiss popups
    for text in ["OK", "Not Now", "Cancel"]:
        try:
            page.click(f"text={text}", timeout=3000)
            time.sleep(1)
            print(f"Dismissed {text} popup")
        except:
            pass

    page.screenshot(path="debug.png")

    # Click the + button (top right)
    try:
        with page.expect_file_chooser(timeout=15000) as fc_info:
            # Click the + icon in top nav
            page.click("svg[aria-label='New post']", timeout=10000)
        file_chooser = fc_info.value
        file_chooser.set_files(image_path)
        time.sleep(3)
        
        page.screenshot(path="after_upload.png")
        
        # Select "Story" option if menu appears
        try:
            page.click("text=Story", timeout=5000)
            time.sleep(3)
        except:
            pass

        page.screenshot(path="final.png")
        print(f"Posted {image_path}")
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="error.png")
    
    browser.close()
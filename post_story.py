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

    page.mouse.click(195, 538)
    print("Clicked OK")
    time.sleep(2)
    page.mouse.click(195, 502)
    print("Clicked Not now")
    time.sleep(2)

    page.screenshot(path="debug.png")

    try:
        with page.expect_file_chooser(timeout=15000) as fc_info:
            page.mouse.click(57, 100)
        file_chooser = fc_info.value
        file_chooser.set_files(image_path)
        time.sleep(5)
        page.screenshot(path="after_upload.png")

        # Find and print all clickable elements after upload
        elements = page.evaluate("""
            () => {
                const all = document.querySelectorAll('*');
                const results = [];
                all.forEach(el => {
                    const t = el.innerText?.trim();
                    if (t && t.length < 30 && (
                        el.getAttribute('role') === 'button' ||
                        t.toLowerCase().includes('add') ||
                        t.toLowerCase().includes('share') ||
                        t.toLowerCase().includes('story') ||
                        t.toLowerCase().includes('next')
                    )) {
                        results.push({
                            tag: el.tagName,
                            text: t,
                            role: el.getAttribute('role'),
                            x: el.getBoundingClientRect().x,
                            y: el.getBoundingClientRect().y,
                        });
                    }
                });
                return results;
            }
        """)
        print("Upload screen elements:", elements)

        page.screenshot(path="final.png")
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="error.png")
    
    browser.close()
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

    # Get ALL elements with text OK or Not now
    elements = page.evaluate("""
        () => {
            const all = document.querySelectorAll('*');
            const results = [];
            all.forEach(el => {
                const t = el.innerText?.trim();
                if (t === 'OK' || t === 'Not now' || t === 'Not Now') {
                    results.push({
                        tag: el.tagName,
                        text: t,
                        role: el.getAttribute('role'),
                        x: el.getBoundingClientRect().x,
                        y: el.getBoundingClientRect().y,
                        width: el.getBoundingClientRect().width,
                        height: el.getBoundingClientRect().height,
                    });
                }
            });
            return results;
        }
    """)
    print("Elements:", elements)

    page.screenshot(path="debug.png")
    browser.close()
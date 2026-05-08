import os
import json
from datetime import datetime
from instagrapi import Client

USERNAME = os.environ["IG_USERNAME"]
PASSWORD = os.environ["IG_PASSWORD"]
SESSION_JSON = os.environ.get("IG_SESSION", "")

STORIES = ["stories/1.png", "stories/2.png", "stories/3.png", "stories/4.png", "stories/5.png"]

cl = Client()
if SESSION_JSON:
    cl.set_settings(json.loads(SESSION_JSON))
    try:
        cl.get_timeline_feed()
    except:
        cl.login(USERNAME, PASSWORD)
else:
    cl.login(USERNAME, PASSWORD)

# Pick image based on day of year, cycles through 4
day_index = datetime.now().timetuple().tm_yday % len(STORIES)
image_path = STORIES[day_index]

cl.photo_upload_to_story(image_path)
print(f"Posted {image_path}")
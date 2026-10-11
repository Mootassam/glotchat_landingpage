"""Tell Bing, Yandex, Seznam, Naver… (IndexNow) about every page in the sitemap.
Run after a deploy:   python src/indexnow.py
"""
import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KEY = open(os.path.join(HERE, "indexnow-key.txt"), encoding="utf-8").read().strip()
SITE = "https://www.glotchat.com"
urls = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
body = json.dumps({"host": "www.glotchat.com", "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow: submitted {len(urls)} URLs -> HTTP {r.status}")

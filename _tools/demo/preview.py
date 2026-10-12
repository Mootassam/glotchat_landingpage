"""Render a few frames of each scene for checking: python preview.py <lang> <fmt> [scene ...]"""
import os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "preview"); os.makedirs(OUT, exist_ok=True)
lang, fmt = sys.argv[1], sys.argv[2]
scenes = sys.argv[3:] or ["accounts", "notify", "chat", "voice", "photo"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 640 if fmt == "port" else 1280, "height": 800})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    for sc in scenes:
        pg.goto(f"file:///{HERE}/demo.html?scene={sc}&lang={lang}&fmt={fmt}&record=1".replace("\\", "/"))
        pg.wait_for_timeout(300)
        dur = pg.evaluate("window.DURATION")
        n = 8
        for i in range(n):
            t = round(dur * i / (n - 1), 2)
            pg.evaluate(f"seek({t})")
            pg.screenshot(path=os.path.join(OUT, f"{sc}-{lang}-{fmt}-{i}.png"))
        print(sc, lang, fmt, "duration", round(dur, 1))
    print("errors:", errs)
    b.close()

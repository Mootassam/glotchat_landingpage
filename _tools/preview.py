import sys, os, asyncio
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "preview"); os.makedirs(OUT, exist_ok=True)
times = {"chat": [3.8, 7.0, 9.5, 12.5], "voice": [1.5, 3.2, 6.5], "photo": [1.5, 3.0, 6.0], "accounts": [1.2, 4.0, 6.6, 9.5]}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1200, "height": 750}, device_scale_factor=1)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    for lang in sys.argv[1:] or ["en"]:
        for sc, ts in times.items():
            pg.goto(f"file:///{HERE}/scenes.html?scene={sc}&lang={lang}&record=1".replace("\\", "/"))
            dur = pg.evaluate("window.DURATION")
            for t in ts:
                pg.evaluate(f"seek({t})")
                pg.screenshot(path=os.path.join(OUT, f"{sc}_{lang}_{t}.png"), clip={"x": 0, "y": 0, "width": 1200, "height": 750})
            print(sc, lang, "duration", round(dur, 1))
    print("errors:", errs)
    b.close()

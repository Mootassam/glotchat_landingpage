import os, sys, subprocess, time, json, urllib.parse
from playwright.sync_api import sync_playwright
SITE = r"D:\polychat-landing"; OUT = os.path.join(SITE, "_tools", "shots"); os.makedirs(OUT, exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        for name, vp, mobile in (("desktop", {"width": 1440, "height": 900}, False), ("mobile", {"width": 390, "height": 844}, True)):
            for lang in ("en", "zh"):
                path = "/" if lang == "en" else "/zh/"
                ctx = b.new_context(viewport=vp, device_scale_factor=1, is_mobile=mobile, has_touch=mobile, locale="en-US")
                pg = ctx.new_page(); errs, fails = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "insights" not in m.text and "404" not in m.text else None)
                pg.on("requestfailed", lambda r: fails.append(r.url))
                pg.on("response", lambda r: fails.append(f"{r.status} {r.url}") if r.status >= 400 and "_vercel" not in r.url else None)
                pg.goto(f"http://127.0.0.1:8765{path}", wait_until="networkidle")
                # scroll through the page so lazy media load and reveal animations run
                h = pg.evaluate("document.body.scrollHeight")
                for y in range(0, h, 500): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(120)
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1500)
                vids = pg.evaluate("[...document.querySelectorAll('video.vid')].map(v=>({scene:v.dataset.scene, src:(v.currentSrc||'').split('/').pop(), ready:v.readyState, playing:!v.paused}))")
                href = pg.evaluate("document.querySelector('.hero [data-tg]').href")
                plan = pg.evaluate("document.querySelector('[data-plan=Pro]').href")
                print(f"== {name} {lang}: errors={errs[:3]} failed={fails[:4]}")
                print("   videos:", vids)
                print("   hero link text:", urllib.parse.unquote(href.split('text=')[1])[:80])
                print("   Pro plan link :", urllib.parse.unquote(plan.split('text=')[1])[:80])
                pg.screenshot(path=os.path.join(OUT, f"{name}_{lang}.png"), full_page=True)
                if lang == "en" and name == "desktop":
                    pg.click("[data-tab=voice]"); pg.wait_for_timeout(1500)
                    print("   tab voice ->", pg.evaluate("document.getElementById('demoVid').currentSrc.split('/').pop()"), "| pane:", pg.evaluate("document.querySelector('.pane:not([hidden]) h3').textContent"))
                    pg.click(".lang a[data-lang=zh]"); pg.wait_for_load_state("networkidle")
                    print("   clicked 中文 ->", pg.url, "|", pg.evaluate("document.querySelector('h1').innerText.slice(0,30)"))
                    pg.click(".lang a[data-lang=en]"); pg.wait_for_load_state("networkidle")
                    print("   clicked EN  ->", pg.url, "(stays English: choice remembered)" if pg.evaluate("document.documentElement.lang") == "en" else "WRONG")
                ctx.close()
        # a visitor whose browser is Chinese lands on / -> taken to /zh/ once
        ctx = b.new_context(locale="zh-CN"); pg = ctx.new_page()
        pg.goto("http://127.0.0.1:8765/", wait_until="networkidle")
        print("== Chinese browser opening / ->", pg.url, "|", pg.title())
        ctx.close()
        b.close()
finally:
    srv.terminate()

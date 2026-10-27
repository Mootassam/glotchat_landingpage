"""Browser test of the built site (desktop + phone, several languages):
page errors, failed requests, horizontal overflow, the hero demo player, the feature clips, Telegram links.

    python _tools/check_site.py [langs]    (needs Chrome + Playwright; serves the repo on 127.0.0.1:8765)
"""
import os
import subprocess
import sys
import time
import urllib.parse

from playwright.sync_api import sync_playwright

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "_tools", "shots"); os.makedirs(OUT, exist_ok=True)
LANGS = sys.argv[1:] or ["en", "zh", "ar", "tr", "es", "pt", "ru"]
problems = []


def check(ok, what):
    print(("   ok  " if ok else "   FAIL ") + what)
    if not ok:
        problems.append(what)


srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1"], cwd=SITE,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        for name, vp, mobile in (("desktop", {"width": 1440, "height": 900}, False), ("phone", {"width": 390, "height": 844}, True)):
            fmt = "port" if mobile else "land"
            for lang in LANGS:
                path = "/" if lang == "en" else f"/{lang}/"
                ctx = b.new_context(viewport=vp, is_mobile=mobile, has_touch=mobile, locale="en-US")
                pg = ctx.new_page(); errs, fails = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "404" not in m.text else None)
                pg.on("response", lambda r: fails.append(f"{r.status} {r.url}") if r.status >= 400 and "_vercel" not in r.url else None)
                pg.goto(f"http://127.0.0.1:8765{path}?nolang=1", wait_until="load")
                print(f"== {name} {lang}")
                pg.wait_for_timeout(2500)
                st = pg.evaluate("""() => { const v = [...document.querySelectorAll('.player video.pv')].find(x => x.classList.contains('on'));
                    return v ? { src: v.currentSrc.split('/').pop(), t: v.currentTime, paused: v.paused } : null; }""")
                check(bool(st) and st["src"] == f"accounts-{lang}-{fmt}.mp4" and not st["paused"] and st["t"] > 0.5,
                      f"hero player plays chapter 1 by itself ({st})")
                bar = pg.evaluate("parseFloat(document.querySelector('.steps2 [aria-selected=true] .bar i').style.width) || 0")
                check(bar > 0, f"chapter progress bar moves ({bar:.0f}%)")
                pg.click(".steps2 [data-ch=chat]"); pg.wait_for_timeout(2500)
                st = pg.evaluate("""() => { const v = [...document.querySelectorAll('.player video.pv')].find(x => x.classList.contains('on'));
                    return { src: v && v.currentSrc.split('/').pop(), cap: document.querySelector('.player .cap').textContent,
                             want: document.querySelector('.steps2 [data-ch=chat]').dataset.cap }; }""")
                check(st["src"] == f"chat-{lang}-{fmt}.mp4" and st["cap"] == st["want"], f"chapter 3 click switches video + caption ({st['src']})")
                pg.screenshot(path=os.path.join(OUT, f"{name}_{lang}_hero.png"))
                pg.evaluate("window.scrollTo(0, 0)")
                pg.click(".hero [data-watch]"); pg.wait_for_timeout(1500)
                full = pg.evaluate("document.querySelector('.player').classList.contains('full')")
                cur = pg.evaluate("[...document.querySelectorAll('.player video.pv')].find(x => x.classList.contains('on'))?.currentSrc.split('/').pop()")
                check(full and cur == f"accounts-{lang}-{fmt}.mp4", f"'Watch it work' opens full screen from chapter 1 ({cur})")
                pg.screenshot(path=os.path.join(OUT, f"{name}_{lang}_full.png"))
                pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
                check(not pg.evaluate("document.querySelector('.player').classList.contains('full')"), "Esc closes full screen")
                pg.evaluate("document.querySelector('.show .srow:nth-of-type(3) video').scrollIntoView({block: 'center'})")
                pg.wait_for_timeout(2500)
                clip = pg.evaluate("(() => { const v = document.querySelector('.show .srow:nth-of-type(3) video'); return { src: v.currentSrc.split('/').pop(), t: v.currentTime }; })()")
                check(clip["src"] == f"chat-{lang}-{fmt}.mp4" and clip["t"] > 0.3, f"feature clip loads + plays when scrolled to ({clip})")
                h = pg.evaluate("document.body.scrollHeight")
                for y in range(0, h, 700):
                    pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
                sw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                check(sw[0] <= sw[1], f"no sideways scrolling ({sw[0]} <= {sw[1]})")
                href = pg.evaluate("document.querySelector('.nav [data-tg]').href")
                check("?text=" in href, "Telegram button has a pre-filled message: " + urllib.parse.unquote(href.split("text=")[-1])[:60])
                check(not errs, f"no page errors {errs[:2]}")
                check(not fails, f"no failed requests {fails[:3]}")
                ctx.close()
        b.close()
finally:
    srv.terminate()
print("\nALL GOOD" if not problems else f"\n{len(problems)} PROBLEM(S):\n - " + "\n - ".join(problems))
sys.exit(1 if problems else 0)

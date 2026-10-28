"""Render the GlotChat video ads (Facebook / Instagram).

    python _tools/ad/record_ad.py                         every language, both formats, both lengths
    python _tools/ad/record_ad.py en --fmt story --cut full
    python _tools/ad/record_ad.py en --preview            a contact sheet of still frames, no video

Output: D:/glotchat-marketing/ads/glotchat-<cut>-<story|feed>-<lang>.mp4 (+ .jpg cover)
  story = 1080x1920 (9:16) for Reels / Stories, feed = 1080x1350 (4:5) for Feed.
"""
import os
import shutil
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
OUT = r"D:\glotchat-marketing\ads"
FPS = 30
LANGS = ["en", "zh", "ar", "tr", "es", "pt", "ru"]


def opt(args, name, default):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v.split(",")
    return default


def main():
    args = sys.argv[1:]
    fmts = opt(args, "--fmt", ["story", "feed"]); cuts = opt(args, "--cut", ["full", "short"])
    port = int(opt(args, "--port", ["8771"])[0])
    preview = "--preview" in args
    langs = [a for a in args if not a.startswith("--")] or LANGS
    os.makedirs(OUT, exist_ok=True)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=SITE,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            for fmt in fmts:
                h = 960 if fmt == "story" else 675
                pg = b.new_page(viewport={"width": 540, "height": h}, device_scale_factor=2)
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                for lang in langs:
                    for cut in cuts:
                        pg.goto(f"http://127.0.0.1:{port}/_tools/ad/ad.html?lang={lang}&fmt={fmt}&cut={cut}&record=1")
                        pg.wait_for_function("window.READY === true", timeout=60000)
                        pg.wait_for_timeout(300)
                        dur = pg.evaluate("window.DURATION")
                        name = f"glotchat-{cut}-{fmt}-{lang}"
                        if preview:
                            shots = []
                            for t in [0.6, 2.0, 3.0, 4.6] + [s for s in pg.evaluate("window.FEATURE_MIDS || []")] + [dur - 2.0, dur - 0.2]:
                                pg.evaluate(f"seekAd({t})"); pg.wait_for_timeout(30)
                                f = os.path.join(OUT, "_preview", f"{name}-{t:05.1f}.png"); os.makedirs(os.path.dirname(f), exist_ok=True)
                                pg.screenshot(path=f); shots.append(f)
                            print(name, "preview", len(shots), "frames", errs or "")
                            continue
                        mp4 = os.path.join(OUT, name + ".mp4")
                        if os.path.exists(mp4) and os.path.getsize(mp4) > 200_000:
                            print(name, "already done"); continue
                        tmp = os.path.join(HERE, "frames", name)
                        n = int(dur * FPS)
                        have = len(os.listdir(tmp)) if os.path.isdir(tmp) else 0
                        if have != n:                           # frames left by an interrupted run are reused
                            shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
                            for i in range(n):
                                pg.evaluate(f"seekAd({i / FPS})")
                                pg.screenshot(path=os.path.join(tmp, f"{i:05d}.png"))
                        # H.264 high profile, 30 fps, silent AAC track (some placements expect audio), fast start
                        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"),
                                        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                                        "-c:v", "libx264", "-preset", "medium", "-threads", "4", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
                                        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4], check=True)
                        # cover image = the brand frame
                        cover = int(min(n - 1, (pg.evaluate("window.COVER_T || 4.2")) * FPS))
                        shutil.copy(os.path.join(tmp, f"{cover:05d}.png"), os.path.join(OUT, name + "-cover.png"))
                        print(f"{name}: {dur:.1f}s, {os.path.getsize(mp4) // 1024} KB {errs or ''}", flush=True)
                        shutil.rmtree(tmp, ignore_errors=True)
                pg.close()
            b.close()
    finally:
        srv.terminate()


if __name__ == "__main__":
    main()

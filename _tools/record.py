"""Record every demo scene (EN + 中文) frame by frame -> MP4 (page) + GIF (sharing) + poster."""
import os, shutil, subprocess, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
MEDIA = os.path.join(SITE, "assets", "media"); GIF = os.path.join(SITE, "assets", "gif")
os.makedirs(MEDIA, exist_ok=True); os.makedirs(GIF, exist_ok=True)
FPS = 25
scenes = sys.argv[1:] or ["chat", "voice", "photo", "accounts"]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1200, "height": 750}, device_scale_factor=2)
    for lang in ("en", "zh"):
        for sc in scenes:
            tmp = os.path.join(HERE, "frames", f"{sc}-{lang}"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
            pg.goto(f"file:///{HERE}/scenes.html?scene={sc}&lang={lang}&record=1".replace("\\", "/"))
            pg.wait_for_timeout(300)
            dur = pg.evaluate("window.DURATION") + 0.8          # short hold on the final state
            n = int(dur * FPS)
            for i in range(n):
                pg.evaluate(f"seek({i / FPS})")
                pg.screenshot(path=os.path.join(tmp, f"{i:04d}.png"), clip={"x": 0, "y": 0, "width": 1200, "height": 750})
            base = f"{sc}-{lang}"
            src = os.path.join(tmp, "%04d.png")
            run = lambda args: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)
            # page video: H.264, 1600 px, fast start, loops silently
            run(["-framerate", str(FPS), "-i", src, "-vf", "scale=1600:-2:flags=lanczos", "-c:v", "libx264", "-preset", "slow",
                 "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", os.path.join(MEDIA, base + ".mp4")])
            # poster = the final, fully explained state
            run(["-i", os.path.join(tmp, f"{n - 1:04d}.png"), "-vf", "scale=1600:-2:flags=lanczos", "-quality", "82", os.path.join(MEDIA, base + ".webp")])
            # GIF for Telegram / social posts: 800 px, 12 fps, optimised palette
            run(["-framerate", str(FPS), "-i", src, "-filter_complex",
                 "[0:v]fps=12,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                 "-loop", "0", os.path.join(GIF, base + ".gif")])
            sizes = {e: os.path.getsize(os.path.join(MEDIA if e != "gif" else GIF, base + "." + e)) // 1024 for e in ("mp4", "webp", "gif")}
            print(base, f"{dur:.1f}s {n} frames", sizes, flush=True)
            shutil.rmtree(tmp, ignore_errors=True)
    b.close()

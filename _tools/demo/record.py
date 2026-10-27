"""Record the demo scenes frame by frame -> MP4 + poster (website) and GIF (Telegram / social posts).

    python _tools/demo/record.py                     every language, scene and format
    python _tools/demo/record.py en zh               only these languages
    python _tools/demo/record.py en --scene chat     one scene

Website files:  assets/media/<scene>-<lang>-<land|port>.mp4 / .webp
GIFs:           D:/glotchat-marketing/gifs/<scene>-<lang>.gif   (landscape, outside the website repo)
"""
import os
import shutil
import subprocess
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
MEDIA = os.path.join(SITE, "assets", "media")
GIFS = r"D:\glotchat-marketing\gifs"
FPS = 25
SCALE = 1.25                                     # 1280x800 stage -> 1600x1000 video, 640x800 -> 800x1000
LANGS = ["en", "zh", "ar", "tr", "es", "pt", "ru"]
SCENES = ["accounts", "notify", "chat", "telegram", "voice", "photo"]


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def main():
    args = sys.argv[1:]
    scenes = SCENES
    if "--scene" in args:
        i = args.index("--scene"); scenes = args[i + 1].split(","); del args[i:i + 2]
    langs = args or LANGS
    os.makedirs(MEDIA, exist_ok=True); os.makedirs(GIFS, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        for fmt in ("land", "port"):
            vw = 1280 if fmt == "land" else 640
            pg = b.new_page(viewport={"width": vw, "height": 800}, device_scale_factor=SCALE)
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            for lang in langs:
                for sc in scenes:
                    base = f"{sc}-{lang}-{fmt}"
                    tmp = os.path.join(HERE, "frames", base)
                    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
                    pg.goto(f"file:///{HERE}/demo.html?scene={sc}&lang={lang}&fmt={fmt}&record=1".replace("\\", "/"))
                    pg.wait_for_timeout(250)
                    dur = pg.evaluate("window.DURATION") + 1.0          # hold the final state for a second
                    n = int(dur * FPS)
                    for i in range(n):
                        pg.evaluate(f"seek({i / FPS})")
                        pg.screenshot(path=os.path.join(tmp, f"{i:04d}.png"))
                    src = os.path.join(tmp, "%04d.png")
                    # web video: H.264, silent, fast start (plays like a GIF but ~10x smaller)
                    ff("-framerate", str(FPS), "-i", src, "-c:v", "libx264", "-preset", "slow", "-crf", "25",
                       "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", os.path.join(MEDIA, base + ".mp4"))
                    # poster = the last frame: the finished, fully translated state
                    ff("-i", os.path.join(tmp, f"{n - 1:04d}.png"), "-quality", "80", os.path.join(MEDIA, base + ".webp"))
                    if fmt == "land":
                        ff("-framerate", str(FPS), "-i", src, "-filter_complex",
                           "[0:v]fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];"
                           "[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                           "-loop", "0", os.path.join(GIFS, f"{sc}-{lang}.gif"))
                    kb = os.path.getsize(os.path.join(MEDIA, base + ".mp4")) // 1024
                    print(f"{base}: {dur:.1f}s {n} frames, mp4 {kb} KB", flush=True)
                    shutil.rmtree(tmp, ignore_errors=True)
            pg.close()
            if errs:
                print("PAGE ERRORS:", errs)
        b.close()


if __name__ == "__main__":
    main()

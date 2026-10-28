"""30-second GlotChat ad (light style) with voice-over, subtitles, music and sound effects.

    python _tools/ad/promo_build.py en zh                 voice + timeline + video, both formats
    python _tools/ad/promo_build.py en --fmt feed
    python _tools/ad/promo_build.py en --preview          voice + timeline + still frames only

Needs the same tools as explainer_build.py (kokoro-onnx, misaki[zh], Chrome + Playwright, ffmpeg).
Output: D:/glotchat-marketing/ads-30s/glotchat-30s-<lang>-<feed|story>.mp4 (+ cover .png, voice-over .wav, script .txt)
"""
import json
import os
import shutil
import subprocess
import sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import explainer_build as eb  # noqa: E402  (voice model setup, trim, local server)

SITE = eb.SITE
OUT = r"D:\glotchat-marketing\ads-30s"
WORK = os.path.join(OUT, "_work")
FPS = 30
SR = 44100
PAGE = "promo"            # template _tools/ad/<PAGE>.html, timeline <PAGE>-<lang>.json
PREFIX = "glotchat-30s"   # output file names
DRUMS_AT = 4.4           # full beat starts here (seconds)

# fixed timeline: 30.0 s in total. "ev" = moments inside a scene (seconds from the scene start), shared with promo.html
SECTIONS = [
    {"id": "hook", "dur": 4.4, "ev": {"b": [0.2, 0.55, 0.9, 1.25], "no": 2.4}},
    {"id": "brand", "dur": 3.6, "ev": {}},
    {"id": "chat", "dur": 7.8, "ev": {"in1": 0.55, "tr1": 1.15, "type": 2.5, "out": 4.1, "in2": 5.5, "tr2": 6.0}},
    {"id": "feat", "dur": 6.0, "ev": {"c": [0.2, 2.1, 4.0]}},
    {"id": "stats", "dur": 3.7, "ev": {}},
    {"id": "end", "dur": 4.5, "ev": {}},
]
CAPS = {"chat", "feat", "stats"}          # scenes that show the narration as subtitles

# narration: text to speak, or (spoken, shown); "at" = earliest start inside the scene
SCRIPT = {
    "en": {
        "hook": [{"t": "Customers worldwide are messaging you…", "at": 0.25}, {"t": "but you can't read a word?", "at": 2.4}],
        "brand": [{"t": "Meet GlotChat.", "at": 0.3}, {"t": "Now you understand every customer."}],
        "chat": [{"t": "Every message is translated instantly.", "at": 0.35}, {"t": "You reply in English, and they read their own language.", "at": 2.6}],
        "feat": [{"t": "Voice notes become text.", "at": 0.3}, {"t": "Photos get translated.", "at": 2.2}, {"t": "All your WhatsApp numbers, one window.", "at": 4.05}],
        "stats": [{"t": ("Forty-nine languages, offline and private, on your PC.", "49 languages — offline and private, on your PC."), "at": 0.2}],
        "end": [{"t": ("Try GlotChat free for three days.", "Try GlotChat free for 3 days."), "at": 0.3}, {"t": "Contact us now!"}],
    },
    "zh": {
        "hook": [{"t": "客户来自世界各地，", "at": 0.25}, {"t": "可你看不懂他们的语言？", "at": 2.4}],
        "brand": [{"t": "试试 GlotChat。", "at": 0.3}, {"t": "每位客户，你都看得懂。"}],
        "chat": [{"t": "每条消息都会即时翻译。", "at": 0.35}, {"t": "你用中文回复，客户读他们的语言。", "at": 2.6}],
        "feat": [{"t": "语音变成文字。", "at": 0.3}, {"t": "图片也能翻译。", "at": 2.2}, {"t": "所有号码，一个窗口。", "at": 4.05}],
        "stats": [{"t": ("四十九种语言，离线、私密，就在你的电脑上。", "49 种语言，离线、私密，就在你的电脑上。"), "at": 0.2}],
        "end": [{"t": ("免费试用三天。", "免费试用 3 天。"), "at": 0.3}, {"t": "马上联系我们！"}],
    },
}

TABS = [["Shop UAE", "#f59e0b", 3], ["Sales EU", "#10b981", 7], ["Export", "#ef4444", 2], ["Support", "#6366f1", 5], ["Store", "#0ea5e9", 4]]
TEXT = {
    "en": {
        "hook": {"title": 'Customers from <span class="grad">all over the world</span>?', "no": "…but you can't read a word 😵",
                 "bubs": [{"n": "Ahmed", "lang": "Arabic", "c": "#f59e0b", "m": "مرحبا، هل المنتج متوفر؟"},
                          {"n": "Lucía", "lang": "Spanish", "c": "#10b981", "m": "¿Hacen envíos a México?"},
                          {"n": "Wei", "lang": "Chinese", "c": "#ef4444", "m": "你好，可以发样品吗？"},
                          {"n": "Emre", "lang": "Turkish", "c": "#6366f1", "m": "Merhaba, stokta var mı?"}]},
        "brand": {"line": "Understand every customer."},
        "chat": {"title": 'Translated <span class="grad">instantly</span> — both ways', "name": "Ahmed · Shop UAE", "status": "online",
                 "pair": "Arabic ⇄ English", "in1": "مرحبا، هل يمكنك الشحن إلى دبي؟", "code1": "AR→EN", "tr1": "Hi, can you ship to Dubai?",
                 "reply": "Yes! It ships tomorrow 🚚", "out": "نعم! سيتم الشحن غدًا 🚚", "code2": "EN→AR",
                 "in2": "رائع، شكرًا جزيلًا! 🙏", "tr2": "Great, thank you so much! 🙏", "placeholder": "Type in English…", "sent": "Sent in Arabic"},
        "feat": {"title": 'And <span class="grad">so much more</span>', "cards": [
            {"icon": "🎤", "bg": "#e0f2fe", "h": "Voice notes → text", "code": "ES→EN", "text": "“Do you have it in blue?”"},
            {"icon": "📷", "bg": "#fef3c7", "h": "Photos → translated", "code": "ES→EN", "paperH": "Pedido", "paper": "20 cajas · azul", "text": "Order: 20 boxes · blue"},
            {"icon": "📱", "bg": "#dcfce7", "h": "All your numbers, one window", "tabs": TABS}]},
        "stats": {"label": "languages", "chips": ["🔒 Private", "⚡ Works offline", "💻 On your PC"]},
        "end": {"h": "Try it FREE for 3 days", "pts": ["No payment to start", "Windows 10 & 11"], "cta": "Contact us now",
                "legal": "GlotChat is not affiliated with WhatsApp or Meta."},
    },
    "zh": {
        "hook": {"title": '<span class="grad">全世界</span>的客户都在找你？', "no": "……可你一个字都看不懂 😵",
                 "bubs": [{"n": "Ahmed", "lang": "阿拉伯语", "c": "#f59e0b", "m": "مرحبا، هل المنتج متوفر؟"},
                          {"n": "Lucía", "lang": "西班牙语", "c": "#10b981", "m": "¿Hacen envíos a México?"},
                          {"n": "John", "lang": "英语", "c": "#ef4444", "m": "Hi, can you send a sample?"},
                          {"n": "Emre", "lang": "土耳其语", "c": "#6366f1", "m": "Merhaba, stokta var mı?"}]},
        "brand": {"line": "每位客户，你都看得懂。"},
        "chat": {"title": '<span class="grad">即时翻译</span> · 双向沟通', "name": "Ahmed · Shop UAE", "status": "在线",
                 "pair": "阿拉伯语 ⇄ 中文", "in1": "مرحبا، هل يمكنك الشحن إلى دبي؟", "code1": "AR→ZH", "tr1": "你好，可以发货到迪拜吗？",
                 "reply": "可以！明天就发货 🚚", "out": "نعم! سيتم الشحن غدًا 🚚", "code2": "ZH→AR",
                 "in2": "رائع، شكرًا جزيلًا! 🙏", "tr2": "太好了，非常感谢！🙏", "placeholder": "用中文输入…", "sent": "已用阿拉伯语发送"},
        "feat": {"title": '还有<span class="grad">更多功能</span>', "cards": [
            {"icon": "🎤", "bg": "#e0f2fe", "h": "语音 → 文字", "code": "ES→ZH", "text": "“有蓝色的吗？”"},
            {"icon": "📷", "bg": "#fef3c7", "h": "图片 → 翻译", "code": "ES→ZH", "paperH": "Pedido", "paper": "20 cajas · azul", "text": "订单：20 箱 · 蓝色"},
            {"icon": "📱", "bg": "#dcfce7", "h": "所有号码，一个窗口", "tabs": TABS}]},
        "stats": {"label": "种翻译语言", "chips": ["🔒 私密", "⚡ 离线可用", "💻 在你的电脑上"]},
        "end": {"h": "免费试用 3 天", "pts": ["无需付款即可开始", "支持 Windows 10 和 11"], "cta": "立即联系我们",
                "legal": "GlotChat 与 WhatsApp 或 Meta 无关联。"},
    },
}


# ------------------------------------------------------------------ voice
def voice_model(lang):
    from kokoro_onnx import Kokoro
    M = eb.MODELS
    if lang == "zh":
        from misaki import espeak, zh
        eng = espeak.EspeakG2P(language="en-us")
        g2p = zh.ZHG2P(version="1.1", en_callable=lambda t: eng(t)[0])
        k = Kokoro(M + r"\kokoro-v1.1-zh.onnx", M + r"\voices-v1.1-zh.bin", vocab_config=M + r"\config-v1.1-zh.json")
        return lambda text, sp: k.create(g2p(text)[0], voice=eb.VOICE[lang], speed=sp, is_phonemes=True)
    k = Kokoro(M + r"\kokoro-v1.0.onnx", M + r"\voices-v1.0.bin")
    return lambda text, sp: k.create(text, voice=eb.VOICE[lang], speed=sp, lang="en-us")


def timeline(lang):
    """Speak every line, place it in its scene, speed a line up (max 1.3x) if it would overrun."""
    say = voice_model(lang)
    d = os.path.join(WORK, lang); os.makedirs(d, exist_ok=True)
    t, secs, track = 0.0, [], []
    for s in SECTIONS:
        lines = SCRIPT[lang][s["id"]]
        caps, prev_end = [], 0.0
        for i, ln in enumerate(lines):
            spoken, shown = ln["t"] if isinstance(ln["t"], tuple) else (ln["t"], ln["t"])
            start = max(ln.get("at", 0.0), prev_end + 0.2)
            nxt = lines[i + 1].get("at") if i + 1 < len(lines) else None
            limit = (nxt - 0.1) if nxt else s["dur"] - (0.9 if s["id"] == "end" else 0.15)
            sp = 1.0
            for _ in range(4):
                audio, sr = say(spoken, sp); audio = eb.trim(audio, sr); dur = len(audio) / sr
                if start + dur <= limit or sp >= 1.3:
                    break
                sp = min(1.3, sp * dur / max(0.3, limit - start) * 1.02)
            if start + dur > limit:
                print(f"  ! {lang}/{s['id']}/{i}: {dur:.2f}s does not fit ({limit - start:.2f}s)", flush=True)
            p = os.path.join(d, f"{s['id']}-{i}.wav"); sf.write(p, audio, sr)
            caps.append({"t0": round(t + start, 3), "t1": round(t + start + dur, 3), "show": shown})
            track.append((t + start, p)); prev_end = start + dur
            print(f"  {lang}/{s['id']}/{i}: {dur:.2f}s at {start:.2f} speed {sp:.2f}", flush=True)
        secs.append({"id": s["id"], "start": round(t, 3), "dur": s["dur"], "ev": s["ev"], "caps": caps, "showCaps": s["id"] in CAPS})
        t += s["dur"]
    return {"lang": lang, "duration": round(t, 3), "sections": secs, "text": TEXT[lang]}, track, sr


# ------------------------------------------------------------------ music + sound effects (generated, no licence questions)
def music(seconds, sr=SR):
    n = int(seconds * sr); t = np.arange(n) / sr
    L = np.zeros(n); R = np.zeros(n)
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    bpm = 112; beat = 60 / bpm; bar = beat * 4
    chords = [[48, 55, 60, 64, 67], [43, 50, 55, 59, 62], [45, 52, 57, 60, 64], [41, 48, 53, 57, 60]]   # C  G  Am  F
    for ci in range(int(seconds / bar) + 2):
        ch = chords[ci % 4]; t0 = ci * bar
        a, b = int(t0 * sr), min(n, int((t0 + bar + 0.6) * sr))
        if a >= b:
            continue
        tt = t[a:b] - t0; env = np.clip(tt / 0.25, 0, 1) * np.clip((bar + 0.6 - tt) / 0.6, 0, 1)
        for j, m in enumerate(ch[1:]):
            f = hz(m); v = (np.sin(2 * np.pi * f * 0.997 * tt) + np.sin(2 * np.pi * f * 1.003 * tt)) * env * 0.035
            L[a:b] += v * (0.65 if j % 2 else 0.35); R[a:b] += v * (0.35 if j % 2 else 0.65)
        for k in range(8):                                   # bouncy bass on eighths
            b0 = t0 + k * beat / 2; ba, bb = int(b0 * sr), min(n, int((b0 + 0.22) * sr))
            if ba >= n:
                break
            tb = t[ba:bb] - b0; f = hz(ch[0] - 12 + (12 if k % 4 == 3 else 0))
            v = np.sin(2 * np.pi * f * tb) * np.exp(-tb * 9) * 0.11
            L[ba:bb] += v; R[ba:bb] += v
    step = beat / 2                                          # bright pluck arpeggio
    for k in range(int(seconds / step)):
        t0 = k * step; ch = chords[int(t0 / bar) % 4]; m = ch[[2, 3, 4, 3, 2, 4, 3, 1][k % 8]] + 12
        a, b = int(t0 * sr), min(n, int((t0 + 0.6) * sr)); tt = t[a:b] - t0; f = hz(m)
        v = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) + 0.35 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 12)) * 0.04
        pan = 0.5 + 0.35 * np.sin(k * 0.8); L[a:b] += v * (1 - pan); R[a:b] += v * pan
    rng = np.random.default_rng(7)
    for k in range(int(seconds / beat)):                    # soft kick on every beat, hat on the off-beat (from the brand scene on)
        t0 = k * beat; a, b = int(t0 * sr), min(n, int((t0 + 0.3) * sr)); tt = t[a:b] - t0
        gain = 0.35 if t0 < DRUMS_AT else 1.0
        kick = np.sin(2 * np.pi * (48 * tt + 90 / 30 * (1 - np.exp(-tt * 30)))) * np.exp(-tt * 11) * 0.22 * gain
        L[a:b] += kick; R[a:b] += kick
        if t0 >= DRUMS_AT:
            h0 = t0 + beat / 2; ha, hb = int(h0 * sr), min(n, int((h0 + 0.06) * sr))
            if ha < n:
                th = t[ha:hb] - h0; hat = np.diff(rng.standard_normal(hb - ha + 1)) * np.exp(-th * 70) * 0.025
                L[ha:hb] += hat * 0.8; R[ha:hb] += hat
    st = np.stack([L, R], 1)
    fade = np.ones(n); fi, fo = int(0.3 * sr), int(2.0 * sr)
    fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
    st *= fade[:, None]; st /= max(1e-9, np.abs(st).max()) / 0.5
    return st.astype(np.float32)


def promo_sfx(data):
    s = {x["id"]: x for x in data["sections"]}; ev = []
    ev += [("pop", s["hook"]["start"] + b) for b in s["hook"]["ev"]["b"]]
    ev += [("woosh", s["brand"]["start"] + 0.05), ("chime", s["brand"]["start"] + 0.4)]
    c = s["chat"]; ev += [("pop", c["start"] + c["ev"][k]) for k in ("in1", "in2")] + [("woosh", c["start"] + c["ev"]["out"] - 0.1)]
    ev += [("tick", s["feat"]["start"] + x) for x in s["feat"]["ev"]["c"]]
    ev += [("tick", s["stats"]["start"] + 1.0 + i * 0.22) for i in range(3)]
    ev += [("chime", s["end"]["start"] + 0.1)]
    return ev


def sfx_events(data):
    return SFX_EVENTS(data)


SFX_EVENTS = promo_sfx


def sfx(seconds, events, sr=SR):
    n = int(seconds * sr); out = np.zeros(n); rng = np.random.default_rng(3)
    for kind, t0 in events:
        if kind == "pop":
            ln = 0.09; tt = np.arange(int(ln * sr)) / sr; f = 900 * np.exp(-tt * 18) + 380
            snd = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-tt * 38) * 0.5
        elif kind == "tick":
            ln = 0.06; tt = np.arange(int(ln * sr)) / sr
            snd = np.sin(2 * np.pi * 1500 * tt) * np.exp(-tt * 70) * 0.3
        elif kind == "woosh":
            ln = 0.38; m = int(ln * sr); tt = np.arange(m) / sr
            noise = np.convolve(rng.standard_normal(m), np.ones(12) / 12, mode="same")
            snd = noise * np.sin(np.pi * tt / ln) ** 2 * 0.5
        else:   # chime
            ln = 1.4; tt = np.arange(int(ln * sr)) / sr
            snd = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * dk) * g for f, dk, g in [(1046.5, 3.5, 0.25), (1568, 4.5, 0.18), (2093, 6, 0.1)])
        a = int(t0 * sr); b = min(n, a + len(snd)); out[a:b] += snd[: b - a]
    return np.stack([out, out], 1).astype(np.float32)


def mix(lang, data, track, vsr):
    total = data["duration"]
    v = np.zeros(int(total * vsr), dtype=np.float32)
    for t0, p in track:
        a, _ = sf.read(p, dtype="float32"); i = int(t0 * vsr); v[i:i + len(a)] += a[: len(v) - i]
    vp = os.path.join(WORK, f"voice-{lang}.wav"); sf.write(vp, v, vsr)
    mp = os.path.join(WORK, f"music-{lang}.wav"); sf.write(mp, music(total), SR)
    xp = os.path.join(WORK, f"sfx-{lang}.wav"); sf.write(xp, sfx(total, sfx_events(data)), SR)
    final = os.path.join(WORK, f"mix-{lang}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vp, "-i", mp, "-i", xp, "-filter_complex",
                    "[0:a]aresample=44100,aformat=channel_layouts=stereo,asplit=2[v1][v2];"
                    "[1:a]volume=0.42[m];[m][v1]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=350[md];"
                    "[2:a]volume=0.55[x];"
                    "[md][v2][x]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad,atrim=0:" + f"{total:.3f}" + "[a]",
                    "-map", "[a]", "-ar", "48000", final], check=True)
    shutil.copy(vp, os.path.join(OUT, f"{PREFIX}-{lang}-voiceover.wav"))
    return final


# ------------------------------------------------------------------ video
def render(lang, fmt, port, audio, preview=False):
    from playwright.sync_api import sync_playwright
    name = f"{PREFIX}-{lang}-{fmt}"
    h = 960 if fmt == "story" else 675
    data = json.load(open(os.path.join(HERE, f"{PAGE}-{lang}.json"), encoding="utf-8"))
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 540, "height": h}, device_scale_factor=2)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"http://127.0.0.1:{port}/_tools/ad/{PAGE}.html?lang={lang}&fmt={fmt}&record=1")
        pg.wait_for_function("window.READY === true", timeout=60000); pg.wait_for_timeout(300)
        if preview:
            d = os.path.join(WORK, "preview"); os.makedirs(d, exist_ok=True)
            for s in data["sections"]:
                for f in (0.3, 0.65, 0.95):
                    t = s["start"] + s["dur"] * f
                    pg.evaluate(f"seekAd({t})"); pg.screenshot(path=os.path.join(d, f"{name}-{t:05.2f}-{s['id']}.png"))
            print(name, "preview", errs or "", flush=True); b.close(); return
        tmp = os.path.join(WORK, "frames", name); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        n = int(round(data["duration"] * FPS))
        for i in range(n):
            pg.evaluate(f"seekAd({i / FPS})"); pg.screenshot(path=os.path.join(tmp, f"{i:05d}.png"))
        b.close()
    brand = next(s for s in data["sections"] if s["id"] == "brand")
    shutil.copy(os.path.join(tmp, f"{int((brand['start'] + brand['dur'] * 0.9) * FPS):05d}.png"), os.path.join(OUT, name + "-cover.png"))
    mp4 = os.path.join(OUT, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"), "-i", audio,
                    "-c:v", "libx264", "-preset", "medium", "-threads", "4", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", mp4 + ".tmp.mp4"], check=True)
    try:
        os.replace(mp4 + ".tmp.mp4", mp4)
    except PermissionError:                      # the old video is open in a player: keep both
        os.replace(mp4 + ".tmp.mp4", mp4[:-4] + "-new.mp4"); mp4 = mp4[:-4] + "-new.mp4"
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{name}: {data['duration']:.1f}s, {os.path.getsize(mp4) // 1024} KB {errs or ''}", flush=True)


def main():
    args = sys.argv[1:]
    fmts = ["feed", "story"]
    if "--fmt" in args:
        i = args.index("--fmt"); fmts = args[i + 1].split(","); del args[i:i + 2]
    preview = "--preview" in args
    skip_voice = "--skip-voice" in args
    langs = [a for a in args if not a.startswith("--")] or ["en", "zh"]
    os.makedirs(WORK, exist_ok=True)
    port = 8700 + (os.getpid() % 90)
    srv = eb.server(port)
    try:
        for lang in langs:
            jpath = os.path.join(HERE, f"{PAGE}-{lang}.json"); mixed = os.path.join(WORK, f"mix-{lang}.wav")
            if not (skip_voice and os.path.exists(jpath) and os.path.exists(mixed)):
                data, track, vsr = timeline(lang)
                json.dump(data, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                mixed = mix(lang, data, track, vsr)
                with open(os.path.join(OUT, f"{PREFIX}-{lang}-script.txt"), "w", encoding="utf-8") as f:
                    for s in data["sections"]:
                        for c in s["caps"]:
                            f.write(f"[0:{c['t0']:05.2f}] {c['show']}\n")
                print(f"{lang}: timeline {data['duration']:.1f}s", flush=True)
            for fmt in fmts:
                render(lang, fmt, port, mixed, preview)
    finally:
        srv.terminate()


if __name__ == "__main__":
    main()

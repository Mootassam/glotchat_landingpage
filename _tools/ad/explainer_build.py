"""Long GlotChat explainer ad (~1.5 min) with voice-over, subtitles and background music.

    python _tools/ad/explainer_build.py en zh                 voice + timeline + video for both languages, both formats
    python _tools/ad/explainer_build.py en --fmt feed
    python _tools/ad/explainer_build.py en --preview          voice + timeline + a few still frames only

Needs: kokoro-onnx + misaki[zh] (voice), models in D:/glotchat-marketing/tts-models, Chrome + Playwright, ffmpeg.
Output: D:/glotchat-marketing/ads-long/glotchat-explainer-<lang>-<feed|story>.mp4 (+ cover .png, voice-over .wav, script .txt)
"""
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(os.path.dirname(HERE))
OUT = r"D:\glotchat-marketing\ads-long"
WORK = os.path.join(OUT, "_work")
MODELS = r"D:\glotchat-marketing\tts-models"
FPS = 30
VOICE = {"en": "af_heart", "zh": "zf_001"}

# ------------------------------------------------------------------ script
# each sentence: text to speak, or (text to speak, text to show) when they differ
SCRIPT = {
    "en": {
        "hook": ["Do you run more than one WhatsApp number for your business?", "And do your customers write in languages you don't speak?"],
        "pain": ["Switching between phones all day.", "Copying every message into a translator.", "Missing messages on the other number.", "It costs you time, and it costs you customers."],
        "brand": ["Meet GlotChat.", "All your WhatsApp accounts in one window on your PC, and every message in your own language."],
        "accounts": ["First, connect all your WhatsApp numbers.", "Give each account a name, choose your language, and scan the QR code, just like WhatsApp Web.",
                     "Every account is separate, with its own login.", ("We've tested twenty-seven accounts running at the same time.", "We've tested 27 accounts running at the same time.")],
        "notify": ["When a message arrives, the notification tells you which account it's for.", "And it's already translated.", "Click it, and the right chat opens."],
        "chat": ["Every customer message is translated right under the original.", "You reply in your own language.",
                 "GlotChat shows you the translation before it's sent,", "and your customer receives it in their language."],
        "langs": ["Each account has its own languages.", "Your shop in Dubai speaks Arabic, your European sales line speaks Spanish, and your export account speaks Chinese.",
                  "GlotChat even detects each customer's language automatically."],
        "voice": ["Customers love voice notes.", "One click turns a voice message into text, and translates it for you."],
        "photo": ["A photo of an invoice or an order?", "GlotChat reads the text in the picture, and translates it too."],
        "stats": [("Everything is translated offline, on your own computer, in forty-nine languages.", "Everything is translated offline, on your own computer, in 49 languages."),
                  "Your chats are never sent to an online translator."],
        "end": [("Try GlotChat free for three days. No payment needed.", "Try GlotChat free for 3 days. No payment needed."),
                "Contact us now, and start today."],
    },
    "zh": {
        "hook": ["你的生意是不是用好几个 WhatsApp 号码？", "客户说的语言，你又看不懂？"],
        "pain": ["整天在几部手机之间来回切换。", "每条消息都要复制到翻译软件。", "另一个号码的消息又漏看了。", "浪费时间，更流失客户。"],
        "brand": ["试试 GlotChat。", "所有 WhatsApp 账号都在电脑上的一个窗口里，每条消息都翻译成中文。"],
        "accounts": ["首先，连接你所有的 WhatsApp 号码。", "给每个账号起个名字，选好语言，像 WhatsApp 网页版一样扫码即可。",
                     "每个账号相互独立，各自登录。", ("我们测试过二十七个账号同时运行。", "我们测试过 27 个账号同时运行。")],
        "notify": ["新消息到达时，通知会告诉你来自哪个账号。", "而且已经翻译好了。", "点一下，就会打开对应的聊天。"],
        "chat": ["每条客户消息都会翻译在原文下方。", "你用中文回复。", "发送前，GlotChat 会先让你看到译文，", "客户收到的是他们自己的语言。"],
        "langs": ["每个账号都有自己的语言设置。", "迪拜店铺说阿拉伯语，欧洲销售线说西班牙语，出口账号说英语。", "GlotChat 还能自动识别每位客户的语言。"],
        "voice": ["客户喜欢发语音？", "点一下，语音就变成文字，并翻译成中文。"],
        "photo": ["发票或订单的照片？", "GlotChat 能识别图片里的文字，并一起翻译。"],
        "stats": [("所有翻译都在你自己的电脑上离线完成，支持四十九种语言。", "所有翻译都在你自己的电脑上离线完成，支持 49 种语言。"), "你的聊天内容不会被发送到任何在线翻译。"],
        "end": [("免费试用 GlotChat 三天，无需付款。", "免费试用 GlotChat 3 天，无需付款。"), "现在就联系我们，今天就开始吧。"],
    },
}
TEXT = {
    "en": {"hook1": "Too many WhatsApp numbers?", "hook2": "Customers writing in languages you don't speak?",
           "painTitle": "Sound familiar?", "pain": ["📱 Switching phones all day", "📋 Copy → translate → paste", "🔕 Missed messages", "💸 Lost customers"],
           "brand": 'All your WhatsApp accounts in <span class="grad">one window</span>. Every message in <span class="grad">your language</span>.',
           "heads": {"accounts": "Connect all your WhatsApp accounts", "notify": "Each account, its own notifications", "chat": "Translate every chat — both ways",
                     "langs": "Each account speaks its customers' language", "voice": "Voice notes → text", "photo": "Photos & invoices → translated",
                     "stats": "Private · offline · 49 languages"},
           "langCards": [{"name": "Shop UAE", "color": "#f59e0b", "pair": "English ⇄ Arabic", "orig": "مرحبا، هل الطلب جاهز؟", "code": "AR→EN", "tr": "Hello, is the order ready?"},
                         {"name": "Sales EU", "color": "#10b981", "pair": "English ⇄ Spanish", "orig": "¿Cuánto cuesta el envío?", "code": "ES→EN", "tr": "How much is shipping?"},
                         {"name": "Export", "color": "#ef4444", "pair": "English ⇄ Chinese", "orig": "好的，明天发货", "code": "ZH→EN", "tr": "OK, it ships tomorrow"}],
           "stats": [["49", "languages"], ["100%", "offline on your PC"], ["~100", "voice languages"], ["27+", "accounts tested at once"]],
           "end": "Try it FREE for 3 days", "pts": ["No payment to start", "Windows 10 & 11"],
           "cta": "Contact us now", "legal": "GlotChat is not affiliated with WhatsApp or Meta."},
    "zh": {"hook1": "WhatsApp 号码太多，管不过来？", "hook2": "客户说的语言你看不懂？",
           "painTitle": "是不是很熟悉？", "pain": ["📱 整天切换手机", "📋 复制 → 翻译 → 粘贴", "🔕 漏看消息", "💸 流失客户"],
           "brand": '所有 WhatsApp 账号，<span class="grad">一个窗口</span>。每条消息，都是<span class="grad">你的语言</span>。',
           "heads": {"accounts": "连接所有 WhatsApp 账号", "notify": "每个账号，独立通知", "chat": "每个聊天，双向翻译",
                     "langs": "每个账号，说客户的语言", "voice": "语音 → 文字", "photo": "图片和发票 → 翻译", "stats": "私密 · 离线 · 49 种语言"},
           "langCards": [{"name": "Shop UAE", "color": "#f59e0b", "pair": "中文 ⇄ 阿拉伯语", "orig": "مرحبا، هل الطلب جاهز؟", "code": "AR→ZH", "tr": "你好，订单准备好了吗？"},
                         {"name": "Sales EU", "color": "#10b981", "pair": "中文 ⇄ 西班牙语", "orig": "¿Cuánto cuesta el envío?", "code": "ES→ZH", "tr": "运费是多少？"},
                         {"name": "Export", "color": "#ef4444", "pair": "中文 ⇄ 英语", "orig": "Can you send the invoice today?", "code": "EN→ZH", "tr": "今天能发发票吗？"}],
           "stats": [["49", "种翻译语言"], ["100%", "在你的电脑上离线"], ["约 100", "种语音语言"], ["27+", "个账号同时测试"]],
           "end": "免费试用 3 天", "pts": ["无需付款即可开始", "支持 Windows 10 和 11"],
           "cta": "立即联系我们", "legal": "GlotChat 与 WhatsApp 或 Meta 无关联。"},
}
# section order and look
SECTIONS = [
    {"id": "hook", "type": "hook", "min": 3.5},
    {"id": "pain", "type": "pain", "min": 4},
    {"id": "brand", "type": "brand", "min": 4},
    {"id": "accounts", "type": "demo", "scene": "accounts", "num": 1, "dot": 0},
    {"id": "notify", "type": "demo", "scene": "notify", "num": 2, "dot": 1},
    {"id": "chat", "type": "demo", "scene": "chat", "num": 3, "dot": 2},
    {"id": "langs", "type": "langs", "num": 3, "dot": 2, "min": 6},
    {"id": "voice", "type": "demo", "scene": "voice", "num": 4, "dot": 3},
    {"id": "photo", "type": "demo", "scene": "photo", "num": 5, "dot": 4},
    {"id": "stats", "type": "stats", "min": 5},
    {"id": "end", "type": "end", "min": 7, "post": 2.6},
]
PRE, GAP, POST = 0.45, 0.32, 0.55


# ------------------------------------------------------------------ voice
def tts(lang):
    """One wav per sentence; returns {section: [(path, seconds, spoken, shown)]}."""
    from kokoro_onnx import Kokoro
    os.makedirs(os.path.join(WORK, lang), exist_ok=True)
    if lang == "zh":
        from misaki import espeak, zh
        eng = espeak.EspeakG2P(language="en-us")                    # English words inside Chinese (WhatsApp, GlotChat)
        g2p = zh.ZHG2P(version="1.1", en_callable=lambda t: eng(t)[0])
        k = Kokoro(MODELS + r"\kokoro-v1.1-zh.onnx", MODELS + r"\voices-v1.1-zh.bin", vocab_config=MODELS + r"\config-v1.1-zh.json")
    else:
        k = Kokoro(MODELS + r"\kokoro-v1.0.onnx", MODELS + r"\voices-v1.0.bin")
    out = {}
    for sec, lines in SCRIPT[lang].items():
        out[sec] = []
        for i, line in enumerate(lines):
            say, show = (line if isinstance(line, tuple) else (line, line))
            if lang == "zh":
                ph, _ = g2p(say)
                audio, sr = k.create(ph, voice=VOICE[lang], speed=1.0, is_phonemes=True)
            else:
                audio, sr = k.create(say, voice=VOICE[lang], speed=1.0, lang="en-us")
            audio = trim(audio, sr)
            p = os.path.join(WORK, lang, f"{sec}-{i}.wav"); sf.write(p, audio, sr)
            out[sec].append((p, len(audio) / sr, say, show))
    return out, sr


def trim(a, sr, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    if not len(idx):
        return a
    s, e = max(0, idx[0] - int(0.03 * sr)), min(len(a), idx[-1] + int(0.08 * sr))
    return a[s:e]


# ------------------------------------------------------------------ music (generated here, so no licence questions)
def music(seconds, path, sr=44100):
    n = int(seconds * sr); t = np.arange(n) / sr
    left = np.zeros(n); right = np.zeros(n)
    hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    chords = [[48, 52, 55, 59, 62], [45, 48, 52, 55, 59], [41, 45, 48, 52, 55], [43, 47, 50, 52, 57]]   # Cmaj9 Am9 Fmaj9 G6/9
    span = 4.0                                                                                       # seconds per chord
    for ci in range(int(seconds / span) + 2):
        ch = chords[ci % 4]; t0 = ci * span - 0.8
        a, b = max(0, int(t0 * sr)), min(n, int((t0 + span + 1.6) * sr))
        if a >= b:
            continue
        tt = t[a:b] - t0; env = np.clip(tt / 1.0, 0, 1) * np.clip((span + 1.6 - tt) / 1.0, 0, 1)
        env = np.sin(env * np.pi / 2) ** 2
        for j, m in enumerate(ch):                      # warm pad: two detuned sines + soft octave
            f = hz(m)
            v = (np.sin(2 * np.pi * f * 0.998 * tt) + np.sin(2 * np.pi * f * 1.002 * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * env * 0.05
            left[a:b] += v * (0.6 if j % 2 else 0.4); right[a:b] += v * (0.4 if j % 2 else 0.6)
        f = hz(ch[0] - 12)                              # soft bass on the root
        bass = np.sin(2 * np.pi * f * tt) * env * 0.09
        left[a:b] += bass; right[a:b] += bass
    step = 60 / 96 / 2                                  # gentle plucked arpeggio, eighth notes at 96 bpm
    for k in range(int(seconds / step)):
        t0 = k * step; ch = chords[int(t0 / span) % 4]
        m = ch[[0, 2, 4, 3, 1, 3, 2, 4][k % 8]] + 12
        a, b = int(t0 * sr), min(n, int((t0 + 1.2) * sr)); tt = t[a:b] - t0; f = hz(m)
        v = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 5.5) + 0.3 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 9)) * 0.045 * (0.8 + 0.2 * (k % 2))
        pan = 0.5 + 0.35 * np.sin(k * 0.9)
        left[a:b] += v * (1 - pan); right[a:b] += v * pan
    st = np.stack([left, right], 1)
    fade = np.ones(n); fi, fo = int(2 * sr), int(3.5 * sr)
    fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
    st *= fade[:, None]; st /= max(1e-9, np.abs(st).max()) / 0.5
    sf.write(path, st.astype(np.float32), sr)


# ------------------------------------------------------------------ build
def server(port):
    p = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1); return p


def scene_lengths(pg, port, lang):
    out = {}
    for s in SECTIONS:
        if s.get("scene"):
            pg.goto(f"http://127.0.0.1:{port}/_tools/demo/demo.html?scene={s['scene']}&lang={lang}&fmt=port&record=1")
            out[s["scene"]] = pg.evaluate("window.DURATION") + 0.6
    return out


def timeline(lang, voice, lens):
    t, secs, voice_track = 0.0, [], []
    for s in SECTIONS:
        lines = voice[s["id"]]
        speech = sum(d for _, d, _, _ in lines) + GAP * (len(lines) - 1)
        minimum = s.get("min", 0)
        if s.get("scene"):
            minimum = max(minimum, lens[s["scene"]] * 0.8)
        dur = max(minimum, PRE + speech + s.get("post", POST))
        caps, c = [], t + PRE
        for p, d, say, show in lines:
            caps.append({"t0": round(c, 3), "t1": round(c + d, 3), "show": show}); voice_track.append((c, p)); c += d + GAP
        sec = {"id": s["id"], "type": s["type"], "start": round(t, 3), "dur": round(dur, 3), "caps": caps,
               "showCaps": s["type"] in ("demo", "langs", "stats"), "chrome": s["type"] in ("demo", "langs", "stats")}
        if s.get("scene"):
            sec.update(scene=s["scene"], sceneLen=lens[s["scene"]])
        if s["id"] in TEXT[lang]["heads"]:
            sec["head"] = TEXT[lang]["heads"][s["id"]]
        for k in ("num", "dot"):
            if k in s:
                sec[k] = s[k]
        secs.append(sec); t += dur
    return {"lang": lang, "duration": round(t, 3), "sections": secs, "text": TEXT[lang]}, voice_track


def mix(lang, data, voice_track, sr):
    total = data["duration"] + 0.5
    v = np.zeros(int(total * sr), dtype=np.float32)
    for t0, p in voice_track:
        a, _ = sf.read(p, dtype="float32"); i = int(t0 * sr); v[i:i + len(a)] += a[: len(v) - i]
    vp = os.path.join(WORK, f"voice-{lang}.wav"); sf.write(vp, v, sr)
    mp = os.path.join(WORK, f"music-{lang}.wav"); music(total, mp)
    final = os.path.join(WORK, f"mix-{lang}.wav")
    # music ducks under the voice, then the whole mix is set to -14 LUFS (the usual level for social video)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vp, "-i", mp, "-filter_complex",
                    "[0:a]aresample=44100,aformat=channel_layouts=stereo,volume=1.0,asplit=2[v1][v2];"
                    "[1:a]volume=0.32,aecho=0.8:0.6:70|140:0.25|0.15[m];"
                    "[m][v1]sidechaincompress=threshold=0.015:ratio=5:attack=40:release=500[md];"
                    "[md][v2]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
                    "-map", "[a]", "-ar", "48000", final], check=True)
    shutil.copy(vp, os.path.join(OUT, f"glotchat-explainer-{lang}-voiceover.wav"))
    return final


def render(lang, fmt, port, audio, preview=False):
    from playwright.sync_api import sync_playwright
    name = f"glotchat-explainer-{lang}-{fmt}"
    h = 960 if fmt == "story" else 675
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 540, "height": h}, device_scale_factor=2)
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"http://127.0.0.1:{port}/_tools/ad/explainer.html?lang={lang}&fmt={fmt}&record=1")
        pg.wait_for_function("window.READY === true", timeout=60000); pg.wait_for_timeout(300)
        data = json.load(open(os.path.join(HERE, f"explainer-{lang}.json"), encoding="utf-8"))
        if preview:
            d = os.path.join(WORK, "preview"); os.makedirs(d, exist_ok=True)
            for s in data["sections"]:
                for f in (0.35, 0.8):
                    t = s["start"] + s["dur"] * f
                    pg.evaluate(f"seekAd({t})"); pg.screenshot(path=os.path.join(d, f"{name}-{t:06.2f}-{s['id']}.png"))
            print(name, "preview", errs or ""); b.close(); return
        tmp = os.path.join(WORK, "frames", name); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        n = int(data["duration"] * FPS)
        for i in range(n):
            pg.evaluate(f"seekAd({i / FPS})"); pg.screenshot(path=os.path.join(tmp, f"{i:05d}.png"))
        brand = next(s for s in data["sections"] if s["id"] == "brand")
        shutil.copy(os.path.join(tmp, f"{int((brand['start'] + brand['dur'] * 0.85) * FPS):05d}.png"), os.path.join(OUT, name + "-cover.png"))
        b.close()
    mp4 = os.path.join(OUT, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.png"), "-i", audio,
                    "-c:v", "libx264", "-preset", "medium", "-threads", "4", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", mp4 + ".tmp.mp4"], check=True)
    try:
        os.replace(mp4 + ".tmp.mp4", mp4)
    except PermissionError:                      # the old video is open in a player: keep both
        mp4 = mp4[:-4] + "-new.mp4"; os.replace(mp4.replace("-new.mp4", ".mp4") + ".tmp.mp4", mp4)
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
    port = 8800 + (os.getpid() % 90)
    srv = server(port)
    try:
        for lang in langs:
            jpath = os.path.join(HERE, f"explainer-{lang}.json")
            mixed = os.path.join(WORK, f"mix-{lang}.wav")
            if not (skip_voice and os.path.exists(jpath) and os.path.exists(mixed)):
                voice, sr = tts(lang)
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    b = p.chromium.launch(channel="chrome"); pg = b.new_page()
                    lens = scene_lengths(pg, port, lang); b.close()
                data, track = timeline(lang, voice, lens)
                json.dump(data, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                mixed = mix(lang, data, track, sr)
                with open(os.path.join(OUT, f"glotchat-explainer-{lang}-script.txt"), "w", encoding="utf-8") as f:
                    for s in data["sections"]:
                        for c in s["caps"]:
                            m, sec = divmod(c["t0"], 60)
                            f.write(f"[{int(m)}:{sec:05.2f}] {c['show']}\n")
                print(f"{lang}: timeline {data['duration']:.1f}s", flush=True)
            for fmt in fmts:
                render(lang, fmt, port, mixed, preview)
    finally:
        srv.terminate()


if __name__ == "__main__":
    main()

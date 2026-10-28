"""GlotChat ad #3 (30 s): many WhatsApp accounts in one window + translation. Violet style, voice-over, music, sound effects.

    python _tools/ad/multi_build.py en zh            voice + timeline + video, both formats
    python _tools/ad/multi_build.py en --preview     voice + timeline + still frames only

Uses the engine of promo_build.py (voice, music, mix, render). Template: _tools/ad/multi.html
Output: D:/glotchat-marketing/ads-multi/glotchat-multi-<lang>-<feed|story>.mp4 (+ cover, voice-over, script)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import promo_build as pb  # noqa: E402

pb.OUT = r"D:\glotchat-marketing\ads-multi"
pb.WORK = os.path.join(pb.OUT, "_work")
pb.PAGE = "multi"
pb.PREFIX = "glotchat-multi"
pb.DRUMS_AT = 4.6
pb.CAPS = {"add", "notify", "proof"}

pb.SECTIONS = [
    {"id": "hook", "dur": 4.6, "ev": {"ph": [0.15, 0.35, 0.55, 0.75, 0.95], "sub": 2.35}},
    {"id": "brand", "dur": 3.6, "ev": {}},
    {"id": "add", "dur": 6.2, "ev": {"modal": 0.25, "type": 0.55, "typeEnd": 1.35, "lang": 1.6, "press": 2.2, "qr": 2.45, "ok": 3.6, "close": 4.0,
                                     "tab6": 4.2, "more": [4.55, 4.75, 4.95, 5.15, 5.35, 5.55]}},
    {"id": "notify", "dur": 7.0, "ev": {"toasts": [0.3, 0.8, 1.3], "click": 2.4, "in1": 2.75, "tr1": 3.2, "type": 3.7, "out": 5.0, "in2": 5.95, "tr2": 6.35}},
    {"id": "proof", "dur": 4.2, "ev": {}},
    {"id": "end", "dur": 4.4, "ev": {}},
]

pb.SCRIPT = {
    "en": {
        "hook": [{"t": "Still juggling five phones?", "at": 0.25}, {"t": "Every missed message is a lost sale.", "at": 2.4}],
        "brand": [{"t": "GlotChat puts all your WhatsApp numbers in one window.", "at": 0.35}],
        "add": [{"t": "Add a number in seconds.", "at": 0.3}, {"t": "Name it, choose the language, scan the QR code.", "at": 1.55},
                {"t": "Add as many as you need.", "at": 4.35}],
        "notify": [{"t": "Messages from every account land in one place, already translated.", "at": 0.2},
                   {"t": "Reply in English. Your customer reads Hindi.", "at": 4.0}],
        "proof": [{"t": "Built for exporters, online shops, real estate, travel and clinics.", "at": 0.2}],
        "end": [{"t": ("Try it free for three days.", "Try it free for 3 days."), "at": 0.3}, {"t": "Contact us now!"}],
    },
    "zh": {
        "hook": [{"t": "还在用五部手机？", "at": 0.25}, {"t": "漏一条消息，丢一单生意。", "at": 2.3}],
        "brand": [{"t": "GlotChat 把所有 WhatsApp 号码放进一个窗口。", "at": 0.35}],
        "add": [{"t": "几秒添加号码。", "at": 0.3}, {"t": "起名，选语言，扫码。", "at": 1.7}, {"t": "想加多少就加多少。", "at": 4.35}],
        "notify": [{"t": "所有账号的消息汇集一处，而且已经翻译好。", "at": 0.2}, {"t": "你用中文回复，客户读到的是印地语。", "at": 4.0}],
        "proof": [{"t": "外贸、网店、房产、旅游、诊所，都适用。", "at": 0.2}],
        "end": [{"t": ("免费试用三天。", "免费试用 3 天。"), "at": 0.3}, {"t": "马上联系我们！"}],
    },
}

COLORS = ["#0ea5e9", "#10b981", "#ef4444", "#6366f1", "#f59e0b", "#f97316", "#14b8a6", "#ec4899", "#8b5cf6", "#84cc16", "#06b6d4", "#a855f7"]
NAMES = {
    "en": ["Sales US", "Shop EU", "Export", "Support", "Store", "India Sales", "Wholesale", "VIP", "Shop TR", "Sales MX", "Store 2", "Support 2"],
    "zh": ["美国销售", "欧洲店铺", "出口", "客服", "门店", "印度销售", "批发", "VIP", "土耳其店", "墨西哥销售", "门店 2", "客服 2"],
}
HINDI_IN = "नमस्ते, क्या आज डिलीवरी हो सकती है?"
HINDI_OUT = "हाँ! आज शाम तक पहुँच जाएगा 🚚"
HINDI_IN2 = "बहुत बढ़िया, धन्यवाद! 🙏"


def phones(lang):
    third = ({"who": "Wei", "m": "你好，可以发样品吗？"} if lang == "en" else {"who": "John", "m": "Hi, can you send a sample?"})
    return [
        {"who": "Mike", "m": "Is this still available?", "who2": "Anna", "m2": "Can you ship 50 pcs?", "n": 3},
        {"who": "Lucía", "m": "¿Hacen envíos a España?", "who2": "Marco", "m2": "Ciao! È disponibile?", "n": 7},
        {**third, "who2": "Ali", "m2": "Merhaba, katalog var mı?", "n": 2},
        {"who": "Priya", "m": "नमस्ते, मेरा ऑर्डर कहाँ है?", "who2": "Jan", "m2": "Hallo, Rechnung bitte", "n": 5},
        {"who": "Olga", "m": "Привет! Есть доставка?", "who2": "Ana", "m2": "Olá, tem em azul?", "n": 4},
    ]


pb.TEXT = {
    "en": {
        "accounts": [[n, COLORS[i], n[0]] for i, n in enumerate(NAMES["en"])],
        "hook": {"title": 'Still juggling <span class="hl">5 phones</span>?', "sub": "Every missed message = a lost sale 💸", "phones": phones("en")},
        "brand": {"title": 'All your WhatsApp numbers<br><span class="hl">in one window</span>'},
        "list": [["Lucía", "Do you ship to Spain?", "#10b981"], ["Marco", "Hi! Is it available?", "#8b5cf6"], ["Sofía", "Thanks, I'll order today 🙏", "#f59e0b"],
                 ["Jan", "Can you send the invoice?", "#0ea5e9"], ["Nadia", "Perfect, see you tomorrow", "#ec4899"], ["Pierre", "Do you have it in black?", "#14b8a6"]],
        "add": {"title": 'Add an account in <span class="hl">seconds</span>', "h": "Add account", "nameL": "Account name", "nameV": "India Sales",
                "langL": "Translate between", "pairA": "English", "pairB": "हिन्दी", "next": "Scan QR code", "connected": "Connected",
                "hint": "Scan with WhatsApp on your phone", "count": "{n} accounts ✓"},
        "toasts": [{"acc": "India Sales", "tab": 5, "c": COLORS[5], "who": "Priya", "o": HINDI_IN, "code": "HI→EN", "tr": "Hi, can it be delivered today?"},
                   {"acc": "Shop EU", "tab": 1, "c": COLORS[1], "who": "Lucía", "o": "¿Lo tienen en talla M?", "code": "ES→EN", "tr": "Do you have it in size M?"},
                   {"acc": "Export", "tab": 2, "c": COLORS[2], "who": "Wei", "o": "你好，可以发产品目录吗？", "code": "ZH→EN", "tr": "Hi, can you send the catalog?"}],
        "notify": {"title": 'Every account. <span class="hl">Every language.</span>'},
        "chat": {"who": "Priya", "acc": "India Sales", "status": "online", "pair": "English ⇄ हिन्दी", "in1": HINDI_IN, "code1": "HI→EN",
                 "tr1": "Hi, can it be delivered today?", "reply": "Yes! It will arrive this evening 🚚", "out": HINDI_OUT, "code2": "EN→HI",
                 "in2": HINDI_IN2, "tr2": "Great, thank you! 🙏", "placeholder": "Type in English…", "sent": "Sent in Hindi"},
        "proof": {"title": 'Made for businesses that <span class="hl">sell worldwide</span>',
                  "items": [["🏭", "Exporters"], ["🛍️", "Online shops"], ["🏠", "Real estate"], ["✈️", "Travel agencies"], ["🦷", "Clinics"], ["🚗", "Car dealers"]],
                  "checks": ["Each account keeps its own login", "Notifications show which account", "49 languages · offline · private"]},
        "end": {"h": "Try it FREE for 3 days", "pts": ["No payment to start", "Ready in minutes · Windows 10 & 11"], "cta": "Contact us now",
                "legal": "GlotChat is not affiliated with WhatsApp or Meta."},
    },
    "zh": {
        "accounts": [[n, COLORS[i], n[0]] for i, n in enumerate(NAMES["zh"])],
        "hook": {"title": '还在同时用 <span class="hl">5 部手机</span>？', "sub": "漏一条消息 = 丢一单生意 💸", "phones": phones("zh")},
        "brand": {"title": '所有 WhatsApp 号码<br><span class="hl">一个窗口搞定</span>'},
        "list": [["Lucía", "可以发货到西班牙吗？", "#10b981"], ["Marco", "你好！有现货吗？", "#8b5cf6"], ["Sofía", "谢谢，我今天就下单 🙏", "#f59e0b"],
                 ["Jan", "能发一下发票吗？", "#0ea5e9"], ["Nadia", "好的，明天见", "#ec4899"], ["Pierre", "有黑色的吗？", "#14b8a6"]],
        "add": {"title": '<span class="hl">几秒钟</span>添加一个账号', "h": "添加账号", "nameL": "账号名称", "nameV": "印度销售",
                "langL": "翻译语言", "pairA": "中文", "pairB": "हिन्दी", "next": "扫码登录", "connected": "已连接",
                "hint": "用手机上的 WhatsApp 扫码", "count": "{n} 个账号 ✓"},
        "toasts": [{"acc": "印度销售", "tab": 5, "c": COLORS[5], "who": "Priya", "o": HINDI_IN, "code": "HI→ZH", "tr": "你好，今天能送到吗？"},
                   {"acc": "欧洲店铺", "tab": 1, "c": COLORS[1], "who": "Lucía", "o": "¿Lo tienen en talla M?", "code": "ES→ZH", "tr": "有 M 码吗？"},
                   {"acc": "出口", "tab": 2, "c": COLORS[2], "who": "John", "o": "Hi, can you send the catalog?", "code": "EN→ZH", "tr": "你好，能发一下产品目录吗？"}],
        "notify": {"title": '每个账号，<span class="hl">每种语言</span>'},
        "chat": {"who": "Priya", "acc": "印度销售", "status": "在线", "pair": "中文 ⇄ हिन्दी", "in1": HINDI_IN, "code1": "HI→ZH",
                 "tr1": "你好，今天能送到吗？", "reply": "可以！今晚就能送到 🚚", "out": HINDI_OUT, "code2": "ZH→HI",
                 "in2": HINDI_IN2, "tr2": "太好了，谢谢！🙏", "placeholder": "用中文输入…", "sent": "已用印地语发送"},
        "proof": {"title": '专为<span class="hl">做海外生意</span>的你打造',
                  "items": [["🏭", "外贸工厂"], ["🛍️", "网店卖家"], ["🏠", "房产中介"], ["✈️", "旅行社"], ["🦷", "诊所"], ["🚗", "汽车经销"]],
                  "checks": ["每个账号独立登录", "通知显示来自哪个账号", "49 种语言 · 离线 · 私密"]},
        "end": {"h": "免费试用 3 天", "pts": ["无需付款即可开始", "几分钟即可上手 · 支持 Windows 10 和 11"], "cta": "立即联系我们",
                "legal": "GlotChat 与 WhatsApp 或 Meta 无关联。"},
    },
}


def multi_sfx(data):
    s = {x["id"]: x for x in data["sections"]}; ev = []
    ev += [("pop", s["hook"]["start"] + b) for b in s["hook"]["ev"]["ph"]]
    ev += [("woosh", s["brand"]["start"] + 0.1), ("chime", s["brand"]["start"] + 0.55)]
    a = s["add"]; e = a["ev"]
    ev += [("tick", a["start"] + e["press"]), ("chime", a["start"] + e["ok"]), ("pop", a["start"] + e["tab6"])]
    ev += [("tick", a["start"] + m) for m in e["more"]]
    n = s["notify"]; e = n["ev"]
    ev += [("pop", n["start"] + x) for x in e["toasts"]] + [("tick", n["start"] + e["click"]), ("woosh", n["start"] + e["out"] - 0.1), ("pop", n["start"] + e["in2"])]
    ev += [("tick", s["proof"]["start"] + 0.3 + i * 0.2) for i in range(6)]
    ev += [("chime", s["end"]["start"] + 0.1)]
    return ev


pb.SFX_EVENTS = multi_sfx

if __name__ == "__main__":
    pb.main()

"""Site-wide settings for the GlotChat website. Edit here, then run:  python src/build.py"""

SITE = "https://www.glotchat.com"
BRAND = "GlotChat"

# ---------------------------------------------------------------- contact
# Telegram is the main channel. The others are optional: fill one in and its button
# appears everywhere automatically (leave "" to hide it).
TELEGRAM_USER = "GlotChat"
WHATSAPP_NUMBER = ""      # international format without + or spaces, e.g. "971501234567"
WECHAT_ID = ""            # shown on the Chinese pages (Telegram is blocked in mainland China)
EMAIL = ""                # e.g. "hello@glotchat.com"

# ---------------------------------------------------------------- search engine ownership checks
# Paste the code each webmaster tool gives you (only the content="..." part), then rebuild.
BAIDU_SITE_VERIFICATION = ""   # ziyuan.baidu.com → 用户中心 → 站点管理 → 添加网站 → HTML 标签验证
BING_SITE_VERIFICATION = ""    # bing.com/webmasters (Bing also powers cn.bing.com, used by many sellers in China)

# ---------------------------------------------------------------- plans (USDT per year)
# The USDT price is also published as USD in the structured data (USDT is pegged to the dollar).
PLANS = [
    {"id": "Starter", "price": 69, "accounts": 5, "pcs": 1},
    {"id": "Pro", "price": 129, "accounts": 15, "pcs": 1, "popular": True},
    {"id": "Business", "price": 249, "accounts": None, "pcs": 3},   # None = unlimited
]
TRIAL_DAYS = 3

# ---------------------------------------------------------------- download (Cloudflare R2 bucket glotchat-download)
# The installer stays on a version Windows Smart App Control already trusts (a new unsigned installer is
# blocked until Microsoft learns it); newer versions reach customers as automatic updates a minute after start.
# Upload each new installer under a VERSIONED name (Cloudflare caches .exe files at its edge, so a reused
# name keeps serving the old file), then update url/file/version/size/sha256 here and rebuild.
# Also upload it as GlotChat-Setup.exe for links shared earlier, and purge that URL in Cloudflare.
DOWNLOAD = {
    "url": "https://download.glotchat.com/GlotChat-Setup-1.2.5.exe",
    "file": "GlotChat-Setup-1.2.5.exe",
    "version": "1.2.5",
    "date": "2026-10-22",
    "size_mb": 381,          # as Windows shows it (399,644,511 bytes)
    "sha256": "56800eb5894ca7f1336cae5c616a1d8ded4b3e90219862014c21f0959c113c5a",
}
PAY_NETWORKS = "TRC20 · BEP20 · ERC20"

# ---------------------------------------------------------------- product facts (keep them true)
FACTS = {
    "accounts_tested": 27,      # accounts tested running at the same time
    "languages": 49,            # translation languages (offline packs)
    "voice_languages": 100,     # spoken languages recognised in voice notes (about)
    "os": "Windows 10, Windows 11",
    "ram_per_account": "300–450 MB",
}

# The 49 translation languages, as the app lists them (desktop/translator.py NAMES)
TRANSLATION_LANGUAGES = [
    "English", "العربية", "Français", "Español", "Deutsch", "Italiano", "Português", "Português (Brasil)",
    "Русский", "Türkçe", "Nederlands", "Polski", "हिन्दी", "中文 (简体)", "中文 (繁體)", "日本語", "한국어",
    "فارسی", "اردو", "עברית", "Bahasa Indonesia", "Bahasa Melayu", "ไทย", "Tiếng Việt", "Українська",
    "Ελληνικά", "Svenska", "Dansk", "Norsk", "Suomi", "Čeština", "Slovenčina", "Magyar", "Română",
    "Български", "বাংলা", "Català", "Esperanto", "Eesti", "Gaeilge", "Galego", "Lietuvių", "Latviešu",
    "Slovenščina", "Shqip", "Azərbaycan", "Euskara", "Tagalog", "Кыргызча",
]

# ---------------------------------------------------------------- languages of the website
# code -> settings. English lives at "/", the others at "/<code>/".
LANGS = {
    "en": {"name": "English", "hreflang": "en", "html": "en", "og": "en_US", "dir": "ltr"},
    "zh": {"name": "简体中文", "short": "简体", "hreflang": "zh-Hans", "html": "zh-Hans", "og": "zh_CN", "dir": "ltr"},
    # Traditional Chinese (Taiwan / Hong Kong): generated from zh.yaml by src/make_zh_hant.py; uses the zh demo videos
    "zh-hant": {"name": "繁體中文", "short": "繁體", "hreflang": "zh-Hant", "html": "zh-Hant", "og": "zh_TW", "dir": "ltr", "media": "zh"},
    "ar": {"name": "العربية", "hreflang": "ar", "html": "ar", "og": "ar_AR", "dir": "rtl"},
    "tr": {"name": "Türkçe", "hreflang": "tr", "html": "tr", "og": "tr_TR", "dir": "ltr"},
    "es": {"name": "Español", "hreflang": "es", "html": "es", "og": "es_ES", "dir": "ltr"},
    "pt": {"name": "Português", "hreflang": "pt", "html": "pt", "og": "pt_BR", "dir": "ltr"},
    "ru": {"name": "Русский", "hreflang": "ru", "html": "ru", "og": "ru_RU", "dir": "ltr"},
}
DEFAULT_LANG = "en"

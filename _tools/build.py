"""SEO build for the GlotChat landing page.

    python _tools/build.py

- fills every absolute URL (canonical, hreflang, Open Graph, Twitter) from SITE
- writes the structured data (Organization, WebSite, SoftwareApplication, FAQPage) into index.html
- renders /zh/index.html: the same page with the Chinese text in the HTML itself (search engines
  index it without running JavaScript), Chinese title / description / FAQ structured data
- writes sitemap.xml (with language alternates) and robots.txt

Change the domain: edit SITE below and run the script again.
"""
import datetime, json, os, re, subprocess, sys, time
from playwright.sync_api import sync_playwright

SITE = "https://www.glotchat.com"
TELEGRAM = "https://t.me/Capooo007"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8766

ZH_META = {
    "title": "GlotChat – WhatsApp 多开 + 聊天翻译电脑版",
    "description": "在电脑上一个窗口同时运行多个 WhatsApp 账号，离线翻译聊天、语音和图片，支持 49 种语言，每个账号通知独立。免费试用 3 天。",
    "og_title": "GlotChat – 所有 WhatsApp 账号一个窗口，每位客户都用他的语言沟通",
    "og_description": "多个 WhatsApp 账号同屏运行，文字、语音和图片在电脑上离线翻译。免费试用 3 天。",
}
APP_DESC = {
    "en": "Run multiple WhatsApp accounts in one window on Windows, each isolated with its own notifications, "
          "with offline translation of messages, voice notes and photos in 49 languages.",
    "zh": "在 Windows 电脑上一个窗口运行多个 WhatsApp 账号，每个账号相互隔离、通知独立，并可离线翻译文字、语音和图片，支持 49 种语言。",
}


def jsonld(lang, faq, url):
    graph = [
        {"@type": "Organization", "@id": SITE + "/#org", "name": "GlotChat", "url": SITE + "/",
         "logo": SITE + "/assets/img/icon-512.png", "sameAs": [TELEGRAM],
         "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "url": TELEGRAM, "availableLanguage": ["English", "Chinese"]}},
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "GlotChat",
         "inLanguage": ["en", "zh-Hans"], "publisher": {"@id": SITE + "/#org"}},
        {"@type": "SoftwareApplication", "@id": SITE + "/#app", "name": "GlotChat", "url": url,
         "operatingSystem": "Windows 10, Windows 11", "applicationCategory": "BusinessApplication",
         "description": APP_DESC[lang], "image": SITE + "/og.png", "inLanguage": lang if lang == "en" else "zh-Hans",
         "publisher": {"@id": SITE + "/#org"}},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": lang if lang == "en" else "zh-Hans",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    body = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return '<!--jsonld--><script type="application/ld+json">' + body + "</script><!--/jsonld-->"


def set_site(html, lang_path):
    """Absolute URLs from SITE in the SEO tags (works whatever domain was there before)."""
    def fix(m):
        return m.group(1) + SITE + m.group(3)
    pat = r'((?:rel="canonical"|hreflang="[^"]+"|property="og:url"|property="og:image"|name="twitter:image")\s+(?:href|content)=")(https?://[^/"]+)(/[^"]*")'
    html = re.sub(pat, fix, html)
    # canonical / og:url point to this page
    html = re.sub(r'(<link rel="canonical" href=")[^"]*(")', r"\g<1>" + SITE + lang_path + r"\g<2>", html)
    html = re.sub(r'(<meta property="og:url" content=")[^"]*(")', r"\g<1>" + SITE + lang_path + r"\g<2>", html)
    return html


def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            pg = b.new_page()
            faq_js = "[...document.querySelectorAll('#faq details')].map(d => [d.querySelector('summary').textContent.trim(), d.querySelector('p').textContent.trim()])"
            pg.goto(f"http://127.0.0.1:{PORT}/index.html?lang=en&prerender=1", wait_until="networkidle")
            faq_en = pg.evaluate(faq_js)
            pg.goto(f"http://127.0.0.1:{PORT}/index.html?lang=zh&prerender=1", wait_until="networkidle")
            faq_zh = pg.evaluate(faq_js)
            # Chinese head
            pg.evaluate("""(m) => {
                const set = (sel, attr, v) => { const e = document.querySelector(sel); if (e) e.setAttribute(attr, v); };
                document.title = m.title;
                set('meta[name="description"]', 'content', m.description);
                set('meta[property="og:locale"]', 'content', 'zh_CN');
                set('meta[property="og:locale:alternate"]', 'content', 'en_US');
                set('meta[property="og:title"]', 'content', m.og_title);
                set('meta[property="og:description"]', 'content', m.og_description);
                set('meta[name="twitter:title"]', 'content', m.title);
                set('meta[name="twitter:description"]', 'content', m.og_description);
                set('meta[property="og:image:alt"]', 'content', 'GlotChat – WhatsApp 多开 + 翻译');
                set('link[rel="preload"][as="image"]', 'href', '/assets/media/chat-zh.webp');
                document.documentElement.setAttribute('lang', 'zh-Hans');
            }""", ZH_META)
            zh_html = "<!doctype html>\n" + pg.evaluate("document.documentElement.outerHTML") + "\n"
            b.close()
    finally:
        srv.terminate()

    # English page (in place, idempotent)
    p_en = os.path.join(ROOT, "index.html")
    en = open(p_en, encoding="utf-8").read()
    en = set_site(en, "/")
    en = re.sub(r"<!--jsonld-->.*?<!--/jsonld-->", lambda m: jsonld("en", faq_en, SITE + "/"), en, flags=re.S)
    open(p_en, "w", encoding="utf-8").write(en)

    # Chinese page
    zh_html = set_site(zh_html, "/zh/")
    zh_html = re.sub(r"<!--jsonld-->.*?<!--/jsonld-->", lambda m: jsonld("zh", faq_zh, SITE + "/zh/"), zh_html, flags=re.S)
    os.makedirs(os.path.join(ROOT, "zh"), exist_ok=True)
    open(os.path.join(ROOT, "zh", "index.html"), "w", encoding="utf-8").write(zh_html)

    # sitemap + robots
    today = datetime.date.today().isoformat()
    alts = (f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="zh-Hans" href="{SITE}/zh/"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>\n')
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          f"  <url>\n    <loc>{SITE}/</loc>\n    <lastmod>{today}</lastmod>\n{alts}  </url>\n"
          f"  <url>\n    <loc>{SITE}/zh/</loc>\n    <lastmod>{today}</lastmod>\n{alts}  </url>\n</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"built for {SITE}: index.html (EN, {len(faq_en)} FAQ), zh/index.html (中文, {len(faq_zh)} FAQ), sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()

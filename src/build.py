"""GlotChat website generator.

    python src/build.py            build every page in every language
    python src/build.py --no-og    skip the social preview images (faster while editing)

Text lives in src/content/<lang>.yaml (English first: en.yaml is the reference every other
language is checked against). Layout lives in src/templates/. Site settings in src/config.py.
The output is plain static HTML in the repository root, which Vercel serves as-is.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html as _html
import json
import os
import re
import shutil
import subprocess
import sys

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, pass_context  # noqa: F401
from markupsafe import Markup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import config as cfg  # noqa: E402

MANIFEST = os.path.join(ROOT, ".generated.json")
MEDIA_V = ""                 # set by build(): changes when any demo clip changes
MEDIA_DATE = "2026-10-27"          # when the demo clips were last recorded (VideoObject uploadDate)
ICON_TG = ('<svg class="tgi" viewBox="0 0 24 24" aria-hidden="true"><path d="M21.9 4.3 18.6 19.8c-.2 1.1-.9 1.4-1.8.9l-5-3.7-2.4 '
           '2.3c-.3.3-.5.5-1 .5l.4-5.1 9.3-8.4c.4-.4-.1-.6-.6-.2L5.9 13.3l-5-1.6c-1.1-.3-1.1-1.1.2-1.6L20.6 2.6c.9-.3 1.7.2 1.3 1.7z"/></svg>')
DLI = ('<svg class="dli" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 '
       '2-2v-2" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
# the chat apps' marks (simple glyphs drawn here, not the companies' logo files)
ICONS = {
    "dl": DLI,
    "wa": '<svg class="ai" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.7l5-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>',
    "tg": '<svg class="ai" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M21.9 4.3 18.6 19.8c-.2 1.1-.9 1.4-1.8.9l-5-3.7-2.4 2.3c-.3.3-.5.5-1 .5l.4-5.1 9.3-8.4c.4-.4-.1-.6-.6-.2L5.9 13.3l-5-1.6c-1.1-.3-1.1-1.1.2-1.6L20.6 2.6c.9-.3 1.7.2 1.3 1.7z"/></svg>',
    "ms": '<svg class="ai" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5C6.6 2.5 2.5 6.4 2.5 11.6c0 2.8 1.2 5.2 3.1 6.9v3.2l2.9-1.6c1.1.3 2.2.5 3.5.5 5.4 0 9.5-3.9 9.5-9S17.4 2.5 12 2.5zm1 12.2-2.4-2.6-4.7 2.6 5.2-5.5 2.5 2.6 4.6-2.6-5.2 5.5z"/></svg>',
    "ig": '<svg class="ai" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M7.5 3h9A4.5 4.5 0 0 1 21 7.5v9a4.5 4.5 0 0 1-4.5 4.5h-9A4.5 4.5 0 0 1 3 16.5v-9A4.5 4.5 0 0 1 7.5 3z"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></svg>',
    "dc": '<svg class="ai" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M19.3 5.4A16.5 16.5 0 0 0 15.2 4l-.5 1a15 15 0 0 0-5.4 0l-.5-1a16.4 16.4 0 0 0-4.1 1.4C2.1 9.3 1.4 13.1 1.8 16.9a16.6 16.6 0 0 0 5 2.6l1.1-1.7a10.7 10.7 0 0 1-1.7-.8l.4-.3a11.8 11.8 0 0 0 10.2 0l.4.3-1.7.8 1.1 1.7a16.5 16.5 0 0 0 5-2.6c.5-4.4-.8-8.2-2.3-11.5zM8.5 14.6c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2zm7 0c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2z"/></svg>',
}
IMAGES = {
    "switcher": {"src": "/assets/img/app-switcher.webp", "w": 1080, "h": 840},
}


# ------------------------------------------------------------------ content
ONLY = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--lang=")]     # --lang=en: build one language while editing


def load_content():
    out = {}
    for code in cfg.LANGS:
        if ONLY and code not in ONLY[0].split(","):
            continue
        p = os.path.join(HERE, "content", f"{code}.yaml")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                out[code] = yaml.safe_load(f)
    if cfg.DEFAULT_LANG not in out:
        sys.exit("src/content/en.yaml is missing")
    return out


def flat_keys(d, prefix=""):
    keys = set()
    if isinstance(d, dict):
        for k, v in d.items():
            keys.add(prefix + str(k))
            keys |= flat_keys(v, prefix + str(k) + ".")
    return keys


def validate(content):
    """Every language must have every UI string English has (pages may be a subset)."""
    ref = flat_keys(content["en"]["ui"])
    problems = []
    for code, c in content.items():
        if code == "en":
            continue
        missing = sorted(ref - flat_keys(c.get("ui", {})))
        if missing:
            problems.append(f"{code}: ui keys missing: {', '.join(missing[:12])}{' …' if len(missing) > 12 else ''}")
        for pid, pg in (c.get("pages") or {}).items():
            if pid not in content["en"]["pages"] and not pg.get("single"):
                problems.append(f"{code}: page '{pid}' does not exist in en.yaml (or mark it single: true)")
            for k in ("title", "description", "blocks"):
                if not pg.get(k):
                    problems.append(f"{code}: page '{pid}' has no {k}")
    for code, c in content.items():
        for pid, pg in (c.get("pages") or {}).items():
            t, d = pg.get("title", ""), pg.get("description", "")
            if len(t) > 70:
                problems.append(f"warn {code}/{pid}: title is {len(t)} chars (keep ≤ 65)")
            if len(d) > 165 and not code.startswith("zh"):
                problems.append(f"warn {code}/{pid}: description is {len(d)} chars (keep ≤ 160)")
    return problems


# ------------------------------------------------------------------ urls
def path_of(lang, pid):
    base = "/" if lang == cfg.DEFAULT_LANG else f"/{lang}/"
    if pid == "home":
        return base
    return f"{base}{pid}/"


def out_file(lang, pid):
    p = path_of(lang, pid).strip("/")
    return os.path.join(ROOT, *(p.split("/") if p else []), "index.html")


# ------------------------------------------------------------------ helpers
def mark(v):
    s = str(v)
    rep = {"✓": '<span class="y" aria-label="yes">✓</span>', "✕": '<span class="n" aria-label="no">✕</span>',
           "~": '<span class="m" aria-label="partly">~</span>'}
    if s.strip() in rep:
        return Markup(rep[s.strip()])
    for k, r in rep.items():
        if s.startswith(k + " "):
            return Markup(r + " " + s[2:])
    return Markup(s)


def slugify(text):
    t = re.sub(r"<[^>]+>", "", text).strip().lower()
    t = re.sub(r"[^\w\s-]", "", t, flags=re.U)
    return re.sub(r"[\s_]+", "-", t)[:60] or "s"


def render_md(md_text):
    html = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    toc, seen = [], set()

    def h2(m):
        title = m.group(1)
        sid = slugify(title)
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        toc.append((sid, re.sub(r"<[^>]+>", "", title)))
        return f'<h2 id="{sid}">{title}</h2>'
    html = re.sub(r"<h2>(.*?)</h2>", h2, html)
    html = html.replace("<table>", '<div class="tbl-wrap"><table class="tbl">').replace("</table>", "</table></div>")
    return html, toc


def words(text, lang):
    plain = re.sub(r"<[^>]+>", " ", text)
    if lang.startswith("zh"):
        return len(re.findall(r"[一-鿿]", plain)) // 2 + len(re.findall(r"[A-Za-z]+", plain))
    return len(re.findall(r"\w+", plain, flags=re.U))


def ld(obj):
    return Markup(json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))


# ------------------------------------------------------------------ build
def build(make_og=True):
    content = load_content()
    problems = validate(content)
    errors = [p for p in problems if not p.startswith("warn")]
    for p in problems:
        print(("  ! " if p in errors else "  · ") + p)
    if errors:
        sys.exit("fix the content errors above")

    en_pages = content["en"]["pages"]
    page_ids = list(en_pages)
    for c in content.values():                    # + pages written for one language only (single: true)
        page_ids += [pid for pid in (c.get("pages") or {}) if pid not in page_ids]
    available = {pid: [l for l in cfg.LANGS if l in content and pid in (content[l].get("pages") or {})] for pid in page_ids}

    env = Environment(loader=FileSystemLoader(os.path.join(HERE, "templates")), autoescape=True,
                      trim_blocks=False, lstrip_blocks=False)
    env.filters["mark"] = mark
    tpl = env.get_template("page.html")

    def asset_hash():
        h = hashlib.sha1()
        for p in ("assets/css/style.css", "assets/js/main.js"):
            with open(os.path.join(ROOT, p), "rb") as f:
                h.update(f.read())
        return h.hexdigest()[:8]
    version = asset_hash()

    # demo clips are cached for a year under their name, so a re-recorded clip needs a new address:
    # ?v= changes whenever any media file changes (name or size)
    mh = hashlib.sha1()
    for fn in sorted(os.listdir(os.path.join(ROOT, "assets", "media"))):
        mh.update(f"{fn}:{os.path.getsize(os.path.join(ROOT, 'assets', 'media', fn))};".encode())
    mv = mh.hexdigest()[:8]
    global MEDIA_V
    MEDIA_V = mv

    today = dt.date.today().isoformat()
    lastmod = load_lastmod()
    generated, sitemap = [], []
    og_jobs = []
    stats = {}

    for lang, c in content.items():
        L = dict(cfg.LANGS[lang], code=lang)
        ui = c["ui"]
        pages = c.get("pages") or {}

        def link(pid, _lang=lang):
            pid = pid.strip("/")
            if pid == "" or pid == "home":
                pid = "home"
            if pid in available and _lang in available[pid]:
                return path_of(_lang, pid)
            if pid in available and "en" in available[pid]:
                return path_of("en", pid)
            return path_of(_lang, pid)

        def reg(pid):
            p = pages.get(pid) or en_pages.get(pid)
            return {"short": p.get("short") or p.get("title"), "description": p.get("description", ""),
                    "icon": p.get("icon", "📄"), "h1": re.sub(r"<[^>]+>", "", next((b.get("h1", "") for b in p["blocks"] if b.get("h1")), p.get("title")))}
        registry = {pid: reg(pid) for pid in page_ids if pid in pages or pid in en_pages}
        industries = [dict(slug=pid.split("/", 1)[1], name=(pages.get(pid) or en_pages[pid]).get("short"),
                           short=(pages.get(pid) or en_pages[pid]).get("nav_sub", ""), icon=(pages.get(pid) or en_pages[pid]).get("icon", ""))
                      for pid in page_ids if pid.startswith("for/")]
        guides = [dict(id=pid, **registry[pid]) for pid in page_ids if pid.startswith("guides/") and pid in registry]

        contacts = []
        if cfg.WHATSAPP_NUMBER:
            contacts.append({"label": "WhatsApp", "href": f"https://wa.me/{cfg.WHATSAPP_NUMBER}", "ext": True})
        if cfg.WECHAT_ID and lang.startswith("zh"):
            contacts.append({"label": f"微信 {cfg.WECHAT_ID}", "href": "#", "copy": cfg.WECHAT_ID})
        if cfg.EMAIL:
            contacts.append({"label": cfg.EMAIL, "href": f"mailto:{cfg.EMAIL}"})

        gc = {"lang": lang, "vlang": L.get("media", lang), "tg": cfg.TELEGRAM_USER, "msg": ui["msg"], "plans": {k: v["name"] for k, v in ui["plans"].items()},
              "copied": ui["copied"], "langs": list(available["home"]), "default": cfg.DEFAULT_LANG, "mv": mv}

        for pid, page in pages.items():
            page = dict(page)
            url = cfg.SITE + path_of(lang, pid)
            blocks = []
            toc = []
            for b in page["blocks"]:
                b = dict(b)
                if b["type"] == "prose":
                    b["html"], t = render_md(b["md"])
                    toc += t
                elif b["type"] == "html" and "md" in b:
                    b["html"], _ = render_md(b["md"])
                blocks.append(b)
            page["blocks"] = blocks
            if page.get("article"):
                upd = str(page.get("updated") or today)
                page["updated"] = upd
                page["updated_h"] = upd
                txt = " ".join(b.get("html", "") for b in blocks)
                page["read_min"] = max(2, round(words(txt, lang) / 200))

            alts = [{"hreflang": cfg.LANGS[l]["hreflang"], "url": cfg.SITE + path_of(l, pid), "og": cfg.LANGS[l]["og"]}
                    for l in available.get(pid, [lang])]
            if not page.get("special") and "en" in available.get(pid, []):
                alts.append({"hreflang": "x-default", "url": cfg.SITE + path_of("en", pid), "og": None})
            if page.get("special") or page.get("single"):
                alts = []
            lang_menu = [{"code": l, "name": cfg.LANGS[l]["name"], "hreflang": cfg.LANGS[l]["hreflang"],
                          "html": cfg.LANGS[l]["html"],
                          "url": path_of(l, pid) if l in available.get(pid, []) and not page.get("special") else path_of(l, "home")}
                         for l in cfg.LANGS if l in content]

            # breadcrumbs
            crumbs = [{"name": ui["breadcrumb_home"], "url": link("home")}]
            if pid.startswith("guides/"):
                crumbs.append({"name": ui["nav"]["guides"], "url": link("guides")})
            if pid not in ("home", "404"):
                crumbs.append({"name": page.get("short") or page["title"], "url": path_of(lang, pid)})

            og_rel = f"/assets/og/{lang}-{pid.replace('/', '-')}.jpg"
            og_jobs.append({"file": os.path.join(ROOT, og_rel.lstrip("/")), "lang": lang, "dir": L["dir"],
                            "kicker": page.get("og_kicker") or ui["og_kicker"],
                            "title": re.sub(r"<[^>]+>", "", page.get("og_heading") or registry.get(pid, {}).get("h1") or page["title"]),
                            "sub": page.get("og_sub") or ui["og_sub"], "chips": ui["og_chips"]})

            jsonld = ld(make_jsonld(lang, pid, page, url, crumbs, ui, og_rel, blocks))
            vlang = L.get("media", lang)      # demo videos exist per website language (繁體 uses 简体)
            preload = None                    # (desktop image, phone image) of the first big picture
            if blocks and blocks[0]["type"] == "hero_home":
                first = blocks[0]["chapters"][0]["id"]
                preload = (f"/assets/media/{first}-{vlang}-land.webp?v={mv}", f"/assets/media/{first}-{vlang}-port.webp?v={mv}")
            elif blocks and blocks[0].get("media", "").startswith("img:"):
                preload = (IMAGES[blocks[0]["media"].split(":")[1]]["src"], None)
            elif blocks and blocks[0].get("media", "").startswith("video:"):
                name = blocks[0]["media"].split(":")[1]
                preload = (f"/assets/media/{name}-{vlang}-land.webp?v={mv}", f"/assets/media/{name}-{vlang}-port.webp?v={mv}")

            html = tpl.render(
                cfg=cfg, L=L, lang=lang, ui=ui, page=page, page_id=pid, url=url, alternates=alts,
                lang_menu=lang_menu, link=link, home_url=link("home"), tg=f"https://t.me/{cfg.TELEGRAM_USER}", dl=cfg.DOWNLOAD,
                icon_tg=ICON_TG, icons=ICONS, industries=industries, guides=guides, registry=registry, crumbs=crumbs,
                og_image=cfg.SITE + og_rel, jsonld=jsonld,
                gc=ld(dict(gc, alts={l: path_of(l, pid) for l in available.get(pid, [])})), v=version, vlang=vlang, images=IMAGES,
                toc=toc, contacts=contacts, preload=preload, mv=mv, arr='←' if L['dir'] == 'rtl' else '→')
            html = re.sub(r"\n\s*\n+", "\n", html)
            dest = os.path.join(ROOT, "404.html") if pid == "404" else out_file(lang, pid)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", newline="\n") as f:
                f.write(html)
            rel = os.path.relpath(dest, ROOT).replace("\\", "/")
            generated.append(rel)
            touch_lastmod(lastmod, rel, html, today)
            stats[lang] = stats.get(lang, 0) + 1
            if not page.get("special") and "noindex" not in (page.get("robots") or ""):
                sitemap.append((pid, lang, rel))

    if ONLY:                                       # a one-language build: the other languages' files stay as they are
        print(f"built {len(generated)} pages ({ONLY[0]} only) — build all languages before committing")
        if make_og:
            render_og(og_jobs)
        return
    clean_old(generated)
    save_lastmod({k: v for k, v in lastmod.items() if k in generated})
    write_sitemap(sitemap, available, lastmod)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /src/\nDisallow: /_tools/\n\nSitemap: {cfg.SITE}/sitemap.xml\n")
    write_llms(content["en"], available)
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(sorted(generated), f, indent=0)
    if make_og:
        render_og(og_jobs)
    print(f"built {len(generated)} pages for {cfg.SITE}: " + ", ".join(f"{k} {v}" for k, v in stats.items()))


def make_jsonld(lang, pid, page, url, crumbs, ui, og_rel, blocks):
    S = cfg.SITE
    hl = cfg.LANGS[lang]["hreflang"]
    org = {"@type": "Organization", "@id": S + "/#org", "name": "GlotChat", "alternateName": "Glot Chat",
           "url": S + "/", "description": "Maker of GlotChat, the all-in-one messenger with translation for Windows.",
           "logo": {"@type": "ImageObject", "url": S + "/assets/img/icon-512.png", "width": 512, "height": 512},
           "sameAs": [f"https://t.me/{cfg.TELEGRAM_USER}", *cfg.SAME_AS],
           "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "url": f"https://t.me/{cfg.TELEGRAM_USER}",
                            "availableLanguage": ["English", "Chinese", "Arabic", "Turkish", "Spanish", "Portuguese", "Russian"]}}
    # alternateName: what GlotChat is, in the words people search ("GlotChat – All-in-One Messenger")
    site = {"@type": "WebSite", "@id": S + "/#website", "url": S + "/", "name": "GlotChat",
            "alternateName": ["Glot Chat", "GlotChat All-in-One Messenger", "GlotChat Messenger"],
            "inLanguage": [cfg.LANGS[l]["hreflang"] for l in cfg.LANGS], "publisher": {"@id": S + "/#org"}}
    webpage = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": page["title"],
               "description": page["description"], "inLanguage": hl, "isPartOf": {"@id": S + "/#website"},
               "primaryImageOfPage": {"@type": "ImageObject", "url": S + og_rel}}
    graph = [org, site, webpage]
    if len(crumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c["name"], "item": S + c["url"]} for i, c in enumerate(crumbs)]})
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
    if page.get("app", True) and not page.get("special") and not pid.startswith(("privacy", "terms")):
        pricing_url = S + path_of(lang, "pricing")
        graph.append({
            "@type": "SoftwareApplication", "@id": S + f"/#app-{lang}", "name": "GlotChat",
            "alternateName": "GlotChat All-in-One Messenger",
            "url": S + path_of(lang, "home"), "operatingSystem": cfg.FACTS["os"],
            "applicationCategory": "BusinessApplication", "applicationSubCategory": "Communication",
            "description": ui["app_description"], "image": S + og_rel, "inLanguage": hl,
            "featureList": ui["feature_list"], "publisher": {"@id": S + "/#org"},
            "downloadUrl": cfg.DOWNLOAD["url"], "installUrl": S + path_of(lang, "download"),
            "softwareVersion": cfg.DOWNLOAD["version"], "fileSize": f"{cfg.DOWNLOAD['size_mb']}MB",
            "softwareRequirements": "Windows 10 or Windows 11, 64-bit", "memoryRequirements": "4 GB RAM",
            "storageRequirements": "2 GB free disk space",
            "offers": [{"@type": "Offer", "name": ui["plans"][p["id"]]["name"], "price": str(p["price"]),
                        "priceCurrency": "USD", "url": pricing_url, "availability": "https://schema.org/InStock",
                        "category": "subscription",
                        "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(p["price"]),
                                               "priceCurrency": "USD", "unitCode": "ANN", "referenceQuantity":
                                               {"@type": "QuantitativeValue", "value": 1, "unitCode": "ANN"}}}
                       for p in cfg.PLANS]})
        webpage["about"] = {"@id": S + f"/#app-{lang}"}
    if page.get("article"):
        graph.append({"@type": "Article", "@id": url + "#article", "headline": re.sub(r"<[^>]+>", "", page.get("og_heading") or page["title"])[:110],
                      "description": page["description"], "inLanguage": hl, "image": S + og_rel,
                      "datePublished": str(page.get("published") or page["updated"]), "dateModified": page["updated"],
                      "author": {"@id": S + "/#org"}, "publisher": {"@id": S + "/#org"},
                      "mainEntityOfPage": {"@id": url + "#webpage"}})
    # the demo clips of the page, for Google's video results
    vlang = cfg.LANGS[lang].get("media", lang)
    vids = []
    for b in blocks:
        if b["type"] == "hero_home":
            vids += [(c["id"], c["label"], c["cap"]) for c in b["chapters"]]
        elif b["type"] == "showcase":
            vids += [(r["media"].split(":")[1], r["h"], r["p"]) for r in b["rows"] if r["media"].startswith("video:")]
    seen = set()
    for scene, name, desc in vids:
        if scene in seen:
            continue
        seen.add(scene)
        graph.append({"@type": "VideoObject", "@id": url + "#video-" + scene,
                      "name": "GlotChat – " + re.sub(r"<[^>]+>", "", name), "description": re.sub(r"<[^>]+>", "", desc),
                      "inLanguage": hl, "thumbnailUrl": S + f"/assets/media/{scene}-{vlang}-land.webp?v={MEDIA_V}",
                      "contentUrl": S + f"/assets/media/{scene}-{vlang}-land.mp4?v={MEDIA_V}", "uploadDate": MEDIA_DATE,
                      "publisher": {"@id": S + "/#org"}})
    faq = [b for b in blocks if b["type"] == "faq"]
    if faq:
        items = [it for b in faq for it in b["items"]]
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": hl, "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", _html.unescape(a))}}
            for q, a in items]})
    return {"@context": "https://schema.org", "@graph": graph}


def clean_old(generated):
    """Delete pages a previous build made that this build didn't (renamed/removed pages)."""
    try:
        with open(MANIFEST, encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        old = []
    keep = set(generated)
    for rel in old:
        if rel in keep or not rel.endswith(".html"):
            continue
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            os.remove(p)
            d = os.path.dirname(p)
            while d != ROOT and os.path.isdir(d) and not os.listdir(d):
                os.rmdir(d)
                d = os.path.dirname(d)


LASTMOD = os.path.join(HERE, "lastmod.json")


def load_lastmod():
    """{output file: {"hash", "date"}}: the date each page's HTML last really changed.

    A sitemap that says "changed today" for every page on every build teaches Google to ignore
    <lastmod>; with real dates it can tell which pages are worth crawling again."""
    try:
        with open(LASTMOD, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def touch_lastmod(lastmod, rel, html, today):
    h = hashlib.sha1(html.encode("utf-8")).hexdigest()[:16]
    old = lastmod.get(rel)
    if old and old["hash"] == h:
        return
    date = today
    if old is None:  # first time recorded: if the page is the same as in the last commit, use that commit's date
        committed = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True)
        if committed.returncode == 0 and hashlib.sha1(committed.stdout).hexdigest()[:16] == h:
            r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT, capture_output=True, text=True)
            date = r.stdout.strip() or today
    lastmod[rel] = {"hash": h, "date": date}


def save_lastmod(lastmod):
    with open(LASTMOD, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(lastmod.items())), f, indent=0)


def write_sitemap(entries, available, lastmod):
    S = cfg.SITE
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for pid, lang, rel in entries:
        if pid == "404":
            continue
        out.append("  <url>")
        out.append(f"    <loc>{S}{path_of(lang, pid)}</loc>")
        out.append(f"    <lastmod>{lastmod[rel]['date']}</lastmod>")
        langs = available.get(pid, [])
        if len(langs) > 1:
            for l in langs:
                out.append(f'    <xhtml:link rel="alternate" hreflang="{cfg.LANGS[l]["hreflang"]}" href="{S}{path_of(l, pid)}"/>')
            if "en" in langs:  # Chinese-only guides have no English page to be the default
                out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{S}{path_of("en", pid)}"/>')
        out.append("  </url>")
    out.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")


def write_llms(en, available):
    """llms.txt — a plain summary that AI assistants (ChatGPT, Perplexity, …) can read."""
    S = cfg.SITE
    ui = en["ui"]
    lines = [f"# GlotChat", "", f"> {ui['app_description']}", "",
             "GlotChat is a Windows desktop app — an all-in-one messenger for business. It opens the official websites of WhatsApp, "
             "Telegram, Facebook Messenger, Instagram and Discord for each account in its own isolated session, several accounts per app, "
             "and adds offline two-way translation of messages in every app (plus voice notes and text in photos on WhatsApp and Telegram). "
             "Before a reply is sent, it shows the translation translated back into the writer's language and checks that prices, numbers "
             "and links are unchanged. It is an independent product, not affiliated with WhatsApp, Meta, Telegram or Discord.", "",
             "## Key facts", "",
             f"- Platform: {cfg.FACTS['os']} (64-bit)",
             "- Apps: WhatsApp, WhatsApp Business, Telegram, Facebook Messenger, Instagram Direct, Discord (several accounts of each; all apps in every plan)",
             f"- Accounts: tested with {cfg.FACTS['accounts_tested']} accounts at the same time; each uses about {cfg.FACTS['ram_per_account']} of memory",
             f"- Translation: {cfg.FACTS['languages']} languages, offline on the user's PC; voice notes recognised in about {cfg.FACTS['voice_languages']} languages",
             f"- Free trial: {cfg.TRIAL_DAYS} days, every feature, no payment — starts with one click in the app (\"Start my free 3-day trial\"), one trial per computer",
             f"- Download (Windows installer, version {cfg.DOWNLOAD['version']}, {cfg.DOWNLOAD['size_mb']} MB): {cfg.DOWNLOAD['url']} — install guide: {S}{path_of('en', 'download')}",
             "- Prices (per year, paid in USDT " + cfg.PAY_NETWORKS + "): " + ", ".join(
                 f"{p['id']} {p['price']} USDT ({'unlimited' if p['accounts'] is None else 'up to ' + str(p['accounts'])} accounts per app, {p['pcs']} PC{'s' if p['pcs'] > 1 else ''})" for p in cfg.PLANS),
             f"- Contact / purchase: Telegram https://t.me/{cfg.TELEGRAM_USER}",
             f"- Website languages: " + ", ".join(cfg.LANGS[l]["name"] for l in available["home"]), "",
             "## Pages", ""]
    for pid, p in en["pages"].items():
        if p.get("special"):
            continue
        lines.append(f"- [{p.get('short') or p['title']}]({S}{path_of('en', pid)}): {p['description']}")
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def render_og(jobs):
    """1200×630 social preview per page, rendered with headless Chrome."""
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(ROOT, "assets", "og"), exist_ok=True)
    tpl = open(os.path.join(HERE, "templates", "og.html"), encoding="utf-8").read()
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for j in jobs:
            html = (tpl.replace("{{dir}}", j["dir"]).replace("{{lang}}", j["lang"])
                    .replace("{{kicker}}", _html.escape(j["kicker"])).replace("{{title}}", _html.escape(j["title"]))
                    .replace("{{sub}}", _html.escape(j["sub"]))
                    .replace("{{chips}}", "".join(f"<span>{_html.escape(c)}</span>" for c in j["chips"]))
                    .replace("{{root}}", ROOT.replace("\\", "/")))
            tmp = os.path.join(HERE, "templates", "_og_tmp.html")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(html)
            pg.goto("file:///" + tmp.replace("\\", "/"))
            pg.wait_for_timeout(120)
            pg.screenshot(path=j["file"], type="jpeg", quality=84)
        b.close()
    try:
        os.remove(os.path.join(HERE, "templates", "_og_tmp.html"))
    except OSError:
        pass
    print(f"rendered {len(jobs)} preview images")


if __name__ == "__main__":
    build(make_og="--no-og" not in sys.argv)

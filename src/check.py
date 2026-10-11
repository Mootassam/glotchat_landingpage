"""SEO + integrity check for the generated site.   python src/check.py

Checks every generated page: title/description length, canonical = own URL, hreflang
alternates point back (reciprocal), valid JSON-LD, one <h1>, image alt text, the preview
image exists, no template leftovers, every internal link and asset resolves to a file,
and the sitemap lists exactly the indexable pages.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import config as cfg  # noqa: E402


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.in_title, self.h1, self.meta, self.links, self.imgs = "", False, 0, {}, [], []
        self.hrefs, self.srcs, self.ld, self.in_ld = [], [], [], False

    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "title":
            self.in_title = True
        elif t == "h1":
            self.h1 += 1
        elif t == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        elif t == "link":
            self.links.append(a)
        elif t == "img":
            self.imgs.append(a)
        elif t == "script" and a.get("type") == "application/ld+json":
            self.in_ld = True
            self.ld.append("")
        if t == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        for k in ("src", "data-src", "poster"):
            if a.get(k):
                self.srcs.append(a[k])
        if t == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest", "preload"):
            self.srcs.append(a.get("href", ""))

    def handle_endtag(self, t):
        if t == "title":
            self.in_title = False
        if t == "script":
            self.in_ld = False

    def handle_data(self, d):
        if self.in_title:
            self.title += d
        if self.in_ld:
            self.ld[-1] += d


def file_for(path):
    path = path.split("#")[0].split("?")[0]
    if not path.startswith("/"):
        return None
    p = os.path.join(ROOT, *[x for x in path.split("/") if x])
    if path.endswith("/"):
        p = os.path.join(p, "index.html")
    return p


def main():
    with open(os.path.join(ROOT, ".generated.json"), encoding="utf-8") as f:
        pages = json.load(f)
    errors, warns, parsed = [], [], {}
    for rel in pages:
        html = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        p = Page()
        p.feed(html)
        url = cfg.SITE + "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)
        parsed[url] = p
        where = rel
        if "{{" in html or "{%" in html or ">None<" in html or "Undefined" in html:
            errors.append(f"{where}: template leftovers")
        t, d = p.title.strip(), p.meta.get("description", "")
        if not t or len(t) > 70:
            warns.append(f"{where}: title {len(t)} chars")
        if not d or len(d) > 165:
            warns.append(f"{where}: description {len(d)} chars")
        if p.h1 != 1:
            errors.append(f"{where}: {p.h1} <h1>")
        canon = [l.get("href") for l in p.links if l.get("rel") == "canonical"]
        if rel != "404.html" and canon != [url]:
            errors.append(f"{where}: canonical {canon} != {url}")
        for j in p.ld:
            try:
                json.loads(j)
            except Exception as e:
                errors.append(f"{where}: JSON-LD invalid ({e})")
        for im in p.imgs:
            if im.get("alt") is None:
                errors.append(f"{where}: <img {im.get('src')}> has no alt")
        og = p.meta.get("og:image", "")
        if not og.startswith(cfg.SITE) or not os.path.isfile(file_for(og[len(cfg.SITE):]) or ""):
            errors.append(f"{where}: og:image missing {og}")
        for h in p.hrefs + p.srcs:
            if h.startswith(cfg.SITE):
                h = h[len(cfg.SITE):] or "/"
            f = file_for(h)
            if f is None or h.startswith("/_vercel/"):
                continue
            if not (os.path.isfile(f) or os.path.isfile(f + ".html")):
                errors.append(f"{where}: broken link {h}")
    # hreflang reciprocity
    for url, p in parsed.items():
        alts = {l["hreflang"]: l["href"] for l in p.links if l.get("rel") == "alternate" and l.get("hreflang")}
        for hl, href in alts.items():
            if hl == "x-default":
                continue
            other = parsed.get(href)
            if other is None:
                errors.append(f"{url}: hreflang {hl} -> {href} not generated")
                continue
            back = {l["hreflang"]: l["href"] for l in other.links if l.get("rel") == "alternate" and l.get("hreflang")}
            if url not in back.values():
                errors.append(f"{url}: hreflang {hl} -> {href} doesn't point back")
    # sitemap
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
    indexable = {u for u, p in parsed.items() if "noindex" not in p.meta.get("robots", "")}
    for u in indexable - locs:
        errors.append(f"sitemap missing {u}")
    for u in locs - indexable:
        errors.append(f"sitemap lists non-page {u}")
    for w in warns:
        print("  · " + w)
    for e in errors:
        print("  ✗ " + e)
    print(f"\nchecked {len(parsed)} pages, {len(locs)} sitemap URLs: {len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

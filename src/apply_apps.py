"""Apply the 2026-10 "five apps" update to a translated language file.

    python src/apply_apps.py <lang>        reads src/patches/apps-<lang>.yaml

The patch holds: ui (merged), pages (added / replaced), and "home" / "pricing" with the new texts of the
home page and the pricing table. Those two pages keep everything else of their existing translation.
"""
import os
import sys

import yaml

from merge_content import Dumper, deep

HERE = os.path.dirname(os.path.abspath(__file__))


def main(lang):
    path = os.path.join(HERE, "content", f"{lang}.yaml")
    with open(path, encoding="utf-8") as f:
        cur = yaml.safe_load(f)
    with open(os.path.join(HERE, "patches", f"apps-{lang}.yaml"), encoding="utf-8") as f:
        pt = yaml.safe_load(f)
    first = pt["ui"].pop("feature_first")         # replaces "WhatsApp and Telegram…" + "… (beta)" in feature_list
    cur["ui"]["feature_list"][0:2] = [first]
    deep(cur["ui"], pt["ui"])
    pages = cur["pages"]
    # new pages go right after the Telegram pages (the order sets the sitemap and llms.txt order)
    order = list(pages.items())
    at = max(i for i, (k, _) in enumerate(order) if k in ("telegram-translator", "multiple-telegram-accounts")) + 1
    new = [(k, v) for k, v in pt["pages"].items() if k not in pages]
    order = order[:at] + new + [(k, v) for k, v in order[at:]]
    pages = dict(order)
    for k, v in pt["pages"].items():
        pages[k] = v
    cur["pages"] = pages

    h, H = pt["home"], pages["home"]
    for k in ("title", "description", "keywords", "og_title", "og_heading"):
        if k in h:
            H[k] = h[k]
    by = {}
    for b in H["blocks"]:
        by.setdefault(b["type"], b)
    hero = by["hero_home"]
    hero.update({k: h[k] for k in ("eyebrow", "h1", "lead")})
    hero["chapters"] = [dict(id="apps", icon="🧩", **h["chapter"]) if c["id"] == "telegram" else c for c in hero["chapters"]]
    by["facts"]["items"][0] = h["fact"]
    apps = by["apps"]
    apps["h"] = h["apps_h"]
    apps["items"] = apps["items"][:2] + h["apps_items"]
    apps["note"] = h["apps_note"]
    apps["link"] = ["all-in-one-messenger", h["apps_link"]]
    rows = by["showcase"]["rows"]
    if not any(r["media"] == "video:apps" for r in rows):
        i = next(i for i, r in enumerate(rows) if r["media"] == "video:telegram")
        rows.insert(i + 1, dict(media="video:apps", **h["showcase"]))
    by["vs"]["good"][0] = h["vs_good"]
    faq = by["faq"]["items"]
    faq[1] = h["faq_apps"]
    faq[2][1] = h["faq_safe"]
    by["related"]["items"] = ["all-in-one-messenger", "telegram-translator", "instagram-dm-translator"]

    tbl = next(b for b in pages["pricing"]["blocks"] if b["type"] == "table")
    tbl["rows"][0][0] = pt["pricing"]["accounts"]
    tbl["rows"][4][0] = pt["pricing"]["apps"]

    head = f"# GlotChat website — {lang} (structure follows en.yaml; updated with src/merge_content.py and src/apply_apps.py)\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(head)
        yaml.dump(cur, f, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=10000, default_flow_style=False)
    print(f"{lang}: {len(pt['pages'])} pages, home + pricing updated")


if __name__ == "__main__":
    main(sys.argv[1])

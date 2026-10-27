"""Apply a partial translation on top of a language file.

    python src/merge_content.py <lang> <patch.yaml>

The patch has the same shape as src/content/<lang>.yaml (ui: …, pages: …). Its ui keys are merged
into the existing ones (deep merge); every page it contains replaces that page completely.
Used for the 2026-10 Telegram update, so pages that didn't change keep their existing translation.
"""
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))


def deep(a, b):
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            deep(a[k], v)
        else:
            a[k] = v
    return a


class Dumper(yaml.SafeDumper):
    pass


def _str(d, s):
    if "\n" in s:
        return d.represent_scalar("tag:yaml.org,2002:str", s, style="|")
    return d.represent_scalar("tag:yaml.org,2002:str", s)


Dumper.add_representer(str, _str)


def main(lang, patch_file):
    path = os.path.join(HERE, "content", f"{lang}.yaml")
    with open(path, encoding="utf-8") as f:
        cur = yaml.safe_load(f)
    with open(patch_file, encoding="utf-8") as f:
        patch = yaml.safe_load(f)
    deep(cur.setdefault("ui", {}), patch.get("ui") or {})
    pages = cur.setdefault("pages", {})
    for pid, pg in (patch.get("pages") or {}).items():
        pages[pid] = pg
    for pid in patch.get("drop") or []:
        pages.pop(pid, None)
    head = f"# GlotChat website — {lang} (structure follows en.yaml; updated with src/merge_content.py)\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(head)
        yaml.dump(cur, f, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=10000, default_flow_style=False)
    print(f"{lang}: {len(patch.get('pages') or {})} pages replaced, ui merged")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

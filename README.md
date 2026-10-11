# GlotChat website — www.glotchat.com

Static, multi-language marketing site, generated from templates + one text file per language.
Every button opens Telegram **@GlotChat** with a ready-made message in the visitor's language.

## Languages and pages

7 languages: English (`/`), 中文 (`/zh/`), العربية (`/ar/`, right-to-left), Türkçe (`/tr/`),
Español (`/es/`), Português (`/pt/`), Русский (`/ru/`). Each has 12 pages:

| Page | Path |
|---|---|
| Home | `/` |
| Pricing | `/pricing/` |
| WhatsApp translator | `/whatsapp-translator/` |
| Multiple WhatsApp accounts | `/multiple-whatsapp-accounts/` |
| Comparison | `/compare/` |
| Industries | `/for/real-estate/`, `/for/clinics/`, `/for/exporters/`, `/for/travel/` |
| Guides | `/guides/` + 2 guides |

Plus (English only) `/privacy/`, `/terms/`, `/404.html`, and `sitemap.xml`, `robots.txt`, `llms.txt`.

## Edit and rebuild

```
python src/build.py          # build every page (+ social preview images, needs Chrome + Playwright)
python src/build.py --no-og  # faster while editing text
python src/check.py          # SEO + broken-link check — must say 0 errors
```

- **Text:** `src/content/<lang>.yaml`. `en.yaml` is the reference; the build refuses to run if another
  language is missing a UI text that English has.
- **Layout:** `src/templates/` (`base.html` = head, header, footer; `page.html` = the content blocks).
- **Prices, contact, product facts, languages:** `src/config.py`.
  Optional extra contact buttons: set `WHATSAPP_NUMBER`, `WECHAT_ID` (shown on 中文 pages — Telegram is
  blocked in mainland China) or `EMAIL` and rebuild.
- **Never edit the generated `index.html` files directly** — they are overwritten by the build.

Commit the generated files: Vercel serves the repository as plain static files (no build step on Vercel).
`src/`, `_tools/` and this README are not deployed (`.vercelignore`).

## SEO built in

- Static HTML per language, `hreflang` between all 7 versions + `x-default`, canonical URLs.
- Structured data: Organization, WebSite, WebPage, BreadcrumbList, SoftwareApplication with the three
  plans as Offers (price in USD — USDT is pegged), FAQPage, Article (guides).
- Per-page social preview image (`assets/og/<lang>-<page>.jpg`), titles ≤ 70 and descriptions ≤ 160 chars.
- `sitemap.xml` with language alternates, `robots.txt`, `llms.txt` for AI assistants.
- First visit: visitors whose browser language is one of the 7 are sent to their language once
  (search engines are not redirected; a manual language choice is remembered).
- `vercel.json`: the old `glotchatlandingpage.vercel.app` address redirects permanently to www.glotchat.com.

After a deploy, in **Google Search Console** submit `https://www.glotchat.com/sitemap.xml`
(and the same in Bing Webmaster Tools).

## Analytics

Vercel Web Analytics events: `telegram_click` (place, plan, lang), `plan_finder`, `calculator`,
`exit_popup`, `demo_tab`, `language`, `copy`.

## Media

| File | Use |
|---|---|
| `assets/media/*-en.mp4`, `*-zh.mp4` | Demo videos (English / Chinese agent) |
| `assets/media/*.webp` | Video posters |
| `assets/gif/*.gif` | GIFs for marketing posts |
| `assets/og/*.jpg` | Social previews (generated) |

Re-record the demos after editing `_tools/scenes.html`: `python _tools/record.py` (Chrome, Playwright, ffmpeg).

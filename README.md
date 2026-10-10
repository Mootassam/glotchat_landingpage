# GlotChat landing page

Static site (HTML + CSS + JS, no build step) — every button opens Telegram **@Capooo007** with a
ready-made message. English at `/`, 中文 at `/zh/` (Chinese browsers are sent there once; EN / 中文 switch in the header).

## Deploy on Vercel

1. Put this folder in a GitHub repo (or use the Vercel CLI: `npx vercel` inside this folder).
2. In Vercel: **Add New → Project → import the repo** → Framework preset **Other** → Deploy.
   No build command, no output directory needed.
3. **Settings → Domains** → add `glotchat.com` (and `www.glotchat.com`), then add the DNS records Vercel
   shows at Namecheap (usually A `@` → `76.76.21.21`, CNAME `www` → `cname.vercel-dns.com`).
4. **Analytics** tab → *Enable Web Analytics*. Telegram clicks are tracked as the event
   `telegram_click` (with `place` = which button and `plan`), so you see what converts.

## SEO

- English page `/`, Chinese page `/zh/` (real Chinese HTML, not only JavaScript), linked with hreflang.
- Titles / descriptions target searches like "multiple WhatsApp accounts on PC", "WhatsApp translator".
- Structured data: Organization, WebSite, SoftwareApplication and FAQ (can appear in Google results).
- `sitemap.xml` + `robots.txt`.

**Domain** is set in `_tools/build.py` (`SITE = "https://glotchat.com"`). After changing it — or after
editing any text in `index.html` / `assets/js/main.js` — run:

```
python _tools/build.py
```

It rewrites the absolute URLs, the structured data, `zh/index.html`, `sitemap.xml` and `robots.txt`
(needs Chrome + Playwright). **Edit English text in `index.html` and Chinese text in `main.js`, never
`zh/index.html` directly** — it is generated.

After going live: add the site to **Google Search Console** (and **Bing Webmaster Tools**), verify the
domain, and submit `https://glotchat.com/sitemap.xml`.

## Edit prices / plans

In `index.html`, section `id="pricing"` (look for **EDIT PRICES HERE**): change the number in
`<b class="amt">` **and** in `data-price="…"` of the same plan's button. Chinese plan texts are in
`assets/js/main.js` (`pl1_…`, `pl2_…`, `pl3_…`).

## Change the Telegram username

`assets/js/main.js` → `var TG_USER = 'Capooo007';` and the `href="https://t.me/Capooo007"` links in
`index.html` (fallback when JavaScript is off), plus `assets/img/telegram-qr.svg`
(regenerate: `python -c "import segno; segno.make('https://t.me/NEWNAME').save('telegram-qr.svg', scale=8, border=2, dark='#0b1220')"`).

## Media

| File | Use |
|---|---|
| `assets/media/*-en.mp4`, `*-zh.mp4` | Demo videos on the page (English / Chinese agent) |
| `assets/media/*.webp` | Video posters |
| `assets/gif/*.gif` | **GIFs for marketing** — post them in Telegram groups, WhatsApp status, social media |
| `og.png` | Link preview image (1200 × 630) |

Scenes: `chat` (two-way translation), `voice` (voice note → text), `photo` (photo text → translation),
`accounts` (many accounts, notifications, Ctrl+K). Re-record after editing `_tools/scenes.html`:
`python _tools/record.py` (needs Chrome, Playwright and ffmpeg).

# Keren Or Farm — Adoption Page (English)

A fully translated English version of the [Keren Or Farm adoption page](https://www.kerenorfarm.com/adoption).

- All 33 rescued animals with individual clickable profile pages
- Original photos preserved (downloaded locally in `/images`)
- Perfect English translation of every story
- Premium typography: **Fraunces** (display serif) + **Inter** (body sans)
- Warm cream + terracotta palette befitting a farm sanctuary
- Fully responsive, no build step, pure static HTML/CSS/JS

## Structure

```
index.html            # Main adoption page
animals/<slug>.html   # 33 individual animal profile pages
images/               # All animal photos (originally from kerenorfarm.com)
style.css             # Global styles
reveal.js             # Scroll-reveal animations
build.py              # Regenerates all HTML from source_data.json + translations.json
translations.json     # English translations
source_data.json      # Original Hebrew source data
```

## Rebuild

```
python3 build.py
```

## Deploy

Serve statically from any host (GitHub Pages, Netlify, etc.).

## Credit

All original content, animal stories, and photographs belong to [Keren Or Farm](https://www.kerenorfarm.com/).

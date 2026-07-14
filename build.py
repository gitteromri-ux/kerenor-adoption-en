#!/usr/bin/env python3
"""Build the Kerenor Farm English adoption site from source data + translations."""
import json, os, re, urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent
SRC = json.loads((ROOT / "source_data.json").read_text(encoding="utf-8"))
T = json.loads((ROOT / "translations.json").read_text(encoding="utf-8"))

PAGE = T["page"]
SPECIES = T["species"]
ANIMALS_T = T["animals"]

def slugify(name_en: str) -> str:
    s = name_en.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_&]+", "-", s).strip("-")
    return s

# Enrich animals with translations + slug + local image path
animals = []
for a in SRC["animals"]:
    heb = a["name"]
    if heb not in ANIMALS_T:
        raise SystemExit(f"Missing translation for {heb}")
    tr = ANIMALS_T[heb]
    slug = slugify(tr["name"])
    ext = ".png" if ".png" in a["photo_url"] else ".jpg"
    animals.append({
        "hebrew_name": heb,
        "name": tr["name"],
        "species": SPECIES.get(a["species"], a["species"]),
        "tagline": tr["tagline"],
        "bio": tr["bio"],
        "photo_url": f"images/{slug}{ext}",
        "photo_url_animal": f"../images/{slug}{ext}",
        "slug": slug,
    })

# Ensure unique slugs
slugs = [a["slug"] for a in animals]
assert len(slugs) == len(set(slugs)), f"Duplicate slugs: {slugs}"

BASE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_path}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='45' fill='%23c96f3f'/%3E%3Cpath d='M35 55c0-8 6-14 15-14s15 6 15 14c0 6-4 10-8 12l-7-3-7 3c-4-2-8-6-8-12z' fill='%23fdf8f1'/%3E%3Ccircle cx='42' cy='42' r='3' fill='%23fdf8f1'/%3E%3Ccircle cx='58' cy='42' r='3' fill='%23fdf8f1'/%3E%3C/svg%3E">
</head>"""

NAV = """<header class="site-header">
  <a href="{home}" class="brand" aria-label="Keren Or Farm">
    <svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true">
      <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="1.5"/>
      <path d="M14 28c0-6 4-10 10-10s10 4 10 10c0 4-3 7-6 8l-4-2-4 2c-3-1-6-4-6-8z" fill="currentColor"/>
      <circle cx="20" cy="24" r="1.6" fill="var(--cream)"/>
      <circle cx="28" cy="24" r="1.6" fill="var(--cream)"/>
    </svg>
    <span class="brand-name"><span class="brand-name-1">Keren Or</span><span class="brand-name-2">Farm</span></span>
  </a>
  <nav class="site-nav">
    <a href="{home}#residents">Residents</a>
    <a href="{home}#how">How it works</a>
    <a href="{home}#packages">Packages</a>
    <a href="{home}#contact">Contact</a>
  </nav>
  <a href="{home}#packages" class="nav-cta">Adopt</a>
</header>"""

FOOTER = """<footer class="site-footer" id="contact">
  <div class="footer-inner">
    <div class="footer-brand">
      <svg viewBox="0 0 48 48" class="brand-mark" aria-hidden="true">
        <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="1.5"/>
        <path d="M14 28c0-6 4-10 10-10s10 4 10 10c0 4-3 7-6 8l-4-2-4 2c-3-1-6-4-6-8z" fill="currentColor"/>
        <circle cx="20" cy="24" r="1.6" fill="var(--cream)"/>
        <circle cx="28" cy="24" r="1.6" fill="var(--cream)"/>
      </svg>
      <span>Keren Or Farm</span>
    </div>
    <p class="footer-tagline">A safe home for animals rescued from neglect, abuse, and industry.</p>
    <div class="footer-contact">
      <div><span class="label">Location</span><span>Keren Or Farm — Beit Berl</span></div>
      <div><span class="label">Email</span><a href="mailto:info@kerenorfarm.com">info@kerenorfarm.com</a></div>
      <div><span class="label">WhatsApp</span><a href="https://wa.me/972549033445">054-903-3445</a></div>
    </div>
    <p class="footer-legal">Keren Or is a registered nonprofit with Section 46 tax-deductible status. © Keren Or Farm.</p>
  </div>
</footer>"""

CSS = r"""
:root {
  --cream: #fdf8f1;
  --cream-warm: #f5ecdc;
  --paper: #faf3e6;
  --ink: #1f1a15;
  --ink-soft: #4a4038;
  --muted: #7a6e63;
  --line: #e6d9c1;
  --terracotta: #c96f3f;
  --terracotta-deep: #a3542b;
  --olive: #6a7043;
  --sage: #8b9268;
  --sunlight: #e9b455;
  --shadow-sm: 0 1px 2px rgba(31, 26, 21, .06), 0 2px 8px rgba(31, 26, 21, .04);
  --shadow-md: 0 6px 20px rgba(31, 26, 21, .08), 0 2px 6px rgba(31, 26, 21, .05);
  --shadow-lg: 0 20px 50px rgba(31, 26, 21, .12), 0 6px 16px rgba(31, 26, 21, .06);
  --radius-sm: 6px;
  --radius: 14px;
  --radius-lg: 24px;
  --max: 1240px;
}

*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
  color: var(--ink);
  background: var(--cream);
  font-size: 17px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
img { max-width: 100%; display: block; }
a { color: var(--terracotta-deep); text-decoration: none; transition: color .2s ease; }
a:hover { color: var(--terracotta); }

h1, h2, h3, h4 {
  font-family: 'Fraunces', 'Times New Roman', serif;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.1;
  letter-spacing: -0.01em;
  margin: 0;
  font-variation-settings: "opsz" 40;
}
h1 { font-size: clamp(2.4rem, 5.5vw, 4.5rem); font-weight: 400; letter-spacing: -0.025em; }
h2 { font-size: clamp(1.8rem, 3.5vw, 2.75rem); }
h3 { font-size: 1.3rem; font-weight: 500; }
p { margin: 0 0 1em; color: var(--ink-soft); }

.container { max-width: var(--max); margin: 0 auto; padding: 0 24px; }

/* ---------- Header ---------- */
.site-header {
  position: sticky; top: 0; z-index: 50;
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 40px;
  background: rgba(253, 248, 241, 0.85);
  backdrop-filter: saturate(160%) blur(12px);
  -webkit-backdrop-filter: saturate(160%) blur(12px);
  border-bottom: 1px solid rgba(230, 217, 193, 0.6);
}
.brand { display: flex; align-items: center; gap: 12px; color: var(--terracotta-deep); }
.brand-mark { width: 40px; height: 40px; color: var(--terracotta); flex-shrink: 0; }
.brand-name { display: flex; flex-direction: column; line-height: 1; }
.brand-name-1 { font-family: 'Fraunces', serif; font-size: 1.15rem; font-weight: 500; color: var(--ink); }
.brand-name-2 { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.22em; color: var(--muted); margin-top: 3px; }
.site-nav { display: flex; gap: 34px; }
.site-nav a { color: var(--ink-soft); font-size: 0.95rem; font-weight: 500; }
.site-nav a:hover { color: var(--terracotta); }
.nav-cta {
  padding: 10px 22px; background: var(--terracotta); color: var(--cream) !important;
  border-radius: 999px; font-size: 0.9rem; font-weight: 600; letter-spacing: 0.02em;
  transition: all .2s ease;
}
.nav-cta:hover { background: var(--terracotta-deep); transform: translateY(-1px); }

@media (max-width: 780px) {
  .site-header { padding: 14px 20px; }
  .site-nav { display: none; }
}

/* ---------- Hero ---------- */
.hero {
  padding: 90px 24px 70px;
  text-align: center;
  background: radial-gradient(ellipse at top, var(--paper), var(--cream));
  border-bottom: 1px solid var(--line);
  position: relative; overflow: hidden;
}
.hero::before, .hero::after {
  content: ''; position: absolute; width: 260px; height: 260px; border-radius: 50%;
  filter: blur(80px); opacity: .4; z-index: 0;
}
.hero::before { background: var(--sunlight); top: -40px; left: 10%; }
.hero::after { background: var(--sage); bottom: -40px; right: 8%; }
.hero-inner { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; }
.hero-kicker {
  display: inline-block;
  font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.28em;
  color: var(--terracotta-deep); font-weight: 600;
  padding: 8px 20px; border: 1px solid var(--terracotta); border-radius: 999px;
  margin-bottom: 28px;
}
.hero h1 { margin-bottom: 24px; font-style: italic; font-weight: 300; }
.hero h1 em { font-style: normal; color: var(--terracotta-deep); font-family: 'Fraunces', serif; }
.hero-sub { font-size: clamp(1.05rem, 1.6vw, 1.25rem); color: var(--ink-soft); max-width: 660px; margin: 0 auto 36px; line-height: 1.6; }
.hero-actions { display: inline-flex; gap: 14px; flex-wrap: wrap; justify-content: center; }
.btn {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 14px 30px; border-radius: 999px;
  font-family: 'Inter', sans-serif; font-size: 0.98rem; font-weight: 600; letter-spacing: 0.01em;
  cursor: pointer; border: 1px solid transparent;
  transition: transform .2s ease, box-shadow .25s ease, background .25s ease;
}
.btn-primary { background: var(--terracotta); color: var(--cream); box-shadow: var(--shadow-md); }
.btn-primary:hover { background: var(--terracotta-deep); color: var(--cream); transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.btn-ghost { background: transparent; color: var(--ink); border-color: var(--line); }
.btn-ghost:hover { border-color: var(--terracotta); color: var(--terracotta-deep); }

/* ---------- Sections ---------- */
section { padding: 90px 0; }
.section-eyebrow {
  text-align: center; font-size: 0.78rem; text-transform: uppercase;
  letter-spacing: 0.32em; color: var(--terracotta-deep); font-weight: 600;
  margin-bottom: 14px;
}
.section-title { text-align: center; margin-bottom: 16px; font-weight: 400; }
.section-title em { font-style: italic; color: var(--terracotta-deep); font-family: 'Fraunces', serif; }
.section-sub { text-align: center; max-width: 620px; margin: 0 auto 60px; font-size: 1.08rem; color: var(--muted); }

/* ---------- How It Works ---------- */
.how { background: var(--cream-warm); border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.how-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
.how-step {
  padding: 32px; background: var(--cream); border-radius: var(--radius);
  border: 1px solid var(--line); position: relative;
  transition: transform .3s ease, box-shadow .3s ease;
}
.how-step:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.how-step-num {
  font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 300;
  color: var(--terracotta); line-height: 1; margin-bottom: 16px;
  font-style: italic;
}
.how-step h3 { margin-bottom: 10px; font-size: 1.2rem; }
.how-step p { margin: 0; font-size: 0.98rem; }
@media (max-width: 800px) { .how-grid { grid-template-columns: 1fr; } }

/* ---------- Residents grid ---------- */
.residents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 36px 28px;
}
.animal-card {
  background: var(--cream);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--line);
  display: flex; flex-direction: column;
  transition: transform .35s cubic-bezier(.2,.7,.2,1), box-shadow .35s ease;
  color: inherit;
}
.animal-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  color: inherit;
}
.animal-photo { position: relative; overflow: hidden; aspect-ratio: 4 / 3.4; background: var(--cream-warm); }
.animal-photo img {
  width: 100%; height: 100%; object-fit: cover; object-position: center;
  transition: transform .8s cubic-bezier(.2,.7,.2,1);
}
.animal-card:hover .animal-photo img { transform: scale(1.06); }
.animal-species-tag {
  position: absolute; top: 14px; left: 14px;
  padding: 6px 12px; background: rgba(253, 248, 241, 0.95);
  color: var(--terracotta-deep);
  font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em;
  font-weight: 600; border-radius: 999px;
  backdrop-filter: blur(8px);
}
.animal-body { padding: 24px 26px 28px; flex: 1; display: flex; flex-direction: column; }
.animal-name {
  font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 500;
  color: var(--ink); margin-bottom: 10px; line-height: 1.15;
}
.animal-tagline {
  font-size: 0.95rem; color: var(--ink-soft); line-height: 1.55;
  flex: 1; margin-bottom: 20px;
  display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical;
  overflow: hidden;
}
.animal-cta {
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 0.9rem; font-weight: 600; color: var(--terracotta-deep);
  letter-spacing: 0.02em;
}
.animal-cta::after {
  content: '→'; transition: transform .3s ease; font-size: 1.1rem;
}
.animal-card:hover .animal-cta::after { transform: translateX(6px); }

/* ---------- Packages ---------- */
.packages { background: var(--ink); color: var(--cream); }
.packages .section-eyebrow { color: var(--sunlight); }
.packages .section-title { color: var(--cream); }
.packages .section-title em { color: var(--sunlight); }
.packages .section-sub { color: rgba(253, 248, 241, .7); }
.packages-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.pkg {
  padding: 36px 26px; text-align: center;
  background: rgba(253, 248, 241, .04);
  border: 1px solid rgba(253, 248, 241, .12);
  border-radius: var(--radius);
  transition: all .3s ease;
}
.pkg:hover { background: rgba(253, 248, 241, .07); transform: translateY(-4px); border-color: var(--sunlight); }
.pkg-name { font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--sunlight); margin-bottom: 20px; font-weight: 600; }
.pkg-price { font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 300; color: var(--cream); margin-bottom: 24px; line-height: 1; }
.pkg-price small { font-size: 1rem; color: rgba(253, 248, 241, .5); font-family: 'Inter', sans-serif; display: block; margin-top: 8px; letter-spacing: 0.1em; text-transform: uppercase; }
.pkg .btn {
  background: var(--terracotta); color: var(--cream); width: 100%; justify-content: center;
}
.pkg .btn:hover { background: var(--sunlight); color: var(--ink); }
@media (max-width: 900px) { .packages-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .packages-grid { grid-template-columns: 1fr; } }

/* ---------- Tax note ---------- */
.tax { background: var(--cream-warm); }
.tax-inner {
  max-width: 780px; margin: 0 auto; text-align: center;
  padding: 40px 30px;
  background: var(--cream);
  border-radius: var(--radius);
  border: 1px solid var(--line);
}
.tax-inner h3 { margin-bottom: 14px; font-family: 'Fraunces', serif; font-size: 1.5rem; }
.tax-inner p { margin: 0; font-size: 0.98rem; color: var(--ink-soft); }

/* ---------- Footer ---------- */
.site-footer {
  background: var(--ink); color: rgba(253, 248, 241, .75);
  padding: 70px 24px 40px;
}
.footer-inner { max-width: var(--max); margin: 0 auto; text-align: center; }
.footer-brand { display: inline-flex; align-items: center; gap: 12px; color: var(--sunlight); font-family: 'Fraunces', serif; font-size: 1.4rem; margin-bottom: 8px; }
.footer-brand .brand-mark { width: 34px; height: 34px; color: var(--sunlight); }
.footer-tagline { color: rgba(253, 248, 241, .65); font-size: 1rem; margin-bottom: 40px; max-width: 500px; margin-left: auto; margin-right: auto; }
.footer-contact {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px;
  max-width: 700px; margin: 0 auto 40px; padding: 30px 0;
  border-top: 1px solid rgba(253, 248, 241, .12);
  border-bottom: 1px solid rgba(253, 248, 241, .12);
}
.footer-contact > div { display: flex; flex-direction: column; gap: 6px; }
.footer-contact .label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.22em; color: rgba(253, 248, 241, .45); }
.footer-contact a, .footer-contact span:not(.label) { color: var(--cream); font-size: 0.95rem; }
.footer-contact a:hover { color: var(--sunlight); }
.footer-legal { font-size: 0.82rem; color: rgba(253, 248, 241, .45); margin: 0; }
@media (max-width: 700px) { .footer-contact { grid-template-columns: 1fr; } }

/* ---------- Individual animal page ---------- */
.animal-hero {
  padding: 60px 24px 30px;
  background: var(--cream-warm);
  border-bottom: 1px solid var(--line);
}
.back-link {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 0.9rem; font-weight: 500; color: var(--muted);
  margin-bottom: 20px;
}
.back-link:hover { color: var(--terracotta-deep); }

.profile {
  display: grid; grid-template-columns: 1fr 1fr; gap: 60px;
  max-width: var(--max); margin: 0 auto; padding: 60px 24px;
  align-items: start;
}
.profile-photo {
  position: sticky; top: 100px;
  border-radius: var(--radius-lg); overflow: hidden;
  aspect-ratio: 4/5; background: var(--cream-warm);
  box-shadow: var(--shadow-lg);
}
.profile-photo img { width: 100%; height: 100%; object-fit: cover; }
.profile-content { padding-top: 10px; }
.profile-species {
  display: inline-block;
  font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.24em;
  color: var(--terracotta-deep); font-weight: 600;
  padding: 6px 16px; border: 1px solid var(--terracotta); border-radius: 999px;
  margin-bottom: 22px;
}
.profile-content h1 {
  font-family: 'Fraunces', serif; font-size: clamp(3rem, 5vw, 4.5rem);
  color: var(--ink); margin-bottom: 8px; font-weight: 400;
  font-style: italic; letter-spacing: -0.02em;
}
.profile-meta { font-size: 0.95rem; color: var(--muted); margin-bottom: 34px; letter-spacing: 0.06em; }
.profile-meta .hebrew { font-family: 'Fraunces', serif; font-style: italic; font-size: 1.05rem; color: var(--ink-soft); }
.profile-bio { font-size: 1.1rem; line-height: 1.75; color: var(--ink-soft); margin-bottom: 36px; }
.profile-bio::first-letter {
  font-family: 'Fraunces', serif; float: left; font-size: 4.2rem;
  line-height: 0.9; padding: 8px 12px 0 0; color: var(--terracotta-deep);
  font-weight: 400; font-style: italic;
}
.profile-actions { display: flex; gap: 14px; flex-wrap: wrap; }
@media (max-width: 900px) {
  .profile { grid-template-columns: 1fr; gap: 40px; padding: 40px 20px; }
  .profile-photo { position: static; aspect-ratio: 4/3; }
}

/* Related residents strip */
.related { padding: 80px 0; background: var(--cream-warm); border-top: 1px solid var(--line); }
.related h2 { text-align: center; margin-bottom: 40px; }
.related-strip {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
  max-width: var(--max); margin: 0 auto;
}
.related .animal-card { background: var(--cream); }
@media (max-width: 900px) { .related-strip { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .related-strip { grid-template-columns: 1fr; } }

/* ---------- Reveal animation ---------- */
.reveal { opacity: 0; transform: translateY(24px); transition: opacity .8s ease, transform .8s cubic-bezier(.2,.7,.2,1); }
.reveal.visible { opacity: 1; transform: translateY(0); }
"""

# ------------ Build homepage ------------

def render_animal_card(a, home_prefix=""):
    img_src = (home_prefix + a['photo_url']) if home_prefix else a['photo_url']
    return f"""<a class="animal-card reveal" href="{home_prefix}animals/{a['slug']}.html">
  <div class="animal-photo">
    <img src="{img_src}" alt="{a['name']}, {a['species']} rescued by Keren Or Farm" loading="lazy">
    <span class="animal-species-tag">{a['species']}</span>
  </div>
  <div class="animal-body">
    <h3 class="animal-name">{a['name']}</h3>
    <p class="animal-tagline">{a['tagline']}</p>
    <span class="animal-cta">Read full story</span>
  </div>
</a>"""

def render_home():
    cards = "\n".join(render_animal_card(a) for a in animals)
    packages_html = "\n".join(
        f"""<div class="pkg reveal">
          <div class="pkg-name">{p['name']}</div>
          <div class="pkg-price">{p['price']}<small>One-time donation</small></div>
          <a href="{p['url']}" target="_blank" rel="noopener" class="btn btn-primary">Sponsor now</a>
        </div>"""
        for p in PAGE["packages"]
    )
    steps_html = "\n".join(
        f"""<div class="how-step reveal">
          <div class="how-step-num">{s['step']}</div>
          <h3>{s['title']}</h3>
          <p>{s['text']}</p>
        </div>"""
        for s in PAGE["how_it_works"]
    )

    head = BASE_HEAD.format(
        title="Adopt a Resident · Keren Or Farm",
        desc=PAGE["hero_subtitle"],
        css_path="style.css",
    )
    nav = NAV.format(home="index.html")

    return f"""{head}
<body>
{nav}

<section class="hero">
  <div class="hero-inner">
    <span class="hero-kicker">{PAGE['hero_kicker']}</span>
    <h1>Have you always dreamed of raising a dog, a cat,<br>a goat, a donkey — or perhaps <em>even a pig</em>?</h1>
    <p class="hero-sub">{PAGE['hero_subtitle']}</p>
    <div class="hero-actions">
      <a href="#residents" class="btn btn-primary">Meet the residents</a>
      <a href="#packages" class="btn btn-ghost">See packages</a>
    </div>
  </div>
</section>

<section class="how" id="how">
  <div class="container">
    <div class="section-eyebrow">{PAGE['how_it_works_title']}</div>
    <h2 class="section-title">Three simple <em>steps</em></h2>
    <p class="section-sub">A meaningful way to support an animal in need — from anywhere in the world.</p>
    <div class="how-grid">
      {steps_html}
    </div>
  </div>
</section>

<section id="residents">
  <div class="container">
    <div class="section-eyebrow">{PAGE['section_title']}</div>
    <h2 class="section-title">Every animal has a <em>story</em></h2>
    <p class="section-sub">{PAGE['section_subtitle']}</p>
    <div class="residents-grid">
      {cards}
    </div>
  </div>
</section>

<section class="packages" id="packages">
  <div class="container">
    <div class="section-eyebrow">{PAGE['packages_title']}</div>
    <h2 class="section-title">Choose your <em>package</em></h2>
    <p class="section-sub">Every contribution funds food, veterinary care, rehabilitation, and lifelong shelter.</p>
    <div class="packages-grid">
      {packages_html}
    </div>
  </div>
</section>

<section class="tax">
  <div class="container">
    <div class="tax-inner reveal">
      <h3>{PAGE['tax_note_title']}</h3>
      <p>{PAGE['tax_note']}</p>
    </div>
  </div>
</section>

{FOOTER}

<script src="reveal.js"></script>
</body>
</html>"""

def render_animal_page(a, idx):
    # pick 4 others as related (wrap-around)
    others = [x for x in animals if x["slug"] != a["slug"]]
    related = []
    for i in range(4):
        related.append(others[(idx + i) % len(others)])
    related_html = "\n".join(render_animal_card(x, home_prefix="../") for x in related)

    head = BASE_HEAD.format(
        title=f"{a['name']} · Keren Or Farm",
        desc=a["tagline"],
        css_path="../style.css",
    )
    nav = NAV.format(home="../index.html")

    return f"""{head}
<body>
{nav}

<section class="animal-hero">
  <div class="container">
    <a href="../index.html#residents" class="back-link">← Back to all residents</a>
  </div>
</section>

<section class="profile">
  <div class="profile-photo reveal">
    <img src="{a['photo_url_animal']}" alt="{a['name']}, {a['species']} rescued by Keren Or Farm">
  </div>
  <div class="profile-content">
    <span class="profile-species">{a['species']}</span>
    <h1>{a['name']}</h1>
    <p class="profile-meta">Also known as <span class="hebrew">{a['hebrew_name']}</span></p>
    <p class="profile-bio">{a['bio']}</p>
    <div class="profile-actions">
      <a href="../index.html#packages" class="btn btn-primary">Sponsor {a['name']}</a>
      <a href="../index.html#residents" class="btn btn-ghost">See all residents</a>
    </div>
  </div>
</section>

<section class="related">
  <div class="container">
    <h2 class="section-title">Meet other <em>residents</em></h2>
    <div class="related-strip">
      {related_html}
    </div>
  </div>
</section>

{FOOTER}

<script src="../reveal.js"></script>
</body>
</html>"""

REVEAL_JS = """document.addEventListener('DOMContentLoaded', () => {
  const els = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  els.forEach(el => io.observe(el));
});
"""

# Write files
(ROOT / "style.css").write_text(CSS, encoding="utf-8")
(ROOT / "reveal.js").write_text(REVEAL_JS, encoding="utf-8")
(ROOT / "index.html").write_text(render_home(), encoding="utf-8")

anim_dir = ROOT / "animals"
anim_dir.mkdir(exist_ok=True)
# clear any stale files
for f in anim_dir.glob("*.html"):
    f.unlink()

for i, a in enumerate(animals):
    (anim_dir / f"{a['slug']}.html").write_text(render_animal_page(a, i), encoding="utf-8")

print(f"Built {len(animals)} animal pages + index.html")
print("Slugs:")
for a in animals:
    print(f"  {a['slug']:<25} {a['name']:<20} ({a['species']})")

#!/usr/bin/env python3
"""Build the Kerenor Farm English adoption site — exact replica of the Hebrew original, in English."""
import json, os, re
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

# Build animal list with local images
animals = []
for a in SRC["animals"]:
    heb = a["name"]
    tr = ANIMALS_T[heb]
    slug = slugify(tr["name"])
    ext = ".png" if ".png" in a["photo_url"] else ".jpg"
    animals.append({
        "hebrew_name": heb,
        "name": tr["name"],
        "species": SPECIES.get(a["species"], a["species"]),
        "tagline": tr["tagline"],
        "bio": tr["bio"],
        "photo": f"images/{slug}{ext}",
        "photo_from_animal": f"../images/{slug}{ext}",
        "slug": slug,
    })

CSS = r"""
/* ================= EXACT REPLICA — Kerenor Farm adoption page (English) ================= */
:root {
  --teal: #06A2CF;
  --teal-dark: #0489AE;
  --teal-light: #E6F5FA;
  --navy: #045184;
  --navy-dark: #023963;
  --orange: #F5A623;
  --orange-dark: #E08C00;
  --gold: #F5C445;
  --gold-bg: #F7B733;
  --bg: #FFFFFF;
  --text: #2A3541;
  --text-soft: #4a5563;
  --muted: #6f7a86;
  --line: #E5E9EF;
  --card-bg: #FFFFFF;
  --card-shadow: 0 4px 14px rgba(4, 81, 132, 0.08);
  --card-shadow-hover: 0 12px 30px rgba(4, 81, 132, 0.15);
}

*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: 'Nunito', 'Proxima Nova', 'Helvetica Neue', Arial, sans-serif;
  color: var(--text);
  background: var(--bg);
  font-size: 17px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
img { max-width: 100%; display: block; }
a { color: var(--teal); text-decoration: none; transition: color .2s; }
a:hover { color: var(--teal-dark); }

h1, h2, h3, h4 {
  font-family: 'Nunito', 'Proxima Nova', sans-serif;
  font-weight: 800;
  color: var(--navy);
  line-height: 1.15;
  margin: 0;
}
h1 { font-size: clamp(1.9rem, 4vw, 2.9rem); }
h2 { font-size: clamp(1.7rem, 3.2vw, 2.4rem); }
h3 { font-size: 1.35rem; font-weight: 700; }
p { margin: 0 0 1em; color: var(--text-soft); }

.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

/* ---------- Top strip ---------- */
.top-strip {
  background: #fff;
  border-bottom: 1px solid var(--line);
  padding: 10px 24px;
}
.top-strip-inner {
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
}
.lang-btn {
  padding: 6px 14px; font-size: 0.82rem; font-weight: 700;
  border: 1px solid var(--line); background: #fff; border-radius: 20px;
  color: var(--navy); cursor: pointer;
}
.top-ctas { display: flex; gap: 10px; }
.top-cta {
  padding: 8px 20px; font-size: 0.9rem; font-weight: 700;
  background: var(--teal); color: #fff !important; border-radius: 22px;
  transition: background .2s, transform .2s;
}
.top-cta:hover { background: var(--teal-dark); transform: translateY(-1px); }
.top-cta.secondary { background: var(--orange); }
.top-cta.secondary:hover { background: var(--orange-dark); }

/* ---------- Logo band ---------- */
.logo-band {
  padding: 20px 24px 8px;
  text-align: center;
  background: #fff;
}
.logo-band img { display: inline-block; max-width: 170px; height: auto; }

/* ---------- Main nav ---------- */
.main-nav {
  background: #fff;
  border-bottom: 1px solid var(--line);
  position: sticky; top: 0; z-index: 40;
  box-shadow: 0 1px 4px rgba(0,0,0,.03);
}
.main-nav-inner {
  max-width: 1200px; margin: 0 auto; padding: 6px 24px;
  display: flex; align-items: center; justify-content: center;
  flex-wrap: wrap; gap: 4px;
}
.nav-item {
  padding: 12px 18px; font-size: 0.95rem; font-weight: 700;
  color: var(--navy); border-radius: 22px;
  transition: all .2s;
}
.nav-item:hover { background: var(--teal-light); color: var(--teal-dark); }
.nav-item.active {
  background: var(--teal); color: #fff !important;
  position: relative;
}
.nav-item.active::after {
  content: ''; position: absolute; bottom: -6px; left: 50%;
  transform: translateX(-50%); width: 0; height: 0;
  border-left: 6px solid transparent; border-right: 6px solid transparent;
  border-top: 6px solid var(--teal);
}
@media (max-width: 900px) {
  .main-nav-inner { justify-content: flex-start; overflow-x: auto; flex-wrap: nowrap; padding: 6px 16px; }
  .nav-item { flex-shrink: 0; padding: 10px 14px; font-size: 0.85rem; }
}

/* ---------- Hero ---------- */
.hero {
  padding: 44px 24px 40px;
  text-align: center;
  background: #fff;
}
.hero-video-wrap {
  max-width: 720px; margin: 0 auto 32px;
  padding: 8px; background: var(--gold);
  border-radius: 12px;
  box-shadow: 0 10px 32px rgba(245, 166, 35, 0.25);
}
.hero-video {
  position: relative; padding-top: 56.25%;
  border-radius: 6px; overflow: hidden; background: #000;
}
.hero-video iframe {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  border: 0;
}
.hero h1 {
  max-width: 900px; margin: 0 auto 16px;
  font-weight: 900; color: var(--navy);
}
.hero-sub {
  font-size: clamp(1.05rem, 1.6vw, 1.25rem);
  color: var(--navy); font-weight: 600;
  max-width: 700px; margin: 0 auto 28px;
}
.tax-note {
  max-width: 780px; margin: 24px auto 0;
  padding: 18px 26px;
  background: #FFF8E7; border: 1px dashed var(--gold);
  border-radius: 14px;
  display: flex; align-items: center; gap: 16px; text-align: left;
}
.tax-note .icon { font-size: 2.2rem; flex-shrink: 0; }
.tax-note p { margin: 0; font-size: 0.94rem; color: var(--text-soft); }
.tax-note strong { color: var(--navy); }

/* ---------- Sections ---------- */
section { padding: 70px 0; }
.section-title { text-align: center; margin-bottom: 12px; color: var(--navy); font-weight: 900; }
.section-title span { color: var(--teal); }
.section-intro { text-align: center; color: var(--text-soft); font-size: 1.05rem; max-width: 640px; margin: 0 auto 44px; }

/* ---------- How it works ---------- */
.how { background: #fff; }
.how-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; align-items: start; }
.how-card { text-align: center; }
.how-illust {
  width: 240px; height: 240px; margin: 0 auto 20px;
  background: var(--teal-light);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  position: relative;
}
.how-illust::before, .how-illust::after {
  content: '✦'; position: absolute; color: var(--gold); font-size: 1.4rem;
}
.how-illust::before { top: 10px; right: 20px; }
.how-illust::after { bottom: 20px; left: 20px; font-size: 1rem; }
.how-illust img { width: 82%; height: 82%; object-fit: contain; }
.how-step {
  font-size: 1.15rem; font-weight: 800; color: var(--navy);
  max-width: 260px; margin: 0 auto; line-height: 1.35;
}
.how-step .num { color: var(--teal); font-size: 1.3rem; margin-right: 6px; }
@media (max-width: 850px) { .how-grid { grid-template-columns: 1fr; gap: 30px; } }

/* ---------- Packages ---------- */
.packages { background: #FAFCFE; }
.packages-grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 28px;
  max-width: 1000px; margin: 0 auto;
}
.pkg {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--card-shadow);
  display: flex; flex-direction: column;
  transition: transform .3s, box-shadow .3s;
}
.pkg:hover { transform: translateY(-4px); box-shadow: var(--card-shadow-hover); }
.pkg-header {
  background: var(--teal); color: #fff;
  padding: 16px 24px; text-align: center;
  font-weight: 800; font-size: 1.3rem;
  letter-spacing: 0.01em;
  position: relative;
}
.pkg.vip .pkg-header { background: linear-gradient(135deg, var(--teal) 0%, var(--navy) 100%); }
.pkg-body { padding: 24px 26px 26px; flex: 1; display: flex; flex-direction: column; }
.pkg-includes-title {
  color: var(--orange); font-weight: 800; font-size: 1.05rem;
  margin-bottom: 12px;
}
.pkg-list { list-style: none; padding: 0; margin: 0 0 16px; }
.pkg-list li {
  padding: 8px 0 8px 26px; position: relative;
  font-size: 0.96rem; color: var(--text); line-height: 1.5;
  border-bottom: 1px dashed #E7EBF0;
}
.pkg-list li:last-child { border-bottom: 0; }
.pkg-list li::before {
  content: '✓'; position: absolute; left: 0; top: 8px;
  color: var(--teal); font-weight: 900; font-size: 1.05rem;
}
.pkg-footnote {
  font-size: 0.82rem; color: var(--muted); font-style: italic;
  margin: 8px 0 18px;
}
.pkg-price {
  text-align: center; font-size: 1.5rem; font-weight: 900;
  color: var(--orange); margin: 12px 0 18px;
}
.pkg-price small { font-size: 0.9rem; color: var(--muted); font-weight: 500; font-style: italic; display: block; margin-top: 4px; }
.pkg-cta {
  display: block; width: 100%; text-align: center;
  padding: 14px; font-size: 1rem; font-weight: 800;
  border: 2px solid var(--teal); border-radius: 30px;
  color: var(--teal) !important; background: #fff;
  transition: all .25s;
}
.pkg-cta:hover { background: var(--teal); color: #fff !important; }
.pkg.vip .pkg-cta { border-color: var(--orange); color: var(--orange) !important; }
.pkg.vip .pkg-cta:hover { background: var(--orange); color: #fff !important; }
.pkg-vip-bonuses {
  display: flex; gap: 12px; margin-top: 14px; justify-content: center;
  flex-wrap: wrap;
}
.pkg-vip-bonuses img { width: 68px; height: 68px; object-fit: contain; }
@media (max-width: 780px) { .packages-grid { grid-template-columns: 1fr; } }

/* ---------- Residents grid ---------- */
.residents { background: #fff; }
.residents-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px;
  max-width: 1180px; margin: 0 auto;
}
.animal-card {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  transition: transform .3s, box-shadow .3s;
  color: inherit;
  display: block;
}
.animal-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--card-shadow-hover);
  color: inherit;
}
.animal-photo { position: relative; aspect-ratio: 3 / 2; overflow: hidden; background: #f0f4f8; }
.animal-photo img {
  width: 100%; height: 100%; object-fit: cover;
  transition: transform .6s ease;
}
.animal-card:hover .animal-photo img { transform: scale(1.05); }
.animal-photo-overlay {
  position: absolute; left: 0; right: 0; bottom: 0;
  background: linear-gradient(to top, rgba(4,81,132,0.85), rgba(4,81,132,0));
  padding: 40px 16px 14px; text-align: center;
}
.animal-photo-overlay span {
  color: #fff; font-size: 0.95rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
}
.animal-body { padding: 18px 22px 22px; }
.animal-name {
  color: var(--teal); font-size: 1.5rem; font-weight: 900;
  margin: 0 0 8px; line-height: 1.15;
}
.animal-tagline {
  color: var(--text-soft); font-size: 0.94rem; line-height: 1.5;
  margin: 0;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  overflow: hidden;
}
@media (max-width: 900px) { .residents-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 580px) { .residents-grid { grid-template-columns: 1fr; } }

/* ---------- Footer ---------- */
.site-footer {
  background: var(--gold-bg);
  color: #fff;
  padding: 50px 24px 24px;
  margin-top: 40px;
}
.footer-inner {
  max-width: 1100px; margin: 0 auto;
  display: grid; grid-template-columns: 1fr 1fr; gap: 40px;
}
.footer-col h3 { color: #fff; font-size: 1.4rem; margin-bottom: 14px; font-weight: 900; }
.footer-col p, .footer-col a { color: #fff; }
.footer-col a { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; }
.footer-col a:hover { color: var(--navy); }
.footer-info p { margin: 4px 0; font-size: 1rem; }
.footer-info strong { display: block; font-weight: 800; margin-top: 10px; }
.footer-socials {
  display: flex; gap: 14px; margin-top: 6px;
}
.social-icon {
  width: 46px; height: 46px; border-radius: 50%;
  background: #fff; color: var(--gold-bg) !important;
  display: flex; align-items: center; justify-content: center;
  transition: transform .2s, background .2s;
}
.social-icon:hover { transform: translateY(-2px) scale(1.06); background: var(--navy); color: #fff !important; }
.social-icon svg { width: 22px; height: 22px; }
.footer-bottom {
  max-width: 1100px; margin: 34px auto 0;
  padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.35);
  display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 16px;
}
.footer-bottom-links { display: flex; gap: 20px; flex-wrap: wrap; }
.footer-bottom-links a { color: #fff; font-size: 0.9rem; text-decoration: none; }
.footer-bottom-links a:hover { text-decoration: underline; }
.footer-bottom .copy { color: rgba(255,255,255,.9); font-size: 0.88rem; }
@media (max-width: 700px) { .footer-inner { grid-template-columns: 1fr; } }

/* ---------- Individual animal page ---------- */
.animal-page-hero {
  background: var(--teal-light);
  padding: 24px 24px;
  border-bottom: 1px solid var(--line);
}
.back-link {
  color: var(--navy); font-weight: 700; font-size: 0.95rem;
  display: inline-flex; align-items: center; gap: 6px;
}
.back-link:hover { color: var(--teal); }

.profile {
  max-width: 1100px; margin: 0 auto;
  padding: 50px 24px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 50px;
  align-items: start;
}
.profile-photo {
  border-radius: 14px; overflow: hidden;
  box-shadow: var(--card-shadow-hover);
  aspect-ratio: 4/5; background: var(--teal-light);
  position: sticky; top: 100px;
}
.profile-photo img { width: 100%; height: 100%; object-fit: cover; }
.profile-content { padding-top: 4px; }
.profile-species {
  display: inline-block;
  background: var(--teal); color: #fff;
  padding: 5px 14px; border-radius: 16px;
  font-size: 0.78rem; font-weight: 800;
  text-transform: uppercase; letter-spacing: 0.1em;
  margin-bottom: 18px;
}
.profile-content h1 {
  color: var(--teal); font-size: clamp(2.4rem, 5vw, 3.6rem);
  margin-bottom: 6px; font-weight: 900;
}
.profile-meta { color: var(--muted); margin-bottom: 26px; font-size: 0.95rem; }
.profile-meta .hebrew { color: var(--navy); font-weight: 600; }
.profile-bio {
  font-size: 1.08rem; line-height: 1.75; color: var(--text);
  margin-bottom: 32px;
}
.profile-actions { display: flex; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 30px; border-radius: 30px;
  font-weight: 800; font-size: 1rem; transition: all .25s;
  cursor: pointer; border: 2px solid transparent;
}
.btn-primary { background: var(--teal); color: #fff !important; }
.btn-primary:hover { background: var(--teal-dark); transform: translateY(-2px); }
.btn-ghost { background: transparent; color: var(--teal) !important; border-color: var(--teal); }
.btn-ghost:hover { background: var(--teal); color: #fff !important; }
@media (max-width: 900px) {
  .profile { grid-template-columns: 1fr; padding: 30px 20px; }
  .profile-photo { position: static; aspect-ratio: 4/3; }
}

.related { background: #FAFCFE; padding: 60px 0; }
.related h2 { text-align: center; margin-bottom: 32px; }
.related .residents-grid { max-width: 1180px; }

/* Reveal */
.reveal { opacity: 0; transform: translateY(20px); transition: opacity .7s ease, transform .7s cubic-bezier(.2,.7,.2,1); }
.reveal.visible { opacity: 1; transform: translateY(0); }
"""

def render_nav(active_href="index.html", prefix=""):
    items = []
    for it in PAGE["nav"]:
        href = it["href"]
        # Relative links stay relative, external stay absolute
        if not href.startswith("http") and not href.startswith("#"):
            href = prefix + href
        is_active = it.get("active") and active_href == "index.html"
        cls = "nav-item active" if is_active else "nav-item"
        items.append(f'<a href="{href}" class="{cls}">{it["label"]}</a>')
    return f"""
<div class="top-strip">
  <div class="top-strip-inner">
    <button class="lang-btn" aria-label="Language">HE</button>
    <div class="top-ctas">
      <a href="https://www.kerenorfarm.com/donation" class="top-cta secondary">Donate to the Farm</a>
      <a href="{prefix}index.html" class="top-cta">Virtual Adoption</a>
    </div>
  </div>
</div>
<div class="logo-band">
  <a href="https://www.kerenorfarm.com/" aria-label="Keren Or Farm">
    <img src="{prefix}images/kerenor-logo.png" alt="Keren Or Farm">
  </a>
</div>
<nav class="main-nav">
  <div class="main-nav-inner">
    {''.join(items)}
  </div>
</nav>
"""

def render_footer():
    s = PAGE["social"]
    return f"""
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-col footer-info">
      <h3>{PAGE['footer_talk_title']}</h3>
      <p><strong>{PAGE['footer_farm_name']}</strong></p>
      <p>Email: <a href="mailto:{PAGE['footer_email']}">{PAGE['footer_email']}</a></p>
      <p>WhatsApp: <a href="{s['whatsapp']}">{PAGE['footer_whatsapp']}</a></p>
    </div>
    <div class="footer-col">
      <h3>{PAGE['footer_follow_title']}</h3>
      <div class="footer-socials">
        <a href="{s['whatsapp']}" class="social-icon" aria-label="WhatsApp" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.7-.9-2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.3-.7.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2.05-.4 0-.5-.1-.1-.7-1.7-1-2.3-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.6 1.4 5.1L2 22l5-1.3c1.5.8 3.2 1.2 5 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2z"/></svg>
        </a>
        <a href="{s['facebook']}" class="social-icon" aria-label="Facebook" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 20V13h2.5l.5-3H13V8c0-.9.2-1.5 1.5-1.5H16V3.9C15.7 3.9 14.8 3.8 13.8 3.8c-2 0-3.3 1.2-3.3 3.5v2.7H8v3h2.5v7H13z"/></svg>
        </a>
        <a href="{s['youtube']}" class="social-icon" aria-label="YouTube" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.6 7.2c-.2-.9-.9-1.6-1.8-1.8C18.1 5 12 5 12 5s-6.1 0-7.8.4c-.9.2-1.6.9-1.8 1.8C2 8.9 2 12 2 12s0 3.1.4 4.8c.2.9.9 1.6 1.8 1.8C5.9 19 12 19 12 19s6.1 0 7.8-.4c.9-.2 1.6-.9 1.8-1.8.4-1.7.4-4.8.4-4.8s0-3.1-.4-4.8zM10 15V9l5 3-5 3z"/></svg>
        </a>
        <a href="{s['instagram']}" class="social-icon" aria-label="Instagram" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.3 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.2.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.3 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.2.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.3-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.3-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2M12 0C8.7 0 8.3 0 7.1.1 5.8.1 5 .3 4.2.6c-.8.3-1.5.7-2.2 1.4C1.3 2.7.9 3.4.6 4.2.3 5 .1 5.8.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.1 1.3.3 2.1.6 2.9.3.8.7 1.5 1.4 2.2.7.7 1.4 1.1 2.2 1.4.8.3 1.6.5 2.9.6C8.3 24 8.7 24 12 24s3.7 0 4.9-.1c1.3-.1 2.1-.3 2.9-.6.8-.3 1.5-.7 2.2-1.4.7-.7 1.1-1.4 1.4-2.2.3-.8.5-1.6.6-2.9.1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.1-1.3-.3-2.1-.6-2.9-.3-.8-.7-1.5-1.4-2.2C21.3 1.3 20.6.9 19.8.6c-.8-.3-1.6-.5-2.9-.6C15.7 0 15.3 0 12 0zm0 5.8c-3.4 0-6.2 2.8-6.2 6.2s2.8 6.2 6.2 6.2 6.2-2.8 6.2-6.2S15.4 5.8 12 5.8zm0 10.2c-2.2 0-4-1.8-4-4s1.8-4 4-4 4 1.8 4 4-1.8 4-4 4zm7.8-10.4c0 .8-.7 1.4-1.4 1.4-.8 0-1.4-.7-1.4-1.4 0-.8.7-1.4 1.4-1.4.7-.1 1.4.6 1.4 1.4z"/></svg>
        </a>
        <a href="{s['tiktok']}" class="social-icon" aria-label="TikTok" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19.6 5.8c-1.2-.8-2-2.2-2-3.8H14v13.4c0 1.6-1.3 2.9-2.9 2.9-1.6 0-2.9-1.3-2.9-2.9s1.3-2.9 2.9-2.9c.3 0 .6 0 .9.1V9c-.3 0-.6-.1-.9-.1C7.8 8.9 5 11.7 5 15.4 5 19 7.9 22 11.6 22c3.7 0 6.6-2.9 6.6-6.6V9.1c1.4 1 3.1 1.6 5 1.6V7.3c0 0-2.1 0-3.6-1.5z"/></svg>
        </a>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="copy">© Keren Or Farm. All rights reserved.</div>
    <div class="footer-bottom-links">
      <a href="https://www.kerenorfarm.com/terms">{PAGE['footer_terms']}</a>
      <a href="https://www.kerenorfarm.com/privacy">{PAGE['footer_privacy']}</a>
      <a href="https://www.kerenorfarm.com/accessibility">{PAGE['footer_accessibility']}</a>
    </div>
  </div>
</footer>
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_path}">
<link rel="icon" href="{prefix}images/kerenor-logo.png" type="image/png">
</head>"""

def render_home():
    # 3 step icons
    step_imgs = ["step-plan.png", "step-choose-animal.png", "step-certificate.png"]
    steps_html = "".join(
        f"""<div class="how-card reveal">
          <div class="how-illust"><img src="images/{step_imgs[i]}" alt=""></div>
          <div class="how-step"><span class="num">{s['step']}.</span> {s['text']}</div>
        </div>"""
        for i, s in enumerate(PAGE["how_it_works"])
    )

    packages_html = ""
    for p in PAGE["packages"]:
        vip_class = " vip" if p["key"] == "vip" else ""
        includes = "".join(f"<li>{item}</li>" for item in p["includes"])
        footnote = f'<p class="pkg-footnote">{p["footnote"]}</p>' if p["footnote"] else ""
        vip_bonus = ""
        if p["key"] == "vip":
            vip_bonus = """<div class="pkg-vip-bonuses">
              <img src="images/vip-crown.png" alt="VIP" title="VIP crown">
              <img src="images/vip-block.png" alt="Block photo of your adopted animal" title="Block photo">
            </div>"""
        packages_html += f"""<div class="pkg{vip_class} reveal">
          <div class="pkg-header">{p['name']}</div>
          <div class="pkg-body">
            <div class="pkg-includes-title">What's included:</div>
            <ul class="pkg-list">{includes}</ul>
            {footnote}
            {vip_bonus}
            <div class="pkg-price">Donation: {p['price']}<small>one-time</small></div>
            <a href="{p['url']}" target="_blank" rel="noopener" class="pkg-cta">{p['cta']}</a>
          </div>
        </div>"""

    animals_html = ""
    for a in animals:
        animals_html += f"""<a class="animal-card reveal" href="animals/{a['slug']}.html">
          <div class="animal-photo">
            <img src="{a['photo']}" alt="{a['name']}, {a['species']}" loading="lazy">
            <div class="animal-photo-overlay"><span>{PAGE['click_to_adopt']}</span></div>
          </div>
          <div class="animal-body">
            <h3 class="animal-name">{a['name']}</h3>
            <p class="animal-tagline">{a['tagline']}</p>
          </div>
        </a>"""

    head = HEAD.format(
        title="Virtual Adoption · Keren Or Farm",
        desc=PAGE["hero_subtitle"],
        css_path="style.css",
        prefix="",
    )
    nav = render_nav(active_href="index.html", prefix="")
    footer = render_footer()

    return f"""{head}
<body>
{nav}

<section class="hero">
  <div class="hero-video-wrap">
    <div class="hero-video">
      <iframe src="https://www.youtube.com/embed/HvYXUiC_gt8?rel=0"
        title="Keren Or Farm" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
    </div>
  </div>
  <h1>{PAGE['hero_title']}</h1>
  <p class="hero-sub">{PAGE['hero_subtitle']}</p>
  <div class="tax-note">
    <div class="icon">🏆</div>
    <p><strong>Tax-Deductible Donation:</strong> {PAGE['tax_note']}</p>
  </div>
</section>

<section class="how" id="how">
  <div class="container">
    <h2 class="section-title">{PAGE['how_it_works_title']}</h2>
    <div class="how-grid">
      {steps_html}
    </div>
  </div>
</section>

<section class="packages" id="packages">
  <div class="container">
    <h2 class="section-title">{PAGE['packages_title']}</h2>
    <p class="section-intro">{PAGE['packages_intro']}</p>
    <div class="packages-grid">
      {packages_html}
    </div>
  </div>
</section>

<section class="residents" id="residents">
  <div class="container">
    <h2 class="section-title">{PAGE['residents_title']}</h2>
    <p class="section-intro">{PAGE['residents_intro']}</p>
    <div class="residents-grid">
      {animals_html}
    </div>
  </div>
</section>

{footer}
<script src="reveal.js"></script>
</body>
</html>"""

def render_animal_page(a, idx):
    others = [x for x in animals if x["slug"] != a["slug"]]
    related = [others[(idx + i) % len(others)] for i in range(3)]
    related_html = ""
    for r in related:
        related_html += f"""<a class="animal-card reveal" href="{r['slug']}.html">
          <div class="animal-photo">
            <img src="../{r['photo']}" alt="{r['name']}, {r['species']}" loading="lazy">
            <div class="animal-photo-overlay"><span>{PAGE['click_to_adopt']}</span></div>
          </div>
          <div class="animal-body">
            <h3 class="animal-name">{r['name']}</h3>
            <p class="animal-tagline">{r['tagline']}</p>
          </div>
        </a>"""

    head = HEAD.format(
        title=f"{a['name']} · Keren Or Farm",
        desc=a["tagline"],
        css_path="../style.css",
        prefix="../",
    )
    nav = render_nav(active_href="index.html", prefix="../")
    footer = render_footer()

    return f"""{head}
<body>
{nav}

<section class="animal-page-hero">
  <div class="container">
    <a href="../index.html#residents" class="back-link">{PAGE['back_to_all']}</a>
  </div>
</section>

<section class="profile">
  <div class="profile-photo reveal">
    <img src="../{a['photo']}" alt="{a['name']}, {a['species']}">
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
    <h2 class="section-title">Meet other <span>residents</span></h2>
    <div class="residents-grid">
      {related_html}
    </div>
  </div>
</section>

{footer}
<script src="../reveal.js"></script>
</body>
</html>"""

REVEAL_JS = """document.addEventListener('DOMContentLoaded', () => {
  const els = document.querySelectorAll('.reveal');
  // If IntersectionObserver missing or user prefers reduced motion, just show all
  const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window) || reduced) {
    els.forEach(el => el.classList.add('visible'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.01, rootMargin: '0px 0px 200px 0px' });
  els.forEach(el => io.observe(el));
  // Safety net: after 3s, force-show anything still hidden
  setTimeout(() => document.querySelectorAll('.reveal:not(.visible)').forEach(el => el.classList.add('visible')), 3000);
});
"""

# Write files
(ROOT / "style.css").write_text(CSS, encoding="utf-8")
(ROOT / "reveal.js").write_text(REVEAL_JS, encoding="utf-8")
(ROOT / "index.html").write_text(render_home(), encoding="utf-8")

anim_dir = ROOT / "animals"
anim_dir.mkdir(exist_ok=True)
for f in anim_dir.glob("*.html"):
    f.unlink()
for i, a in enumerate(animals):
    (anim_dir / f"{a['slug']}.html").write_text(render_animal_page(a, i), encoding="utf-8")

print(f"Built {len(animals)} animal pages + index.html")

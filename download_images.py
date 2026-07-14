#!/usr/bin/env python3
"""Download all animal images locally so the site is self-contained."""
import json, os, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
IMG_DIR = ROOT / "images"
IMG_DIR.mkdir(exist_ok=True)

SRC = json.loads((ROOT / "source_data.json").read_text(encoding="utf-8"))
T = json.loads((ROOT / "translations.json").read_text(encoding="utf-8"))

def slugify(name_en: str) -> str:
    s = name_en.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_&]+", "-", s).strip("-")
    return s

def fix_url(url: str) -> str:
    # Replace w_0,h_0 with real dimensions
    return url.replace("w_0,h_0,al_c,q_auto", "w_1200,h_1200,al_c,q_88")

for a in SRC["animals"]:
    heb = a["name"]
    en = T["animals"][heb]["name"]
    slug = slugify(en)
    url = fix_url(a["photo_url"])
    ext = ".jpg"
    if ".png" in a["photo_url"]:
        ext = ".png"
    elif ".jpeg" in a["photo_url"]:
        ext = ".jpg"
    outfile = IMG_DIR / f"{slug}{ext}"
    if outfile.exists() and outfile.stat().st_size > 5000:
        print(f"  skip {slug} (exists)")
        continue
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://www.kerenorfarm.com/",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        outfile.write_bytes(data)
        print(f"  ok   {slug}  {len(data)} bytes")
    except Exception as e:
        print(f"  FAIL {slug}: {e}")

print("done")

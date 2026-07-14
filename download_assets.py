#!/usr/bin/env python3
"""Download Kerenor site assets: logo, how-it-works illustrations, VIP bonus items."""
import urllib.request, os
from pathlib import Path

IMG = Path(__file__).parent / "images"
IMG.mkdir(exist_ok=True)

ASSETS = {
    "kerenor-logo.png": "https://static.wixstatic.com/media/2440e7_8182dad031a04663a34072ef2cc3d069~mv2.png/v1/fill/w_400,h_400,al_c,q_90/2440e7_8182dad031a04663a34072ef2cc3d069~mv2.png",
    "step-plan.png": "https://static.wixstatic.com/media/bd9d21_f73b0a977f4f4eaa82134db620264e46~mv2.png/v1/fill/w_506,h_420,al_c,lg_1,q_90/plan.png",
    "step-choose-animal.png": "https://static.wixstatic.com/media/bd9d21_275792229b894035bfa79ba7e25ca6ae~mv2.png/v1/fill/w_510,h_420,al_c,lg_1,q_90/choose-animal.png",
    "step-certificate.png": "https://static.wixstatic.com/media/bd9d21_0bd1bb0a61fa4250b2fa51e7bd436a6f~mv2.png/v1/fill/w_484,h_400,al_c,lg_1,q_90/certificate.png",
    "vip-crown.png": "https://static.wixstatic.com/media/bd9d21_096d8e5048a04c39b222260d34922fc2~mv2.png/v1/fill/w_175,h_127,al_c,lg_1,q_90/crown-vip.png",
    "vip-block.png": "https://static.wixstatic.com/media/bd9d21_4fd67c78d28747b1979d2ae0ec3c6ea2~mv2.png/v1/fill/w_304,h_206,al_c,lg_1,q_90/block-pics.png",
}

for name, url in ASSETS.items():
    outfile = IMG / name
    if outfile.exists() and outfile.stat().st_size > 3000:
        print(f"  skip {name}")
        continue
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.kerenorfarm.com/adoption",
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        outfile.write_bytes(data)
        print(f"  ok   {name}  {len(data)} bytes")
    except Exception as e:
        print(f"  FAIL {name}: {e}")

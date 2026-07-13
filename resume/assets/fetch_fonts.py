#!/usr/bin/env python3
"""Fetch the resume's web fonts once and inline them as base64 @font-face
rules into fonts.css, so rendered resumes are fully self-contained (no
network at print time). Latin subset only, to keep the payload small.

    python3 resume/assets/fetch_fonts.py    # writes resume/assets/fonts.css
"""

import base64
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")

FAMILIES = {
    "Inter": "Inter:wght@400;500;600;700",
    "Lora": "Lora:wght@500;600;700",
}


def curl(url: str) -> bytes:
    return subprocess.run(
        ["curl", "-sS", "--max-time", "40", "-H", f"User-Agent: {UA}", url],
        capture_output=True, check=True).stdout


# A @font-face block is "latin" when its unicode-range covers basic ASCII.
BLOCK_RE = re.compile(r"/\*\s*(?P<name>[\w-]+)\s*\*/\s*(?P<face>@font-face\s*\{.*?\})",
                      re.DOTALL)
WEIGHT_RE = re.compile(r"font-weight:\s*(\d+)")
URL_RE = re.compile(r"url\((https://[^)]+\.woff2)\)")


def build() -> str:
    out = []
    for family, spec in FAMILIES.items():
        css = curl(f"https://fonts.googleapis.com/css2?family={spec}&display=swap").decode()
        for m in BLOCK_RE.finditer(css):
            if m.group("name") != "latin":
                continue
            face = m.group("face")
            weight = WEIGHT_RE.search(face).group(1)
            woff2_url = URL_RE.search(face).group(1)
            data = curl(woff2_url)
            b64 = base64.b64encode(data).decode()
            out.append(
                f"@font-face{{font-family:'{family}';font-style:normal;"
                f"font-weight:{weight};font-display:swap;"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
            )
            print(f"  {family} {weight}: {len(data)//1024} KB")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    css = build()
    (HERE / "fonts.css").write_text(css)
    print(f"wrote {HERE/'fonts.css'} ({len(css)//1024} KB)")

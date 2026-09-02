#!/usr/bin/env python3
"""Render the link-preview card and the iPhone home-screen icon.

    docs/og.png                1200x630 — what iMessage, LinkedIn, and Slack show
                               when the link is shared
    docs/apple-touch-icon.png  180x180  — Add to Home Screen / Safari bookmarks

Both are drawn in the site's own palette and type (Lora + the same terracotta)
so a shared link and the page it opens read as one thing. Same flow as the
résumé PDFs: HTML → headless Chromium. Re-run whenever the hero words change;
the outputs are committed, so the site build never depends on a browser.

    python3 build_og.py
"""

import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

import content as C

ROOT = Path(__file__).parent
FONTS = (ROOT / "resume" / "assets" / "fonts.css").read_text()

EYEBROW = "GTM Strategy & Operations · AI Deployment"
THESIS = "Systems at scale, across the whole revenue function."


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chromium():
    for cand in ("/opt/pw-browsers/chromium", shutil.which("chromium"),
                 shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if cand and Path(cand).exists():
            return cand
    return None


OG_HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden;background:#FAFAF9}}
body{{position:relative;font-family:'Inter',system-ui,sans-serif;color:#1C1A19}}
.disc{{position:absolute;border-radius:50%;background:#F1EDE9}}
.d1{{width:520px;height:520px;right:-190px;top:-250px}}
.d2{{width:150px;height:150px;right:20px;top:-30px;background:#D97757;opacity:.22}}
.rule{{position:absolute;left:80px;top:96px;width:70px;height:4px;background:#D97757}}
.eyebrow{{position:absolute;left:80px;top:130px;font-family:ui-monospace,'SF Mono','JetBrains Mono',Menlo,monospace;
  font-size:21px;letter-spacing:.2em;text-transform:uppercase;color:#C15A34}}
.name{{position:absolute;left:80px;top:196px;font-family:'Lora',Georgia,serif;font-weight:600;
  font-size:104px;line-height:1;letter-spacing:-.01em}}
.thesis{{position:absolute;left:80px;top:340px;width:900px;font-family:'Lora',Georgia,serif;
  font-weight:500;font-size:42px;line-height:1.28;color:#2B2826}}
.site{{position:absolute;left:80px;bottom:78px;font-family:ui-monospace,'SF Mono','JetBrains Mono',Menlo,monospace;
  font-size:21px;letter-spacing:.06em;color:#8A857F}}
</style></head><body>
<div class="disc d1"></div><div class="disc d2"></div>
<div class="rule"></div>
<div class="eyebrow">{esc(EYEBROW)}</div>
<div class="name">{esc(C.NAME)}</div>
<div class="thesis">{esc(THESIS).replace(", ", ",<br>")}</div>
<div class="site">{esc(C.SITE)}</div>
</body></html>"""

ICON_HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{margin:0;padding:0}}
html,body{{width:180px;height:180px;overflow:hidden;background:#D97757}}
.m{{width:180px;height:180px;display:flex;align-items:center;justify-content:center;
  font-family:'Lora',Georgia,serif;font-weight:600;font-size:86px;color:#fff;
  letter-spacing:-.02em;padding-bottom:6px}}
</style></head><body><div class="m">DR</div></body></html>"""

CARDS = [
    ("og.png", 1200, 630, OG_HTML),
    ("apple-touch-icon.png", 180, 180, ICON_HTML),
]


# Headless Chromium leaves the bottom ~85px of a --screenshot unpainted (the
# window height includes chrome it never draws). Render taller, then crop —
# in pure Python, so this script needs nothing beyond the browser.
PAD = 120


def crop_png(raw, width, height):
    """Return the top-left width x height of an 8-bit RGB/RGBA PNG."""
    assert raw[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    pos, idat, ihdr = 8, b"", None
    while pos < len(raw):
        (ln,) = struct.unpack(">I", raw[pos:pos + 4])
        kind = raw[pos + 4:pos + 8]
        data = raw[pos + 8:pos + 8 + ln]
        if kind == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", data)
        elif kind == b"IDAT":
            idat += data
        pos += 12 + ln
    src_w, src_h, depth, ctype, _, _, interlace = ihdr
    assert depth == 8 and ctype in (2, 6) and interlace == 0, "unexpected PNG layout"
    bpp = 4 if ctype == 6 else 3
    stride = src_w * bpp
    flat = zlib.decompress(idat)
    prev = bytearray(stride)
    rows = []
    for y in range(min(height, src_h)):
        off = y * (stride + 1)
        f, line = flat[off], bytearray(flat[off + 1:off + 1 + stride])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1: line[i] = (line[i] + a) & 255
            elif f == 2: line[i] = (line[i] + b) & 255
            elif f == 3: line[i] = (line[i] + ((a + b) >> 1)) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(b"\x00" + bytes(line[:width * bpp]))
        prev = line

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, ctype, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
            + chunk(b"IEND", b""))


def render(binary, name, w, h, html):
    out = ROOT / "docs" / name
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "card.html"
        shot = Path(td) / "shot.png"
        src.write_text(html)
        subprocess.run(
            [binary, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", f"--window-size={w},{h + PAD}",
             f"--screenshot={shot}", src.as_uri()],
            check=True, capture_output=True,
        )
        out.write_bytes(crop_png(shot.read_bytes(), w, h))
    print(f"wrote docs/{name} ({w}x{h})")


if __name__ == "__main__":
    binary = chromium()
    if not binary:
        sys.exit("no Chromium found — install one or run this where the résumé PDFs are printed")
    (ROOT / "docs").mkdir(exist_ok=True)
    for name, w, h, html in CARDS:
        render(binary, name, w, h, html)

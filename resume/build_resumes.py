#!/usr/bin/env python3
"""Render Dylan Ram's targeted resumes to print-ready HTML in two designs.

One fact base, two lenses, two layouts. Career facts live in content.py (the
single source shared with the site); the look lives in the two CSS blocks +
render fns here. Every claim traces to the source
resume or to work in this repo — see resume/STRATEGY.md.

    python3 resume/assets/fetch_fonts.py     # once — bundles the fonts
    python3 resume/build_resumes.py          # writes resume/output/*.html

    # print to PDF (chromium shown; any browser's Print works):
    #   chromium --headless --no-sandbox --print-to-pdf-no-header \
    #     --print-to-pdf=out.pdf file:///.../resume/output/<file>.html

The two lenses
--------------
- ai-deployment      : the AI person — builds/ships AI AND sets the strategy
                       for deploying it. Flexes technical-forward (lead with
                       the engine + evals) or strategy-forward (lead with
                       self-serve + enablement) by reordering bullets.
- business-operations: the operating leader — signature programs, planning,
                       the two-sided-marketplace stakeholder story, zero-to-one
                       / one-to-100, with AI as the modern edge.

Design notes
------------
- Typography: Lora (editorial serif) for display, Inter for everything else,
  bundled as base64 in assets/fonts.css so PDFs are fully self-contained.
- Palette: warm near-black ink, terracotta accent — the same family as the
  portfolio, so the resume and the site read as one system.
- Two layouts: editorial (single column, ATS-safe) and modern (two-column
  with a skills rail; more designed, slight ATS risk — see STRATEGY.md).
- No fabricated metrics. Bullets lead with what the work was and its quality.
"""

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))  # repo root, so `import content` works when run as a script

import content as C

OUT_DIR = HERE / "output"
FONTS = (HERE / "assets" / "fonts.css").read_text()


def esc(s):
    """Escape plain text for HTML. content.py stores plain text; entities are a
    render-time concern, applied exactly once, here."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


NAME = esc(C.NAME)
CONTACT = [esc(c) for c in (C.EMAIL, C.PHONE, C.SITE, C.LINKEDIN, f"github.com/{C.GITHUB_USER}")]
EDUCATION_SCHOOL = esc(C.EDUCATION_SCHOOL)
EDUCATION_DEGREE = esc(C.EDUCATION_DEGREE)


def _variant(L, bullets_key):
    """Assemble one render-ready (pre-escaped) variant from content.py."""
    return {
        "tagline": esc(L["tagline"]),
        "summary": esc(L["summary"]),
        "skills": [(esc(label), esc(body)) for label, body in L["skills"]],
        "jobs": [
            {
                "company": esc(j["company"]),
                "role": esc(j["role"]),
                "note": esc(j["resume_note"]),
                "dates": esc(j["dates"]),
                "bullets": [esc(b) for b in j["bullets"][bullets_key]],
            }
            for j in C.JOBS
        ],
        "project_title": esc(L["project_title"]),
        "project_bullets": [esc(b) for b in L["project_bullets"]],
    }


# One résumé now — the unified record, in both layouts. The per-lens variants
# still build from LENSES if ever needed; the shipped set is C.RESUME alone.
VARIANTS = {C.RESUME["resume_stem"]: _variant(C.RESUME, "one")}

# ---------------------------------------------------------------------------
# Shared bits
# ---------------------------------------------------------------------------

RESET = """
    @page { size: letter; margin: 0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { background: #ffffff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
"""


def _skill_lines(variant, label_cls, body_cls):
    # Bodies are stored lowercase-led (they are lists, and resume.json splits
    # them into keywords); the résumé line reads as a sentence, so capitalize here.
    return "".join(
        f'<div class="skill-line"><span class="{label_cls}">{label}</span>'
        f'<span class="{body_cls}">{body[:1].upper() + body[1:]}</span></div>'
        for label, body in variant["skills"]
    )


def _jobs(variant):
    out = []
    for job in variant["jobs"]:
        note = f' <span class="job-note">{job["note"]}</span>' if job["note"] else ""
        bullets = "".join(f"<li>{b}</li>" for b in job["bullets"])
        out.append(
            f'<div class="job"><div class="job-head">'
            f'<div class="job-role">{job["role"]} &nbsp;·&nbsp; '
            f'<span class="job-co">{job["company"]}</span>{note}</div>'
            f'<div class="job-dates">{job["dates"]}</div></div>'
            f'<ul>{bullets}</ul></div>'
        )
    return "".join(out)


def _project(variant):
    pb = "".join(f"<li>{b}</li>" for b in variant["project_bullets"])
    return (
        f'<div class="job"><div class="proj-title">{variant["project_title"]}'
        f' <span class="proj-link">— github.com/{C.REPO_SLUG}</span></div>'
        f'<ul>{pb}</ul></div>'
    )


def _doc(css, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>{NAME} — Résumé</title><style>{FONTS}{RESET}{css}</style></head>'
            f'<body>{body}</body></html>')


# ---------------------------------------------------------------------------
# Layout A — EDITORIAL (single column, ATS-safe)
# ---------------------------------------------------------------------------

EDITORIAL_CSS = """
    body { font-family: 'Inter', system-ui, sans-serif; font-size: 9.2pt;
           line-height: 1.33; color: #33302e; }
    .page { width: 8.5in; padding: 0.4in 0.6in; }
    .name { font-family: 'Lora', Georgia, serif; font-size: 22pt; font-weight: 600;
            color: #1c1a19; line-height: 1; letter-spacing: 0.005em; }
    .tagline { font-size: 9.8pt; font-weight: 600; color: #B4552F; margin-top: 4pt;
               letter-spacing: 0.01em; }
    .contact { font-size: 8.5pt; color: #6b6560; margin-top: 4pt; }
    .contact span + span::before { content: "   ·   "; color: #cbc4bd; }
    h2 { font-size: 7.9pt; font-weight: 700; letter-spacing: 0.17em; text-transform: uppercase;
         color: #B4552F; border-bottom: 1px solid #e6e1dc; padding-bottom: 2pt;
         margin: 8.5pt 0 4pt; }
    .summary { color: #33302e; }
    .skill-line { margin-bottom: 2.5pt; }
    .skill-line .sk-label { font-weight: 700; color: #1c1a19; }
    .skill-line .sk-label::after { content: "  —  "; color: #b8b1aa; font-weight: 400; }
    .job { margin-bottom: 5pt; }
    .job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; }
    .job-role { font-size: 9.9pt; font-weight: 600; color: #1c1a19; }
    .job-co { color: #B4552F; font-weight: 600; }
    .job-note { font-size: 8.3pt; font-style: italic; font-weight: 400; color: #8a8580; }
    .job-dates { font-size: 8.7pt; color: #6b6560; white-space: nowrap; }
    ul { margin: 2.5pt 0 0; padding-left: 14pt; }
    li { margin-bottom: 1.7pt; color: #33302e; }
    li::marker { color: #D97757; }
    .proj-title { font-size: 9.8pt; font-weight: 600; color: #1c1a19; }
    .proj-title .proj-link { display: inline-block; font-weight: 400; font-size: 8.3pt; color: #8a8580; }
    .edu { color: #33302e; }
    .edu strong { color: #1c1a19; }
"""


def render_editorial(variant):
    contact = "".join(f"<span>{c}</span>" for c in CONTACT)
    skills = _skill_lines(variant, "sk-label", "sk-body")
    body = f"""<div class="page">
      <div class="name">{NAME}</div>
      <div class="tagline">{variant["tagline"]}</div>
      <div class="contact">{contact}</div>
      <h2>Summary</h2><div class="summary">{variant["summary"]}</div>
      <h2>Skills</h2>{skills}
      <h2>Experience</h2>{_jobs(variant)}
      <h2>Selected Project</h2>{_project(variant)}
      <h2>Education</h2>
      <div class="edu"><strong>{EDUCATION_SCHOOL}</strong> — {EDUCATION_DEGREE}</div>
    </div>"""
    return _doc(EDITORIAL_CSS, body)


# ---------------------------------------------------------------------------
# Layout B — MODERN (two-column, skills rail)
# ---------------------------------------------------------------------------

MODERN_CSS = """
    body { font-family: 'Inter', system-ui, sans-serif; font-size: 8.9pt;
           line-height: 1.31; color: #33302e; }
    .page { width: 8.5in; }
    .header { padding: 0.38in 0.55in 0.18in; display: flex; justify-content: space-between;
              align-items: flex-end; border-bottom: 2.2px solid #1c1a19; gap: 18pt; }
    .name { font-size: 21pt; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
            color: #1c1a19; line-height: 1; }
    .tagline { font-size: 8.7pt; font-weight: 600; color: #B4552F; text-transform: uppercase;
               letter-spacing: 0.11em; margin-top: 5pt; }
    .header-contact { text-align: right; font-size: 8.3pt; color: #6b6560; line-height: 1.65;
                      white-space: nowrap; }
    .cols { display: flex; align-items: stretch; }
    .rail { width: 31%; background: #F6F3F1; padding: 0.24in 0.28in; }
    .main { width: 69%; padding: 0.24in 0.36in 0.3in 0.34in; }
    h2 { font-size: 7.5pt; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase;
         color: #B4552F; margin: 0 0 5pt; }
    .main h2 { border-bottom: 1px solid #e6e1dc; padding-bottom: 2.5pt; }
    .block + .block { margin-top: 9pt; }
    .summary { color: #33302e; }
    .rail .skill-line { margin-bottom: 6pt; }
    .rail .sk-label { display: block; font-weight: 700; color: #1c1a19; margin-bottom: 1pt; }
    .rail .sk-body { color: #4f4a46; font-size: 8.6pt; }
    .rail .rail-links { font-size: 8.5pt; color: #4f4a46; line-height: 1.7; }
    .rail .edu-school { font-weight: 700; color: #1c1a19; }
    .rail .edu-degree { color: #4f4a46; font-size: 8.6pt; margin-top: 1pt; }
    .job { margin-bottom: 5.5pt; }
    .job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10pt; }
    .job-role { font-size: 9.4pt; font-weight: 600; color: #1c1a19; }
    .job-co { color: #B4552F; font-weight: 600; }
    .job-note { display: block; font-size: 8.1pt; font-style: italic; font-weight: 400;
                color: #8a8580; margin-top: 1pt; }
    .job-dates { font-size: 8.3pt; color: #6b6560; white-space: nowrap; }
    ul { margin: 3pt 0 0; padding-left: 13pt; }
    li { margin-bottom: 1.7pt; color: #33302e; }
    li::marker { color: #D97757; }
    .proj-title { font-size: 9.4pt; font-weight: 600; color: #1c1a19; }
    .proj-title .proj-link { display: block; font-weight: 400; font-size: 8.1pt;
                             color: #8a8580; margin-top: 1pt; }
"""


def render_modern(variant):
    header_contact = "<br>".join(CONTACT[:2])
    links = "<br>".join(CONTACT[2:])
    skills = _skill_lines(variant, "sk-label", "sk-body")
    body = f"""<div class="page">
      <div class="header">
        <div><div class="name">{NAME}</div>
             <div class="tagline">{variant["tagline"]}</div></div>
        <div class="header-contact">{header_contact}</div>
      </div>
      <div class="cols">
        <div class="rail">
          <div class="block"><h2>Skills</h2>{skills}</div>
          <div class="block"><h2>Links</h2>
            <div class="rail-links">{links}</div></div>
          <div class="block"><h2>Education</h2>
            <div class="edu-school">{EDUCATION_SCHOOL}</div>
            <div class="edu-degree">{EDUCATION_DEGREE}</div></div>
        </div>
        <div class="main">
          <div class="block"><h2>Summary</h2>
            <div class="summary">{variant["summary"]}</div></div>
          <div class="block"><h2>Experience</h2>{_jobs(variant)}</div>
          <div class="block"><h2>Selected Project</h2>{_project(variant)}</div>
        </div>
      </div>
    </div>"""
    return _doc(MODERN_CSS, body)


LAYOUTS = {"editorial": render_editorial, "modern": render_modern}


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    for stem, variant in VARIANTS.items():
        for layout, fn in LAYOUTS.items():
            path = OUT_DIR / f"{stem}--{layout}.html"
            path.write_text(fn(variant))
            print(f"wrote {path.name}")

#!/usr/bin/env python3
"""Assemble Dylan Ram's one-link portfolio site into docs/index.html.

A neutral hero with a lens toggle (Business Operations / AI Deployment) that
reframes the pitch and points at the matching resume, then the signature
work, the self-built agent operating system as proof, the experience
timeline, and downloads. Self-contained: fonts inlined as base64 so it
renders identically on GitHub Pages or anywhere.

    python3 build_site.py        # writes docs/index.html (+ scratchpad body-only for previews)

Deploy: repo Settings -> Pages -> Deploy from branch -> main -> /docs.

The resume PDFs are copied into docs/resumes/ and linked relatively, so the
published site serves them itself — the links never depend on a branch name
and keep working after feature branches are deleted.
"""

import json
import shutil
from pathlib import Path

import site_qa

ROOT = Path(__file__).parent
FONTS = (ROOT / "resume" / "assets" / "fonts.css").read_text()

BRANCH = "main"
REPO = "https://github.com/dylan3796/anthropic-portfolio"
BLOB = f"{REPO}/blob/{BRANCH}"

# Source PDFs live in resume/output/; the site serves its own copies.
PDF_SRC = ROOT / "resume" / "output"
PDF_DIR = ROOT / "docs" / "resumes"

RESUME_FILES = {
    "biz_ed": "dylan-ram-business-operations--editorial.pdf",
    "biz_mo": "dylan-ram-business-operations--modern.pdf",
    "ai_ed": "dylan-ram-ai-deployment--editorial.pdf",
    "ai_mo": "dylan-ram-ai-deployment--modern.pdf",
}
RESUMES = {key: f"resumes/{name}" for key, name in RESUME_FILES.items()}


def sync_resumes():
    """Copy the built PDFs next to index.html so Pages serves them directly."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for name in RESUME_FILES.values():
        src = PDF_SRC / name
        if not src.exists():
            raise SystemExit(f"missing resume PDF: {src} — run resume/build_resumes.py first")
        shutil.copy2(src, PDF_DIR / name)

LENS = {
    "ops": {
        "copy": ("The operating spine of a GTM org — zero to one, then one to 100. I run the "
                 "forecast, attribution, incentive, and quota systems a partner business "
                 "depends on, and align them across a two-sided marketplace."),
        "targets": "Business Operations · Chief of Staff · Partner &amp; Revenue Ops",
        "href": RESUMES["biz_mo"],
        "label": "Business Operations résumé",
    },
    "ai": {
        "copy": ("The AI-native operator. I deploy LLM agents into the workflows a GTM org "
                 "runs on — reporting, forecasting, crediting — and set up how it adopts them: "
                 "foundational data, KPI alignment, self-serve enablement, with tested code "
                 "owning anything that touches money. All of it is public, down to the eval "
                 "suite."),
        "targets": "Applied AI · AI Operations · AI Strategy &amp; Enablement",
        "href": RESUMES["ai_mo"],
        "label": "AI Deployment résumé",
    },
}

PROGRAMS = [
    ("The first forecast",
     "Built the partner team's first revenue forecasting process where none existed — "
     "methodology and cadence designed from the ground up."),
    ("The attribution model",
     "The canonical, single source of truth for how sourced, influenced, and attributed "
     "revenue is credited across the marketplace."),
    ("The first new-logo incentive",
     "Launched the partner org's first incentive program tied to new-logo acquisition — "
     "crediting and payout logic built from scratch."),
]

LAYERS = [
    ("Memory", "what every session boots knowing"),
    ("Data", "one governed dictionary, defined once"),
    ("Big rocks", "a living plan per initiative"),
    ("Skills", "recurring work, made invocable"),
    ("Loop", "the setup reviews and rewrites itself"),
]

PROOF_LINKS = [
    ("The repository", REPO),
    ("Architecture write-up", f"{BLOB}/docs/claude-code-architecture.md"),
    ("The crediting engine", f"{BLOB}/crediting/engine.py"),
    ("Interactive walkthrough", f"{BLOB}/app.py"),
]

EXPERIENCE = [
    ("2021 — now", "Databricks", "Partner Strategy &amp; Ops Manager",
     "first Partner S&amp;O hire · promoted 2023",
     "Built the data-and-AI foundation and the forecast, attribution, and incentive systems "
     "the partner business runs on; deployed the team's first LLM agents; leads quota-setting "
     "across Sales, Finance, and Partner leadership."),
    ("2019 — 2021", "Salesforce", "SMB Sales Strategy &amp; Operations Analyst", "",
     "Built the territory-carving model behind the annual GTM plan, automated QBR and "
     "forecast-accuracy tooling, and was the direct analytics partner to a $250M AMER SMB "
     "business."),
    ("2018 — 2019", "CBRE", "Business Data Analyst", "",
     "Owned the product-analytics stack end to end — data warehouse, Python data collection, "
     "and client-facing Tableau dashboards."),
]

CONTACT = [
    ("Email", "dylanmr96@gmail.com", "mailto:dylanmr96@gmail.com"),
    ("LinkedIn", "in/dylanram", "https://linkedin.com/in/dylanram"),
    ("GitHub", "dylan3796", "https://github.com/dylan3796"),
]

# ---------------------------------------------------------------------------
CSS = """
:root {
  --ground:#FAFAF9; --surface:#FFFFFF; --panel:#F1EDE9;
  --ink:#1C1A19; --body:#4A4643; --muted:#8A857F;
  --accent:#C15A34; --accent-bright:#D97757; --hairline:#E7E1DB;
  --shadow:0 1px 3px rgba(28,26,25,.07),0 8px 24px rgba(28,26,25,.05);
  --serif:'Lora',Georgia,serif;
  --sans:'Inter',system-ui,-apple-system,sans-serif;
  --mono:ui-monospace,'SF Mono','JetBrains Mono',Menlo,monospace;
}
@media (prefers-color-scheme:dark){
  :root{
    --ground:#191817; --surface:#201E1D; --panel:#242120;
    --ink:#F4F1ED; --body:#C9C3BC; --muted:#948E87;
    --accent:#E58C64; --accent-bright:#D97757; --hairline:#34302D;
    --shadow:0 1px 3px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.28);
  }
}
:root[data-theme="dark"]{
  --ground:#191817; --surface:#201E1D; --panel:#242120;
  --ink:#F4F1ED; --body:#C9C3BC; --muted:#948E87;
  --accent:#E58C64; --accent-bright:#D97757; --hairline:#34302D;
  --shadow:0 1px 3px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.28);
}
:root[data-theme="light"]{
  --ground:#FAFAF9; --surface:#FFFFFF; --panel:#F1EDE9;
  --ink:#1C1A19; --body:#4A4643; --muted:#8A857F;
  --accent:#C15A34; --accent-bright:#D97757; --hairline:#E7E1DB;
  --shadow:0 1px 3px rgba(28,26,25,.07),0 8px 24px rgba(28,26,25,.05);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{background:var(--ground);color:var(--body);font-family:var(--sans);
  font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:940px;margin:0 auto;padding:0 28px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:3px}

.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--accent);margin-bottom:22px}

/* hero */
.hero{padding:76px 0 30px}
.hero-name{font-family:var(--serif);font-weight:600;color:var(--ink);
  font-size:clamp(46px,9vw,78px);line-height:.98;letter-spacing:-.01em}
.hero-thesis{font-family:var(--serif);font-weight:500;color:var(--ink);
  font-size:clamp(21px,3.4vw,29px);line-height:1.32;max-width:20ch;
  text-wrap:balance;margin:26px 0 18px}
.hero-sub{font-size:17px;color:var(--body);max-width:62ch}

/* lens */
.lens{margin-top:40px}
.lens-label{font-family:var(--mono);font-size:12px;letter-spacing:.08em;
  color:var(--muted);margin-bottom:12px}
.lens-toggle{display:inline-flex;gap:4px;padding:4px;border-radius:999px;
  background:var(--panel);border:1px solid var(--hairline)}
.lens-btn{font-family:var(--mono);font-size:13px;letter-spacing:.03em;
  color:var(--muted);background:transparent;border:0;cursor:pointer;
  padding:9px 18px;border-radius:999px;transition:color .2s,background .2s}
.lens-btn:hover{color:var(--ink)}
.lens-btn.is-active{background:var(--accent-bright);color:#fff}
:root[data-theme="dark"] .lens-btn.is-active,
:root:not([data-theme="light"]) .lens-btn.is-active{color:#241a15}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .lens-btn.is-active{color:#fff}}
.lens-card{margin-top:18px;background:var(--surface);border:1px solid var(--hairline);
  border-left:3px solid var(--accent-bright);border-radius:0 12px 12px 0;
  box-shadow:var(--shadow);padding:24px 26px;max-width:640px}
.lens-copy{font-size:17px;color:var(--ink);transition:opacity .25s ease}
.lens-targets{font-family:var(--mono);font-size:12px;letter-spacing:.04em;
  color:var(--muted);margin-top:12px;transition:opacity .25s ease}
.lens-actions{margin-top:20px;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:14.5px;
  background:var(--ink);color:var(--ground);padding:11px 20px;border-radius:8px;
  transition:transform .15s,opacity .2s}
.btn:hover{text-decoration:none;opacity:.9;transform:translateY(-1px)}
.btn .arr{font-family:var(--mono)}

/* sections */
.section{padding:58px 0;border-top:1px solid var(--hairline)}
.section.alt{background:var(--panel)}
.sec-title{font-family:var(--serif);font-weight:600;color:var(--ink);
  font-size:clamp(26px,4vw,34px);letter-spacing:-.01em;text-wrap:balance}
.sec-lead{font-size:17px;color:var(--body);max-width:64ch;margin-top:12px}

/* program cards */
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:30px}
.card{background:var(--surface);border:1px solid var(--hairline);border-radius:12px;
  box-shadow:var(--shadow);padding:22px 22px 24px}
.card h3{font-family:var(--serif);font-weight:600;color:var(--ink);font-size:19px;
  margin-bottom:9px}
.card p{font-size:14.5px;color:var(--body)}
.aside{margin-top:22px;font-size:15px;color:var(--body);max-width:66ch}
.aside strong{color:var(--ink);font-weight:600}

/* system / layers */
.layers{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:28px 0}
.layer{background:var(--surface);border:1px solid var(--hairline);border-top:2px solid var(--accent-bright);
  border-radius:10px;padding:15px 14px}
.layer-name{font-family:var(--mono);font-size:12.5px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--accent);font-weight:600}
.layer-desc{font-size:12.5px;color:var(--muted);margin-top:7px;line-height:1.45}
.boundary{background:var(--surface);border:1px solid var(--hairline);border-radius:12px;
  box-shadow:var(--shadow);padding:22px 24px;margin-top:6px}
.boundary p{font-size:15.5px;color:var(--body);max-width:70ch}
.boundary strong{color:var(--ink);font-weight:600}
.proof-links{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:22px}
.proof-links a{font-family:var(--mono);font-size:13px}
.proof-links a::before{content:"↗ ";color:var(--muted)}

/* timeline */
.tl{margin-top:30px;display:flex;flex-direction:column;gap:0}
.tl-row{display:grid;grid-template-columns:130px 1fr;gap:22px;padding:20px 0;
  border-top:1px solid var(--hairline)}
.tl-row:first-child{border-top:0}
.tl-when{font-family:var(--mono);font-size:12.5px;color:var(--muted);
  letter-spacing:.04em;padding-top:3px;font-variant-numeric:tabular-nums}
.tl-role{font-family:var(--serif);font-weight:600;color:var(--ink);font-size:18px}
.tl-co{color:var(--accent);font-weight:600}
.tl-note{font-family:var(--mono);font-size:11.5px;color:var(--muted);
  letter-spacing:.03em;margin:3px 0 8px}
.tl-desc{font-size:14.5px;color:var(--body);max-width:70ch}

/* downloads + contact */
.dl-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:26px}
.dl-card{background:var(--surface);border:1px solid var(--hairline);border-radius:12px;
  box-shadow:var(--shadow);padding:20px 22px}
.dl-card h3{font-family:var(--serif);font-weight:600;color:var(--ink);font-size:18px}
.dl-card .dl-for{font-family:var(--mono);font-size:11.5px;color:var(--muted);
  letter-spacing:.04em;margin:5px 0 14px}
.dl-primary{display:inline-block;margin-top:14px;font-weight:600;font-size:14px;
  background:var(--ink);color:var(--ground);padding:10px 18px;border-radius:8px}
.dl-primary:hover{text-decoration:none;opacity:.9}
.dl-primary .arr{font-family:var(--mono)}
.dl-sec{display:block;margin-top:10px;font-size:13px;color:var(--muted)}
.contact{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.contact a{display:flex;flex-direction:column;gap:2px;background:var(--surface);
  border:1px solid var(--hairline);border-radius:10px;padding:14px 20px;min-width:170px}
.contact .c-k{font-family:var(--mono);font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted)}
.contact .c-v{font-size:15px;color:var(--ink);font-weight:500}
footer{padding:40px 0;border-top:1px solid var(--hairline);color:var(--muted);
  font-family:var(--mono);font-size:12px;letter-spacing:.03em}

.js .reveal{opacity:0;transform:translateY(14px);transition:opacity .6s ease,transform .6s ease}
.js .reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .reveal{opacity:1;transform:none;transition:none}}

@media (max-width:720px){
  .hero{padding:52px 0 24px}
  .cards{grid-template-columns:1fr}
  .layers{grid-template-columns:1fr 1fr}
  .dl-grid{grid-template-columns:1fr}
  .tl-row{grid-template-columns:1fr;gap:6px}
}
"""

JS_TAIL = """
const buttons=document.querySelectorAll('.lens-btn');
const copy=document.querySelector('[data-lens-copy]');
const targets=document.querySelector('[data-lens-targets]');
const btn=document.querySelector('[data-lens-resume]');
function setLens(k){
  const d=LENS[k];
  copy.style.opacity=0;targets.style.opacity=0;
  setTimeout(()=>{
    copy.innerHTML=d.copy;
    targets.innerHTML='Target roles: '+d.targets;
    btn.setAttribute('href',d.href);
    btn.querySelector('.lbl').textContent=d.label;
    copy.style.opacity=1;targets.style.opacity=1;
  },160);
  buttons.forEach(b=>{const on=b.dataset.lens===k;
    b.classList.toggle('is-active',on);b.setAttribute('aria-selected',on);});
}
buttons.forEach(b=>b.addEventListener('click',()=>setLens(b.dataset.lens)));
const io=new IntersectionObserver((es)=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}
}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
"""


def build_body():
    cards = "".join(
        f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in PROGRAMS
    )
    layers = "".join(
        f'<div class="layer"><div class="layer-name">{n}</div>'
        f'<div class="layer-desc">{d}</div></div>' for n, d in LAYERS
    )
    proof = "".join(f'<a href="{u}">{t}</a>' for t, u in PROOF_LINKS)
    tl = "".join(
        f'<div class="tl-row reveal"><div class="tl-when">{when}</div><div>'
        f'<div class="tl-role">{role} · <span class="tl-co">{co}</span></div>'
        + (f'<div class="tl-note">{note}</div>' if note else '<div class="tl-note"></div>')
        + f'<div class="tl-desc">{desc}</div></div></div>'
        for when, co, role, note, desc in EXPERIENCE
    )
    dl = f"""
      <div class="dl-card"><h3>Business Operations</h3>
        <div class="dl-for">BizOps · Chief of Staff · Partner &amp; Revenue Ops</div>
        <a class="dl-primary" href="{RESUMES['biz_mo']}">Download résumé <span class="arr">↓</span></a>
        <a class="dl-sec" href="{RESUMES['biz_ed']}">or the ATS-safe version</a></div>
      <div class="dl-card"><h3>AI Deployment</h3>
        <div class="dl-for">Applied AI · AI Ops · AI Strategy &amp; Enablement</div>
        <a class="dl-primary" href="{RESUMES['ai_mo']}">Download résumé <span class="arr">↓</span></a>
        <a class="dl-sec" href="{RESUMES['ai_ed']}">or the ATS-safe version</a></div>"""
    contact = "".join(
        f'<a href="{u}"><span class="c-k">{k}</span><span class="c-v">{v}</span></a>'
        for k, v, u in CONTACT
    )
    d0 = LENS["ops"]
    return f"""
<header class="hero"><div class="wrap">
  <div class="eyebrow">GTM operations · AI deployment</div>
  <h1 class="hero-name">Dylan Ram</h1>
  <p class="hero-thesis">I build the systems a go-to-market org runs on — and the AI that runs on top.</p>
  <p class="hero-sub">First Partner Strategy &amp; Ops hire at Databricks. I stood up the forecast,
  attribution, and incentive programs a partner business runs on — then built and deployed the
  AI layer over them.</p>
  <div class="lens">
    <div class="lens-label">// reading this as a hiring manager for</div>
    <div class="lens-toggle" role="tablist" aria-label="Choose a lens">
      <button class="lens-btn is-active" data-lens="ops" role="tab" aria-selected="true">Business Operations</button>
      <button class="lens-btn" data-lens="ai" role="tab" aria-selected="false">AI Deployment</button>
    </div>
    <div class="lens-card">
      <p class="lens-copy" data-lens-copy>{d0['copy']}</p>
      <p class="lens-targets" data-lens-targets>Target roles: {d0['targets']}</p>
      <div class="lens-actions">
        <a class="btn" data-lens-resume href="{d0['href']}">
          <span class="lbl">{d0['label']}</span><span class="arr">↓ PDF</span></a>
      </div>
    </div>
  </div>
</div></header>

<section class="section" id="work"><div class="wrap reveal">
  <h2 class="sec-title">Signature work</h2>
  <p class="sec-lead">Three systems that didn't exist before — built zero to one, then scaled
  one to 100 — alongside annual quota-setting and the partner program strategy (the Partner
  Value Score and tiering system).</p>
  <div class="cards">{cards}</div>
  <p class="aside">Every one of these runs across a <strong>two-sided marketplace</strong> —
  three constituencies at once: the partner team, the sales org that co-sells through partners,
  and the partners themselves. Balancing internal and external stakeholders is the operating
  problem most companies actually face.</p>
</div></section>

<section class="section alt" id="system"><div class="wrap reveal">
  <h2 class="sec-title">The system I built</h2>
  <p class="sec-lead">I've built this function twice — once at Databricks as its first ops hire,
  and once in public as working software — so I know which parts of an operating cadence an
  agent can own, and which must stay deterministic, tested code. My edge isn't <em>using</em>
  AI; it's building the system an org runs it through: five layers, from governed data to a loop
  that runs the QBR on the tooling itself.</p>
  <div class="layers">{layers}</div>
  <div class="boundary"><p>This isn't a toy domain: the crediting engine models the kind of
  partner-incentive program I launched at Databricks — the real job, rebuilt as tested software.
  The rule that makes AI safe in production: <strong>the model authors rules in plain English;
  deterministic, tested code computes anything that touches money.</strong> An eval suite pins
  the math — mid-quarter hires, territory handoffs, split credit, coverage gaps — so no model
  ever computes a credited dollar, and no deal is silently zeroed.</p>
  <div class="proof-links">{proof}</div></div>
</div></section>

{site_qa.section_html()}

<section class="section alt" id="experience"><div class="wrap reveal">
  <h2 class="sec-title">Experience</h2>
  <div class="tl">{tl}</div>
</div></section>

<section class="section" id="resumes"><div class="wrap reveal">
  <h2 class="sec-title">Take a résumé</h2>
  <p class="sec-lead">Two lenses, two designs each. Editorial is single-column and ATS-safe;
  Modern is the two-column version for reading directly.</p>
  <div class="dl-grid">{dl}</div>
  <div class="contact">{contact}</div>
</div></section>

<footer><div class="wrap">Built by Dylan Ram with Claude Code · 2026 · this site lives in
the <a href="{REPO}">repository</a> it describes.</div></footer>
"""


def build():
    body = build_body()
    style = f"<style>{FONTS}{CSS}{site_qa.QA_CSS}</style>"
    script = (
        f"<script>const LENS={json.dumps(LENS)};{JS_TAIL}"
        f"{site_qa.data_js()}{site_qa.QA_JS}</script>"
    )
    full = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Dylan Ram — GTM Operations &amp; AI Deployment</title>'
        '<meta name="description" content="Dylan Ram — first Partner Strategy &amp; Ops hire at '
        'Databricks. GTM operator and AI builder.">'
        '<script>document.documentElement.classList.add("js")</script>'
        f'{style}</head><body>{body}{script}</body></html>'
    )
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(full)
    (ROOT / "docs" / ".nojekyll").write_text("")  # serve files as-is on GitHub Pages
    sync_resumes()
    # one corpus feeds both the live chat and the offline fallback
    (ROOT / "worker").mkdir(exist_ok=True)
    (ROOT / "worker" / "corpus.js").write_text(site_qa.corpus_js())
    print(f"wrote docs/index.html + {len(RESUME_FILES)} resumes to docs/resumes/")
    # body-only variant (style + content + script, no <head>/<body>) for embedding/previews
    return style + body + script


if __name__ == "__main__":
    build()

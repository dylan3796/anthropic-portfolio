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

import content as C
import site_qa

ROOT = Path(__file__).parent
FONTS = (ROOT / "resume" / "assets" / "fonts.css").read_text()

BRANCH = "main"
REPO = f"https://github.com/{C.REPO_SLUG}"
BLOB = f"{REPO}/blob/{BRANCH}"

# Custom domain. Empty = GitHub Pages default (dylan3796.github.io). When set
# (e.g. "dylanram.com"), the build writes docs/CNAME — which is what actually
# configures Pages, since docs/ is the publishing source — plus canonical and
# og:url tags. Cutover runbook: DOMAIN-SETUP.md.
DOMAIN = "dylanram.com"

# The ask-box section. Off for now at Dylan's call — the offline search box
# read as a gimmick next to the rest of the page. Flip to True to bring it
# back (the corpus, evals, and Worker plumbing all stay live underneath, so
# nothing rots while it's hidden).
QA_SECTION = False


def pages_url():
    """Where GitHub Pages serves this repo, absolute and without a trailing slash.

    Two shapes, and the repo name is what picks between them: a repo named
    <user>.github.io is a *user site* served at the domain root, anything else
    is a *project site* served under /<repo>. Deriving it from REPO_SLUG means
    renaming the repo moves canonical, og:url, JSON-LD, robots, and sitemap
    together — they are the five places a stale URL does real damage.
    """
    repo = C.REPO_SLUG.split("/")[-1]
    root = f"https://{C.GITHUB_USER}.github.io"
    return root if repo.lower() == f"{C.GITHUB_USER}.github.io".lower() else f"{root}/{repo}"

# GoatCounter site code for privacy-light analytics (free; no cookies, no
# consent banner needed). Empty = no analytics script on the page. Set to the
# code chosen at goatcounter.com signup (e.g. "dylanram") once cold outreach
# starts — otherwise clicks from those emails are invisible. See
# outreach/PLAYBOOK.md.
ANALYTICS_ID = ""


def esc(s):
    """Escape plain text for HTML. content.py stores plain text; entities are a
    render-time concern, applied exactly once, here."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

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
    """Copy the built PDFs next to index.html so Pages serves them directly.

    resume/output/ is gitignored, so on a fresh clone (or any session without
    Chromium) it is empty. The committed docs/resumes/ copies are then kept
    as-is — the build must not die just because PDFs weren't regenerated.
    """
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    stale = []
    for name in RESUME_FILES.values():
        src = PDF_SRC / name
        if src.exists():
            shutil.copy2(src, PDF_DIR / name)
        elif (PDF_DIR / name).exists():
            stale.append(name)
        else:
            raise SystemExit(
                f"missing resume PDF: {name} in both resume/output/ and docs/resumes/ "
                "— run resume/build_resumes.py and print the PDFs first"
            )
    if stale:
        print(f"note: {len(stale)} PDF(s) not regenerated this run; "
              "keeping committed docs/resumes/ copies")

# Career content comes from content.py (plain text) and is escaped here.
_LENS_HREF = {"ops": RESUMES["biz_mo"], "ai": RESUMES["ai_mo"]}
_LENS_ATS = {"ops": RESUMES["biz_ed"], "ai": RESUMES["ai_ed"]}
# First words on the page, per lens — a founder arriving on ?lens=ai should
# never read "GTM operations" before anything else.
_LENS_EYEBROW = {
    "ops": "GTM strategy & operations · annual planning",
    "ai": "AI deployment · agent systems",
}

LENS = {
    key: {
        "copy": esc(C.LENSES[key]["site_copy"]),
        "eyebrow": _LENS_EYEBROW[key],
        "href": _LENS_HREF[key],
        "label": C.LENSES[key]["site_label"],
        # the download card follows the lens, so the page never shows two
        # identities at once — an ?lens= link reads as fully committed
        "dlTitle": esc(C.LENSES[key]["site_label"]).replace(" résumé", ""),
        "dlAts": _LENS_ATS[key],
        "otherKey": "ai" if key == "ops" else "ops",
        "otherLabel": esc(C.LENSES["ai" if key == "ops" else "ops"]["site_label"]),
    }
    for key in ("ops", "ai")
}

PROGRAMS = [(esc(t), esc(d)) for t, d in C.PROGRAMS]
PROGRAMS_AI = [(esc(t), esc(d)) for t, d in C.PROGRAMS_AI]

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
    (esc(j["site_when"]), esc(j["company"]), esc(j["role"]),
     esc(j["site_note"]), esc(j["site_desc"]))
    for j in C.JOBS
]

CONTACT = [
    ("Email", C.EMAIL, f"mailto:{C.EMAIL}"),
    ("LinkedIn", C.LINKEDIN.removeprefix("linkedin.com/"), f"https://{C.LINKEDIN}"),
    ("GitHub", C.GITHUB_USER, f"https://github.com/{C.GITHUB_USER}"),
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
.lens-proof{font-family:var(--mono);font-size:12px;letter-spacing:.04em;
  color:var(--muted);margin-top:14px}
.lens-proof a{color:var(--accent);text-decoration:none}
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
.range{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.range span{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--body);
  background:var(--surface);border:1px solid var(--hairline);border-radius:999px;padding:6px 12px}
.flow{display:flex;align-items:stretch;gap:0;margin:28px 0 14px}
.stage{flex:1;background:var(--surface);border:1px solid var(--hairline);border-radius:10px;
  padding:14px 16px;position:relative}
.stage+.stage{margin-left:34px}
.stage+.stage::before{content:"→";position:absolute;left:-26px;top:50%;transform:translateY(-50%);
  color:var(--accent-bright);font-size:17px;font-weight:700}
.stage-k{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--accent-bright);margin-bottom:6px}
.stage-v{font-size:13.5px;color:var(--body);line-height:1.5}
.rail{margin-top:12px;font-family:var(--mono);font-size:12px;letter-spacing:.02em;color:var(--muted);
  border-left:2px solid var(--accent-bright);padding:8px 14px;background:var(--surface)}
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
.dl-grid{display:grid;grid-template-columns:minmax(0,470px);gap:16px;margin-top:26px}
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
.dl-other{font-family:var(--sans);font-size:.87rem;color:var(--muted);margin-top:16px}
.dl-switch{font:inherit;color:var(--accent);background:none;border:none;padding:0;
  cursor:pointer}
.dl-switch:hover{text-decoration:underline}
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
  .eyebrow{font-size:11px;letter-spacing:.09em}
  .flow{flex-direction:column}
  .stage+.stage{margin-left:0;margin-top:30px}
  .stage+.stage::before{content:"↓";left:50%;top:-26px;transform:translateX(-50%)}
  .dl-grid{grid-template-columns:1fr}
  .tl-row{grid-template-columns:1fr;gap:6px}
}
"""

JS_TAIL = """
const buttons=document.querySelectorAll('.lens-btn');
const eyebrow=document.querySelector('[data-lens-eyebrow]');
const copy=document.querySelector('[data-lens-copy]');
const btn=document.querySelector('[data-lens-resume]');
const dlTitle=document.querySelector('[data-dl-title]');
const dlPrimary=document.querySelector('[data-dl-primary]');
const dlAts=document.querySelector('[data-dl-ats]');
const dlSwitch=document.querySelector('[data-dl-switch]');
function setLens(k){
  const d=LENS[k];
  eyebrow.textContent=d.eyebrow;
  // signature work follows the lens too
  document.querySelectorAll('[data-lens-only]').forEach(e=>{e.hidden=e.dataset.lensOnly!==k});
  copy.style.opacity=0;
  setTimeout(()=>{
    copy.innerHTML=d.copy;
    btn.setAttribute('href',d.href);
    btn.querySelector('.lbl').textContent=d.label;
    copy.style.opacity=1;
  },160);
  // the download card follows the lens, so the page never shows two identities
  dlTitle.textContent=d.dlTitle;
  dlPrimary.setAttribute('href',d.href);
  dlAts.setAttribute('href',d.dlAts);
  dlSwitch.textContent=d.otherLabel+' →';
  dlSwitch.dataset.target=d.otherKey;
  buttons.forEach(b=>{const on=b.dataset.lens===k;
    b.classList.toggle('is-active',on);b.setAttribute('aria-selected',on);});
}
buttons.forEach(b=>b.addEventListener('click',()=>{
  setLens(b.dataset.lens);
  const u=new URL(location);u.searchParams.set('lens',b.dataset.lens);
  history.replaceState(null,'',u);
}));
// the quiet "other side" link scrolls back to the toggle so the switch is visible
dlSwitch.addEventListener('click',()=>{
  setLens(dlSwitch.dataset.target||'ai');
  document.getElementById('resumes').scrollIntoView({block:'start'});
});
// shareable per-application links: ?lens=ai preselects the toggle
const lensParam=new URLSearchParams(location.search).get('lens');
if(lensParam==='ai'||lensParam==='ops')setLens(lensParam);
else setLens('ops');  // sync the download card with the default on load
const io=new IntersectionObserver((es)=>es.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}
}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
"""


def build_body():
    cards = "".join(
        f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in PROGRAMS
    )
    cards_ai = "".join(
        f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in PROGRAMS_AI
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
    # One card, following the lens. Showing both at once made the page read as
    # undecided — the last thing a visitor saw was "I'm two people, you pick."
    _d = LENS["ops"]
    dl = f"""
      <div class="dl-card" data-dl-card>
        <h3 data-dl-title>{_d['dlTitle']}</h3>
        <a class="dl-primary" data-dl-primary href="{_d['href']}">Download résumé <span class="arr">↓</span></a>
        <a class="dl-sec" data-dl-ats href="{_d['dlAts']}">or the ATS-safe version</a>
      </div>"""
    dl_other = (f'<p class="dl-other">Hiring for the other side? '
                f'<button type="button" class="dl-switch" data-dl-switch>'
                f'{_d["otherLabel"]} →</button></p>')
    contact = "".join(
        f'<a href="{u}"><span class="c-k">{k}</span><span class="c-v">{v}</span></a>'
        for k, v, u in CONTACT
    )
    d0 = LENS["ops"]
    return f"""
<header class="hero"><div class="wrap">
  <div class="eyebrow" data-lens-eyebrow>GTM strategy &amp; operations · annual planning</div>
  <h1 class="hero-name">Dylan Ram</h1>
  <p class="hero-thesis">Zero to one, then one to 100.</p>
  <p class="hero-sub">First Partner Strategy &amp; Ops hire at Databricks. Forecast, attribution,
  incentives, quotas, annual planning, partner investment strategy: stood up from zero, scaled
  across the org, with AI agents deployed on top.</p>
  <div class="lens">
    <div class="lens-label">// the work, two ways</div>
    <div class="lens-toggle" role="tablist" aria-label="Choose a lens">
      <button class="lens-btn is-active" data-lens="ops" role="tab" aria-selected="true">Business Operations</button>
      <button class="lens-btn" data-lens="ai" role="tab" aria-selected="false">AI Deployment</button>
    </div>
    <div class="lens-card">
      <p class="lens-copy" data-lens-copy>{d0['copy']}</p>
      <div class="lens-actions">
        <a class="btn" data-lens-resume href="{d0['href']}">
          <span class="lbl">{d0['label']}</span><span class="arr">↓ PDF</span></a>
      </div>
    </div>
    <p class="lens-proof">This page runs its own eval suite: every answer it gives is
    pinned by tests. <a href="{REPO}">Repo →</a></p>
  </div>
</div></header>

<section class="section" id="work"><div class="wrap reveal">
  <h2 class="sec-title">Signature work</h2>
  <p class="sec-lead">Systems that didn't exist before — built zero to one, scaled one to 100,
  and run across a two-sided marketplace: the partner team, the sellers who co-sell through
  partners, and the partners themselves.</p>
  <div data-lens-only="ops">
    <div class="cards">{cards}</div>
    <div class="range"><span>Territory design</span><span>Zero-to-one builds</span>
    <span>Strategic initiatives</span><span>Annual &amp; headcount planning</span>
    <span>Executive partnership</span><span>Leadership presentations</span></div>
  </div>
  <div data-lens-only="ai" hidden>
    <div class="cards">{cards_ai}</div>
    <div class="range"><span>Production agents</span><span>Evals &amp; golden tests</span>
    <span>Governed data layers</span><span>Agent workflow design</span>
    <span>Python &amp; SQL</span><span>Self-serve enablement</span></div>
  </div>
</div></section>

<section class="section" id="agents"><div class="wrap reveal">
  <h2 class="sec-title">The agentic system</h2>
  <p class="sec-lead">Stood up at Databricks partner ops and still running: reporting,
  partner recommendations, and natural-language answers, from raw GTM data to agents
  reps actually use.</p>
  <div class="flow">
    <div class="stage"><div class="stage-k">Sources</div>
      <div class="stage-v">Salesforce · Spark &amp; SQL pipelines</div></div>
    <div class="stage"><div class="stage-k">Governed data</div>
      <div class="stage-v">Medallion data layer · one metric dictionary</div></div>
    <div class="stage"><div class="stage-k">Agents</div>
      <div class="stage-v">Reporting agents · partner recommendations for reps ·
      partner-fit Q&amp;A · self-serve analytics</div></div>
    <div class="stage"><div class="stage-k">The org</div>
      <div class="stage-v">Partner team · sellers · leadership, answering their own questions</div></div>
  </div>
  <p class="rail">The operating rule, everywhere: the money path never touches a model.
  Plain-English rules → deterministic, tested code → evals pinning the math.</p>
</div></section>

<section class="section alt" id="system"><div class="wrap reveal">
  <h2 class="sec-title">Built in the open</h2>
  <p class="sec-lead">This repo demonstrates the same discipline, built from scratch on
  synthetic data: five layers, from governed data to a loop that runs the QBR on the
  tooling itself.</p>
  <div class="layers">{layers}</div>
  <div class="boundary"><p>This isn't a toy domain: incentive crediting is a class of problem
  I know from running it — and everything here is built from scratch on synthetic data.
  The rule that makes AI safe in production: <strong>the model authors rules in plain English;
  deterministic, tested code computes anything that touches money.</strong> An eval suite pins
  the math — mid-quarter hires, territory handoffs, split credit, coverage gaps — so no model
  ever computes a credited dollar, and no deal is silently zeroed.</p>
  <div class="proof-links">{proof}</div></div>
</div></section>

{site_qa.section_html() if QA_SECTION else ""}

<section class="section alt" id="experience"><div class="wrap reveal">
  <h2 class="sec-title">Experience</h2>
  <div class="tl">{tl}</div>
</div></section>

<section class="section" id="resumes"><div class="wrap reveal">
  <h2 class="sec-title">Take a résumé</h2>
  <p class="sec-lead">Matched to the lens you picked above. The ATS-safe version is
  single-column for application portals; the default is designed for reading.</p>
  <div class="dl-grid">{dl}</div>
  {dl_other}
  <div class="contact">{contact}</div>
</div></section>

<footer><div class="wrap">Built by Dylan Ram with Claude Code · 2026 · this site lives in
the <a href="{REPO}">repository</a> it describes.</div></footer>
"""


def build():
    body = build_body()
    qa_css = site_qa.QA_CSS if QA_SECTION else ""
    style = f"<style>{FONTS}{CSS}{qa_css}</style>"
    qa_js = f"{site_qa.data_js()}{site_qa.QA_JS}" if QA_SECTION else ""
    script = (
        f"<script>const LENS={json.dumps(LENS)};{JS_TAIL}"
        f"{qa_js}</script>"
    )
    # Absolute base for canonical/OG links: the custom domain once set, the
    # Pages default until then — so link previews work in both eras.
    base = f"https://{DOMAIN}" if DOMAIN else pages_url()
    domain_meta = (
        f'<link rel="canonical" href="{base}/">'
        f'<meta property="og:url" content="{base}/">'
        '<meta property="og:type" content="profile">'
        '<meta property="og:title" content="Dylan Ram — GTM Operations &amp; AI Deployment">'
        '<meta property="og:description" content="First Partner Strategy &amp; Ops hire at '
        'Databricks. Ask my AI stand-in anything — or paste a JD for a grounded fit check.">'
        f'<meta property="og:image" content="{base}/og.png">'
        '<meta name="twitter:card" content="summary_large_image">'
    )
    # Structured data so the "Dylan Ram" search result is his, with the right
    # links attached — the search every cold email and LinkedIn view triggers.
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": C.NAME,
        "url": f"{base}/",
        "email": f"mailto:{C.EMAIL}",
        "jobTitle": C.JOBS[0]["role"],
        "worksFor": {"@type": "Organization", "name": C.JOBS[0]["company"]},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": C.EDUCATION_SCHOOL},
        "sameAs": [f"https://{C.LINKEDIN}", f"https://github.com/{C.GITHUB_USER}"],
        "knowsAbout": [
            "Revenue Operations", "Business Operations", "Revenue Forecasting",
            "Incentive Compensation Design", "Partner Strategy",
            "AI Deployment", "LLM Agents", "Financial Planning & Analysis",
        ],
    }
    domain_meta += f'<script type="application/ld+json">{json.dumps(person)}</script>'
    analytics = (
        f'<script data-goatcounter="https://{ANALYTICS_ID}.goatcounter.com/count" '
        'async src="//gc.zgo.at/count.js"></script>'
    ) if ANALYTICS_ID else ""
    full = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Dylan Ram — GTM Operations &amp; AI Deployment</title>'
        '<meta name="description" content="Dylan Ram — first Partner Strategy &amp; Ops hire at '
        'Databricks. GTM operator and AI builder.">'
        f'{domain_meta}'
        '<script>document.documentElement.classList.add("js")</script>'
        f'{style}</head><body>{body}{script}{analytics}</body></html>'
    )
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(full)
    (ROOT / "docs" / ".nojekyll").write_text("")  # serve files as-is on GitHub Pages
    cname = ROOT / "docs" / "CNAME"
    if DOMAIN:
        cname.write_text(DOMAIN + "\n")
    elif cname.exists():
        cname.unlink()  # never leave a stale CNAME pointing Pages at a dead domain
    sync_resumes()
    # one corpus feeds both the live chat and the offline fallback
    (ROOT / "worker").mkdir(exist_ok=True)
    (ROOT / "worker" / "corpus.js").write_text(site_qa.corpus_js())
    # ...and AI tools browsing the site get the same grounded record
    (ROOT / "docs" / "llms.txt").write_text(site_qa.llms_txt())
    # crawler plumbing so the personal-name search finds and trusts the page
    (ROOT / "docs" / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "# AI agents and recruiting crawlers: /llms.txt is a structured dossier of\n"
        "# this candidate's record; /resume.json is the same record machine-readable.\n"
        f"\nSitemap: {base}/sitemap.xml\n"
    )
    # JSON Resume-style feed for agentic recruiters: the same facts content.py
    # feeds everything else, no more and no less. Phone deliberately omitted.
    resume_json = {
        "basics": {
            "name": C.NAME,
            "label": C.LENSES["ops"]["tagline"],
            "email": C.EMAIL,
            "url": f"{base}/",
            "summary": C.LENSES["ops"]["summary"],
            "profiles": [
                {"network": "LinkedIn", "url": f"https://{C.LINKEDIN}"},
                {"network": "GitHub", "url": f"https://github.com/{C.GITHUB_USER}"},
            ],
        },
        "work": [
            {
                "name": j["company"], "position": j["role"], "dates": j["dates"],
                "summary": j["site_desc"],
                "highlights": j["bullets"]["ops"] + j["bullets"]["ai"],
            }
            for j in C.JOBS
        ],
        "education": [{"institution": C.EDUCATION_SCHOOL, "area": C.EDUCATION_DEGREE}],
        "skills": [
            {"name": name, "keywords": [kw.strip() for kw in details.split(",")]}
            for lens in ("ops", "ai") for name, details in C.LENSES[lens]["skills"]
        ],
        "projects": [{"name": t, "description": d} for t, d in C.PROGRAMS + C.PROGRAMS_AI],
        "meta": {"canonical": f"{base}/resume.json", "llms": f"{base}/llms.txt",
                 "resumes": f"{base}/resumes/"},
    }
    (ROOT / "docs" / "resume.json").write_text(json.dumps(resume_json, indent=1))
    (ROOT / "docs" / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{base}/</loc></url>\n'
        '</urlset>\n'
    )
    print(f"wrote docs/index.html + {len(RESUME_FILES)} resumes to docs/resumes/")
    # body-only variant (style + content + script, no <head>/<body>) for embedding/previews
    return style + body + script


if __name__ == "__main__":
    build()

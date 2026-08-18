# Outreach Playbook — reach without ads

The asset is unusual, so the outreach should lean on what nobody else has: a
link where the hiring manager can **screen you in 60 seconds** — chat with
your stand-in, paste their own JD for a fit check, download the lens-matched
resume. Every email below is built to earn one click of that link.

Order of operations: cold email first (your call, and the right one — it's
targeted, free, and measurable), with LinkedIn as the passive layer that
catches the people your emails send searching for you.

## The link, used properly

One URL, three weapons:

| Link | Use when |
|---|---|
| `dylanram.com/?lens=ops` | BizOps / Chief of Staff / RevOps / finance-adjacent roles |
| `dylanram.com/?lens=ai` | Applied AI / AI Ops / AI Strategy roles |
| bare `dylanram.com` | Anything else — the reader picks the lens |

(Until the domain is live, the same params work on the github.io URL.)

The lens param preselects the toggle, so the first thing they read is pitched
to *their* opening. Never send a PDF attachment cold — attachments get you
filtered, and the PDF undersells you; the page carries the PDFs anyway.

## The cold email

Three sentences. Every added sentence cuts the reply rate.

1. **Their hook** — one specific thing about their company/team/posting that
   shows this isn't a blast. Named product, recent launch, the actual JD line.
2. **Your proof** — one sentence, one claim, matched to their world.
3. **The CTA** — the fit check. It does the work a paragraph of self-praise
   can't, because it lets *them* interrogate *you*.

Subject lines that work cold: short, specific, zero salesmanship —
`forecasting + incentive design — quick fit question`,
`your RevOps opening — 60-second screen`, `partner ops at <Company>`.

### Template — ops/finance-family role

> Hi <Name> — saw <Company> is hiring a <role title>. <One specific sentence
> about their situation: "Scaling incentive comp past the first hundred
> partners is usually where the crediting math starts silently breaking.">
>
> I was Databricks' first Partner Strategy & Ops hire — built their partner
> forecasting, attribution, and first incentive program from zero.
>
> Fastest way to judge me: paste your JD into dylanram.com/?lens=ops and it
> maps my experience to each of your requirements — honestly, gaps included.
> If the map looks right, I'd love 20 minutes.

### Template — AI-family role

> Hi <Name> — <specific hook about their AI effort or posting>.
>
> I deploy LLM agents into GTM workflows for a living — and my portfolio *is*
> one: a grounded AI stand-in that answers your screen, built on the rule that
> a model never gets to invent a fact (or compute a dollar).
>
> Paste your JD at dylanram.com/?lens=ai and it'll screen me against your
> requirements in about a minute. If it holds up, 20 minutes?

### Template — the transfer play (role outside GTM)

This is the maximalist positioning in outreach form. Don't apologize for the
domain — translate it in the first line and let the fit check argue the rest.

> Hi <Name> — your <Financial Operations> opening reads like my Databricks job
> with the labels changed: revenue forecasting is financial planning, incentive
> crediting is comp economics with controls, and annual quota-setting across
> Sales, Finance, and Partner leadership is budget allocation by another name.
>
> I built all three from zero as their first Partner Strategy & Ops hire.
>
> Test the claim: paste your JD into dylanram.com and it maps my experience to
> your requirements line by line. If the transfer argument holds, 20 minutes?

## Cadence and volume

- **10–15 truly researched emails a week beats 100 blasted.** The hook
  sentence is the work; everything else is templated.
- Send to the **hiring manager first**, recruiter second — the manager feels
  the pain the JD describes; the recruiter pattern-matches titles (and your
  title says GTM).
- Follow up **once**, 4–6 days later, two sentences, new angle ("the fit-check
  map for your JD came out strong on X — worth a look"), then stop. Silence
  after two touches is an answer.
- Best-effort send window: Tue–Thu morning, their timezone.

## Measurement (turn on before the first batch)

1. Create a free goatcounter.com account (no cookies, no consent banner —
   it won't uglify the page).
2. Set `ANALYTICS_ID` in `build_site.py`, rebuild, push.
3. The dashboard then shows: visits per day, referrers, and the `?lens=`
   paths — so you know which batch and which framing got the click, and
   whether the click reached the resume downloads.

What to check weekly: emails sent → site visits → fit checks/chats run (Worker
logs show call counts) → replies. Fix the weakest hop, not the loudest one.

## The passive layer (set once, works forever)

- **LinkedIn**: the site URL in the contact-info website slot AND pinned in
  Featured with a one-line description ("Screen me in 60 seconds — my AI
  stand-in answers your questions, or paste your JD for a fit check"). Your
  headline should say what you build, not your title.
- **Email signature**: `dylanram.com — screen me in 60 seconds`. Every reply
  in every thread becomes a distribution channel.
- **GitHub profile README**: one line pointing at the site — engineers
  evaluating the AI-lens story land on the repo first.
- **The name search**: the site ships Person structured data, a sitemap, and
  robots.txt, so Google associates dylanram.com with your name and links.
  Everyone you email searches you — that result page is the second impression.
- **AI tools**: `dylanram.com/llms.txt` feeds recruiting copilots the same
  grounded dossier your stand-in uses. When their AI screens you, it screens
  the record you wrote.

## What NOT to do

- No PDF attachments cold. No five-paragraph cover-letter emails.
- No "did you see my last email?" follow-ups — new information or nothing.
- Don't over-personalize past one sentence; researched-but-brisk beats fawning.
- Don't wait for the domain to start — the github.io link works today; the
  domain makes it prettier, not more functional.

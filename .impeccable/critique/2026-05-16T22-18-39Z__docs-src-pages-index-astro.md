---
target: docs/src/pages/index.astro
total_score: 25
p0_count: 0
p1_count: 3
timestamp: 2026-05-16T22-18-39Z
slug: docs-src-pages-index-astro
---
# rinha2-back-end-python Homepage Design Critique

Target: `docs/src/pages/index.astro`

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---:|---:|---|
| 1 | Visibility of System Status | 2 | CI/reports exist, but latest run/methodology is not summarized inline. |
| 2 | Match System / Real World | 2 | Developer language fits, but Asyncio/Gatling claims conflict with source/k6. |
| 3 | User Control and Freedom | 3 | Clear exits to Docs, GitHub, CI, reports. |
| 4 | Consistency and Standards | 2 | Visual system is cohesive; terminology is inconsistent. |
| 5 | Error Prevention | 2 | No risky flows, but misleading claims create user misunderstanding. |
| 6 | Recognition Rather Than Recall | 3 | Badges, metrics, and report links are visible; Rinha context is assumed. |
| 7 | Flexibility and Efficiency of Use | 3 | Fast paths to Docs/GitHub/reports are present. |
| 8 | Aesthetic and Minimalist Design | 3 | Focused aesthetic; proof section gets dense. |
| 9 | Error Recovery | 2 | Not strongly applicable; reports help validate but methodology is underexplained. |
| 10 | Help and Documentation | 3 | Docs link is prominent; challenge/methodology context should be closer to the hero. |
| **Total** |  | **25/40** | **Acceptable foundation, significant trust/accessibility fixes needed.** |

## Anti-Patterns Verdict

The page does not read as generic SaaS slop. It has a coherent Python/code identity: dark navy, Python blue/yellow, `def rinha2_python()`, code block, hard resource constraints, CI/report links. The slop risk is copy credibility: plausible but inaccurate technical claims (`Asyncio`, `Python Async`, `Gatling`) and generic superlative copy (`Warm, approachable, yet incredibly powerful`).

Deterministic scan found one warning: `single-font` on `docs/src/layouts/BaseLayout.astro`, snippet: `only font used is source code pro`. This is partly false positive because multiple fonts are loaded, but visually the page reads monospace-heavy.

## Overall Impression

Strong developer landing page, credible at a glance, but the proof layer needs to become operator-grade. Preserve the existing aesthetic. Overhaul the hierarchy, copy, benchmark provenance, accessibility, and component structure.

## What's Working

- Distinctive technical identity: Python colors, syntax-inspired logo, dark code surface.
- Good narrative flow: hero, stack badges, constraints code block, features, metrics, reports.
- Correct trust ingredients: hard constraints, CI link, report archive, concrete metrics.

## Priority Issues

### P1: Tech claims conflict with implementation

Hero says `Asyncio`, feature card says `Python Async`, but source is Flask + psycopg2 + Gunicorn sync workers.

Fix: replace with `Flask`, `Gunicorn`, `psycopg2`, `PostgreSQL stored procedures`, or `sync WSGI tuned under constraints`.

### P1: Benchmark language is inconsistent

Feature copy says Gatling, stress section says k6.

Fix: standardize on verified k6 language and remove Gatling unless historical reports prove it.

### P1: Metrics lack visible provenance

`47k+`, `<50ms`, `99.9%` are prominent but not tied to a run, commit, date, environment, or report.

Fix: add a compact provenance line and link the metrics to the latest report.

### P2: Hero copy is generic

`Warm, approachable, yet incredibly powerful` weakens a technically credible page.

Fix: use concrete proof copy tied to 1.5 CPU, 550MB, Flask/Gunicorn/PostgreSQL, and k6 CI.

### P2: Accessibility gaps

No explicit `:focus-visible`, no `prefers-reduced-motion`, CTA contrast around 3.66:1, heading outline skips H1 to H3.

Fix: add focus rings, reduced-motion overrides, darker primary CTA text or darker button background, and semantic H2 structure.

## Persona Red Flags

- First-time Rinha visitor: sees performance claims without challenge context or methodology, so the numbers feel impressive but hard to evaluate.
- Backend maintainer/reviewer: spots Asyncio/Gatling mismatches and starts doubting the whole page.
- Keyboard/reduced-motion user: hover-only affordances and ambient animations create avoidable friction.

## A/B or Variant Testing Plan

### Test 1: Hero proof density
- Hypothesis: surfacing proof above the fold increases Docs/GitHub clicks and trust.
- A/control: current hero with tagline, badges, CTAs, then code block.
- B: add a compact metric strip under tagline: `47k+ req/s`, `<50ms p95`, `33 reports`, `1.5 CPU / 550MB`.
- C: replace metric strip with one provenance capsule: `Latest k6 CI run: Apr 1, 2026, 1.5 CPU, 550MB`.
- Primary metric: Docs CTA CTR, GitHub CTA CTR, scroll depth into stress section.
- Recommendation: try B first, because it preserves the current visual grammar while moving proof earlier.

### Test 2: Copy specificity
- Hypothesis: concrete engineering copy beats generic brand copy for technical visitors.
- A/control: `Warm, approachable, yet incredibly powerful...`
- B: `A Flask/Gunicorn/PostgreSQL implementation tuned for Rinha 2024/Q1: 1.5 CPU, 550MB RAM, validated in k6 CI.`
- C: `Python under pressure: two Flask APIs, one NGINX edge, PostgreSQL procedures, 550MB total.`
- Primary metric: GitHub click-through and report-link click-through.
- Recommendation: B for accuracy; C if you want more attitude while keeping facts.

### Test 3: Proof module order
- Hypothesis: reducing early vertical cost improves comprehension.
- A/control: full `ChallengeConstraints` code block before feature cards and metrics.
- B: hero metric strip first, compact constraints row second, code block lower.
- C: split the code block into a two-column layout: code on left, latest run card on right.
- Primary metric: scroll depth to stress section, report opens.
- Recommendation: C for desktop, B for mobile.

### Test 4: Feature card specificity
- Hypothesis: implementation-specific cards reduce AI-slop perception.
- A/control: `Extreme Constraints`, `High Throughput`, `Python Async`.
- B: `1.5 CPU / 550MB`, `Postgres atomic procedures`, `Gunicorn + NGINX`.
- C: `Topology`, `Data path`, `Validation loop`, each with one source-backed fact.
- Primary metric: time on page, docs CTA after feature card exposure.
- Recommendation: B as the safe correction; C as the stronger overhaul.

### Test 5: Report archive framing
- Hypothesis: users need summary before archive density.
- A/control: eight timestamp cards.
- B: `Latest`, `Best`, `Median` mini-summary plus a smaller archive link.
- C: timeline strip grouped by date with latest report emphasized.
- Primary metric: report archive click-through and latest report opens.
- Recommendation: B, because it makes the archive useful without adding interaction complexity.

## Overhaul Direction

Keep the same aesthetic: dark Python terminal, syntax accents, code block, minimal nav. Shift from theatrical developer landing page to source-backed performance dossier.

Recommended structure:
1. Hero with exact implementation stack and proof strip.
2. Constraints/provenance band: resources, run source, latest report, commit/date.
3. System topology module: NGINX, two Flask/Gunicorn APIs, PostgreSQL procedure path.
4. Benchmark proof module: latest/best/median and report link.
5. Implementation cards with source-backed mechanisms.
6. Report archive with latest/best grouping.
7. Footer with repo and challenge attribution.

## Implementation Plan

1. Branch from synced main: `design/homepage-proof-overhaul`.
2. Correct copy in `docs/src/components/home/Hero.astro` and `Dashboard.astro`.
3. Add source-backed metric/provenance data near the top of `Dashboard.astro`.
4. Refactor headings to H2/H3 in `Dashboard.astro`.
5. Update `docs/src/styles/globals.css` for metric strip, provenance capsule, focus-visible, reduced motion, CTA contrast, and responsive code overflow.
6. Run `bun run build`, inspect homepage, and fix visual regressions.
7. Open PR with before/after screenshots and A/B test notes.

---
version: alpha
name: Rinha2 Backend Python
description: Source-backed performance dossier for a Python Rinha de Backend implementation.
colors:
  deep-python-night: "#0F0F23"
  python-panel: "#13132E"
  primary: "#4B8BBE"
  python-blue: "#4B8BBE"
  python-blue-light: "#79C0E0"
  python-indigo: "#1A2A4A"
  python-yellow: "#FFD43B"
  python-yellow-light: "#FFE873"
  text-ice: "#E8F4FD"
  text-mist: "#A8CCE0"
  text-muted-blue: "#89B8D4"
  code-black: "#050713"
  border-subtle: "#203754"
typography:
  display:
    fontFamily: "Source Code Pro, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    fontSize: "3rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Source Code Pro, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    fontSize: "1.8rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.06em"
  title:
    fontFamily: "Source Code Pro, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    fontSize: "1.2rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0em"
  body:
    fontFamily: "Source Code Pro, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "0em"
  label:
    fontFamily: "JetBrains Mono, Source Code Pro, ui-monospace, monospace"
    fontSize: "0.8rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.1em"
rounded:
  sm: 4px
  md: 8px
  lg: 12px
  xl: 20px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
components:
  button-primary:
    backgroundColor: "{colors.python-blue}"
    textColor: "{colors.deep-python-night}"
    rounded: "{rounded.sm}"
    padding: 16px
  button-primary-hover:
    backgroundColor: "{colors.python-blue-light}"
    textColor: "{colors.deep-python-night}"
    rounded: "{rounded.sm}"
    padding: 16px
  button-secondary:
    backgroundColor: "{colors.python-yellow}"
    textColor: "{colors.deep-python-night}"
    rounded: "{rounded.sm}"
    padding: 16px
  chip-stack:
    backgroundColor: "{colors.python-indigo}"
    textColor: "{colors.text-ice}"
    rounded: "{rounded.sm}"
    padding: 8px
  card-proof:
    backgroundColor: "{colors.python-panel}"
    textColor: "{colors.text-mist}"
    rounded: "{rounded.md}"
    padding: 32px
  code-panel:
    backgroundColor: "{colors.code-black}"
    textColor: "{colors.python-blue-light}"
    rounded: "{rounded.md}"
    padding: 32px
---

# Design System: Rinha2 Backend Python

## Overview

**Creative North Star: "The Python Pressure Lab"**

This visual system is a dark, code-native performance lab for a Python backend under contest constraints. It should feel like a measured engineering artifact: precise, compact, source-backed, and visibly under pressure. The current dark navy surface, Python blue/yellow syntax cues, and `def rinha2_python()` identity are core brand assets and should remain recognizable after the overhaul.

The design must become sharper, not louder. It rejects vague performance theater. Metrics, code snippets, cards, and report links should read as evidence from a real validation loop. Decorative particles and serpentine forms are allowed only as quiet atmosphere behind the proof, never as the proof itself.

**Key Characteristics:**

- Dark Python night surface with controlled blue/yellow syntax accents.
- Mono-forward typography used as identity, not as a blanket excuse for low readability.
- Compact proof modules that connect metrics to resource limits, k6 runs, CI, and reports.
- Flat technical surfaces with thin borders, tonal layering, and rare hover elevation.
- Developer-native copy that names the actual stack and avoids generic superlatives.

## Colors

The palette is a committed Python-brand dark mode: deep navy carries the surface, Python blue carries interaction and proof, Python yellow marks syntax and secondary emphasis.

### Primary

- **Python Blue**: Primary interaction, source-backed metric accents, active states, and semantic links. Use it deliberately, not as a wash over every element.
- **Python Light Blue**: Hover emphasis, metric numerals, and high-attention proof labels.

### Secondary

- **Python Yellow**: Syntax identity, logo emphasis, secondary CTA fill, and rare highlight moments. It should feel like Python syntax lighting up inside the dark surface.
- **Python Yellow Light**: Hover state for yellow fills. Use sparingly.

### Tertiary

- **Python Indigo**: Chip backgrounds, subtle stack badges, borders, and quiet structural separation.

### Neutral

- **Deep Python Night**: Page background and dominant atmosphere.
- **Python Panel**: Cards, sidebars, report containers, and grouped proof modules.
- **Text Ice**: Primary text on dark surfaces.
- **Text Mist**: Long-form body text and documentation summaries.
- **Text Muted Blue**: Secondary text, timestamps, and low-emphasis labels. Do not let this fall below WCAG AA at small sizes.
- **Code Black**: Code panels and terminal-like proof blocks.
- **Border Subtle**: Thin dividers and technical outlines.

### Named Rules

**The Proof Color Rule.** Blue means interaction or evidence. Yellow means syntax or exceptional emphasis. If a color does not clarify either, remove it.

**The No Neon Rule.** This is Python under pressure, not cyberpunk. Avoid purple glows, neon gradients, and glassy overlays.

## Typography

**Display Font:** Source Code Pro with system monospace fallbacks  
**Body Font:** Source Code Pro with system monospace fallbacks  
**Label/Mono Font:** JetBrains Mono for metric numerals and tight labels when extra density is useful

**Character:** The type system is mono-forward because code is part of the brand. It should still read like a careful engineering report. Long paragraphs need generous line-height and restrained width. If body readability suffers, introduce Inter for paragraphs while preserving Source Code Pro for logo, code, badges, metrics, and labels.

### Hierarchy

- **Display** (700, 3rem, 1.1): Hero headline and major identity moments only. Use fluid scaling in CSS for responsive implementation.
- **Headline** (700, 1.8rem, 1.2, tracked): Section titles such as stress results or benchmark proof. Avoid all-caps for long phrases.
- **Title** (700, 1.2rem, 1.3): Card titles, topology labels, and report summaries.
- **Body** (400, 1rem, 1.7): Descriptive copy. Keep line length around 65 to 75 characters.
- **Label** (600, 0.8rem, 0.1em): Metric labels, timestamp labels, stack tags, and compact metadata. Use uppercase only for short labels.

### Named Rules

**The Monospace Earns Its Place Rule.** Monospace is identity when it marks code, metrics, stack, and proof. It becomes friction when it turns every paragraph into a terminal wall.

**The Specificity Rule.** Replace generic hype with stack, constraint, run, and report details.

## Elevation

This system is flat by default. Depth comes from tonal layering, thin borders, and glow only on interaction. Resting cards should not float like SaaS panels. Hover elevation can exist, but it must be subtle and tied to clickable affordance.

### Shadow Vocabulary

- **Interaction Glow** (`0 10px 30px rgba(0, 0, 0, 0.3)`): Use only on hovered metric cards, report links, or CTAs.
- **Blue Proof Glow** (`0 5px 15px rgba(75, 139, 190, 0.35)`): Use only for active proof or primary CTA hover.
- **Yellow Syntax Glow** (`0 5px 15px rgba(255, 212, 59, 0.35)`): Use only for secondary CTA hover or rare syntax emphasis.

### Named Rules

**The Flat Evidence Rule.** Evidence modules sit on the surface. They do not need glass, blur, or heavy shadow to be credible.

**The Motion Opt-Out Rule.** Every particle, ambient drift, entrance reveal, and hover transform must respect `prefers-reduced-motion`.

## Components

### Buttons

- **Shape:** Small technical radius (4px). Buttons should feel precise, not pill-shaped.
- **Primary:** Python Blue fill with Deep Python Night text for WCAG AA contrast. Use for Documentation or the main proof path.
- **Secondary:** Python Yellow fill with Deep Python Night text. Use for GitHub or a secondary proof path.
- **Hover / Focus:** Hover may brighten and lift slightly. Focus must use a visible high-contrast outline, not hover color alone.

### Chips

- **Style:** Indigo-blue tinted background, small radius, compact padding, Source Code Pro label. Chips represent stack facts, not marketing categories.
- **State:** Static stack chips should not look clickable. Interactive filters need visible hover and focus states.

### Cards / Containers

- **Corner Style:** 8px for normal cards, 12px to 20px for large proof containers.
- **Background:** Python Panel or a faint blue-tinted surface over Deep Python Night.
- **Shadow Strategy:** Flat at rest. Use hover glow only for clickable report cards or metric cards.
- **Border:** Thin blue/indigo borders. Avoid side-stripe borders greater than 1px.
- **Internal Padding:** 24px to 32px for cards, 48px for major sections on desktop.

### Inputs / Fields

- **Style:** Code Black background, thin Python Indigo border, Text Ice input, Text Muted Blue placeholder.
- **Focus:** Border shifts to Python Blue with a visible outline or ring.
- **Error / Disabled:** Errors must include text and icon, not color alone.

### Navigation

Navigation is minimal and sticky. The logo uses Python syntax structure: `def` in Python Blue, project function name in Python Yellow. Links are muted by default and brighten on hover or focus. Keep top-level options few: GitHub, Docs, Reports if surfaced.

### Code Panels

Code panels are the signature component. Use Code Black, 8px radius, 1px border, and syntax colors that mirror Python Blue and Python Yellow. Code shown on the homepage must correspond to real constraints or source concepts. No fake terminal output unless explicitly labeled as illustrative.

### Benchmark Proof Modules

Proof modules pair a metric with provenance. Every major metric needs a nearby source signal: report date, run type, resource envelope, workflow link, or commit. A metric without provenance is decorative and should be demoted.

## Do's and Don'ts

### Do:

- **Do** preserve the dark Python/code aesthetic: Deep Python Night, Python Blue, Python Yellow, and the `def rinha2_python()` identity.
- **Do** connect metrics to k6, CI, report date, resource envelope, or commit context.
- **Do** name the actual implementation stack: Flask, Gunicorn, psycopg2, NGINX, PostgreSQL procedures.
- **Do** keep proof above the fold when possible: constraints, latest run, and report access should be visible early.
- **Do** add visible `:focus-visible` states and reduced-motion handling before shipping visual polish.
- **Do** use semantic headings. Section titles should be H2; card titles should be H3.

### Don't:

- **Don't** describe the implementation as Asyncio or Python Async unless the source code actually uses that architecture.
- **Don't** mix Gatling and k6 terminology. Pick the verified benchmark tool and use it consistently.
- **Don't** use generic SaaS landing-page copy such as “incredibly powerful” without proof.
- **Don't** use glassmorphism, purple gradients, neon cyberpunk lighting, or AI-tool marketing aesthetics.
- **Don't** use side-stripe borders greater than 1px as card accents. Use full borders, syntax labels, or metric structure instead.
- **Don't** present fake benchmark dashboards, unsupported metrics, or simulated terminal output as fact.
- **Don't** let decorative particles, clipped circles, or motion compete with metrics and reports.

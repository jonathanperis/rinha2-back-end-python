# Product

## Register

brand

## Users

Primary users are backend engineers, challenge reviewers, performance-minded maintainers, and future contributors evaluating a Python implementation of Rinha de Backend 2024/Q1. They arrive with technical skepticism: Python is not the expected fastest stack, so they need immediate proof that the implementation is serious, measured, and reproducible.

Secondary users are recruiters, portfolio visitors, and open-source readers who need to understand the project without already knowing the Rinha context. They should be able to grasp the constraints, topology, and validation loop in one pass before choosing Docs, GitHub, or a report.

## Product Purpose

This website presents `rinha2-back-end-python` as a source-backed performance dossier for a constrained banking API challenge. Its job is to show that a Python/Flask/Gunicorn/PostgreSQL stack can be tuned under severe limits, then route visitors to documentation, source code, CI stress tests, and historical reports.

Success means a technical visitor quickly understands three things:

1. The challenge envelope: 1.5 CPU and 550MB RAM across the full stack.
2. The implementation shape: NGINX, two Flask/Gunicorn API instances, PostgreSQL procedures, and connection pooling.
3. The proof trail: k6 validation, CI workflow, archived reports, and concrete metrics with provenance.

## Brand Personality

Precise, battle-tested, and developer-native.

The voice should feel like an engineer explaining a benchmark result, not a startup selling a platform. It can have personality through Python syntax, dark terminal atmosphere, and compact phrases, but every claim must remain implementation-specific and source-backed.

## Anti-references

- Generic SaaS landing pages with vague performance claims.
- AI-generated developer pages that use technical words loosely.
- Terminal cosplay that looks cool but hides the actual system behavior.
- Glossy glassmorphism, neon cyberpunk, and purple gradient product-marketing aesthetics.
- Fake benchmark dashboards, unsupported metrics, or simulated terminal output presented as fact.
- Mascot-heavy Python visuals that make the project feel unserious.

## Design Principles

1. **Proof before polish.** Visual style supports the evidence trail. Metrics need source, date, resource envelope, and report links.
2. **Same aesthetic, sharper truth.** Preserve the dark Python/code identity while correcting any copy that misstates the implementation.
3. **Make the constraint visible.** The 1.5 CPU / 550MB envelope is the emotional hook. Keep it close to the hero and benchmark proof.
4. **Developer-native, not developer-costumed.** Use code, monospace, and syntax color only when they carry real meaning.
5. **One pass to trust.** A skeptical reader should not need to open GitHub just to know what stack, workload, and report a claim came from.

## Accessibility & Inclusion

Target WCAG AA for text contrast and keyboard navigation. The dark aesthetic is part of the identity, but low-contrast muted blue text, hover-only states, and motion without opt-out are not acceptable.

Required accommodations:

- Visible `:focus-visible` treatment for all links and buttons.
- `prefers-reduced-motion` support for particles, ambient drift, entrance motion, and hover transforms.
- No color-only semantics for pass/fail/warn states.
- Body copy should remain readable despite the mono-forward visual system. Reserve dense monospace for labels, code, metrics, and identity moments when paragraphs get long.

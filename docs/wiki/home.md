---
title: Home
---

# Documentation Hub

Python 3.14 implementation for the Rinha de Backend 2024/Q1 challenge. This site documents how the fictional bank API keeps the HTTP layer thin, pushes balance consistency into PostgreSQL stored procedures, and keeps k6 evidence tied to committed report pages and release-workflow artifacts.

<div class="doc-hero-panel">
  <p class="eyebrow">source-backed map</p>
  <h2>What to read, and why it matters</h2>
  <p>The public docs are organized around the real runtime: two Flask/Gunicorn API containers behind NGINX, one PostgreSQL 16.7 database, and historical k6 reports published from <code>docs/public/reports</code>.</p>
</div>

<div class="stat-grid">
  <div class="stat-card"><span>Runtime</span><strong>Python 3.14</strong><small>Flask 3.1 + Gunicorn 25.3</small></div>
  <div class="stat-card"><span>Concurrency</span><strong>2 APIs</strong><small>4 workers × 2 threads each</small></div>
  <div class="stat-card"><span>State</span><strong>PostgreSQL</strong><small>atomic stored procedures</small></div>
  <div class="stat-card"><span>Envelope</span><strong>1.5 CPU / 550MB</strong><small>challenge-wide budget</small></div>
</div>

## Fast Paths

<div class="path-grid">
  <a class="path-card" href="challenge">
    <span class="path-kicker">01 · contract</span>
    <strong>Understand the challenge API</strong>
    <small>Endpoints, request rules, status codes, client IDs, and the resource budget.</small>
  </a>
  <a class="path-card" href="architecture">
    <span class="path-kicker">02 · runtime</span>
    <strong>Trace a request through the stack</strong>
    <small>NGINX least_conn, Flask/Gunicorn workers, connection pooling, and database procedures.</small>
  </a>
  <a class="path-card" href="getting-started">
    <span class="path-kicker">03 · local loop</span>
    <strong>Run the stack locally</strong>
    <small>Compose commands, smoke requests, k6 execution, and troubleshooting checkpoints.</small>
  </a>
  <a class="path-card" href="performance">
    <span class="path-kicker">04 · evidence</span>
    <strong>Read the benchmark trail</strong>
    <small>How to interpret k6 reports and connect them back to architecture choices.</small>
  </a>
</div>

## Wiki Pages

| Page | Best for | Source of truth |
|------|----------|-----------------|
| [Challenge](challenge) | API contract and constraints | Original Rinha spec + `src/WebApi/app.py` |
| [Architecture](architecture) | Runtime topology and consistency model | `docker-compose.yml`, `nginx.conf`, SQL init scripts |
| [Getting Started](getting-started) | Local execution and smoke checks | Docker Compose stack |
| [Performance](performance) | Benchmark interpretation and report links | `docs/public/reports`, k6 artifact uploads |
| [CI/CD Pipeline](ci-cd-pipeline) | Release, checks, Pages deployment | `.github/workflows/*` |

## Implementation Signals

- The HTTP layer validates shape, client IDs, and request payloads before handing work to PostgreSQL.
- `InsertTransacao()` performs balance updates and limit checks atomically with row-level locking.
- `GetSaldoClienteById()` returns statement-ready JSON so the API can avoid heavy response shaping.
- NGINX uses `least_conn` to distribute load between two identical API instances.
- Release automation publishes GHCR images, runs container checks, executes k6, uploads the latest stress-test artifact, and deploys this documentation to GitHub Pages.

## External Links

- [GitHub repository](https://github.com/jonathanperis/rinha2-back-end-python)
- [Stress test reports](/rinha2-back-end-python/reports/)
- [Original challenge specification](https://github.com/zanfranceschi/rinha-de-backend-2024-q1)

---

*[GitHub](https://github.com/jonathanperis/rinha2-back-end-python) · [Jonathan Peris](https://jonathanperis.github.io/)*

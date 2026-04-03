# Rinha de Backend 2024/Q1 — Python Implementation

High-performance banking API built with Python/Flask/Gunicorn for the Rinha de Backend challenge. Handles concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM).

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.14 | Language |
| Flask 3.1.3 | Web framework |
| Gunicorn 25.3.0 | WSGI HTTP server (4 workers, 2 threads) |
| psycopg2-binary 2.9.11 | PostgreSQL adapter |
| PostgreSQL 16.7 | Database with stored procedures |
| NGINX 1.27 | Load balancer (least_conn) |
| Docker | python:3.14-slim base |
| k6 | Load testing (shared suite) |

---

## Build Commands

```sh
docker compose up nginx -d --build                     # Full dev stack
docker compose up k6 --build --force-recreate         # Run stress tests
```

---

## Architecture

```
NGINX (:9999, least_conn)
├── webapi1-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w x 2t
├── webapi2-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w x 2t
└── PostgreSQL (0.5 CPU, 330MB)
    ├── InsertTransacao() — atomic balance + validation
    └── GetSaldoClienteById() — statement with JSONB
```

**Single-file API** (`src/WebApi/app.py`). Business logic in PostgreSQL stored procedures.

---

## Key Patterns

- **SimpleConnectionPool** — psycopg2 pool (1-10 connections)
- **Hardcoded client dict** — 5 predefined clients with limits
- **Stored procedures** handle all transaction logic atomically
- **UNLOGGED tables** for write performance
- **Non-root Docker user** for security
- Gunicorn: `--workers=4 --threads=2 --worker-class=sync --timeout=30`

---

## API Endpoints

| Method | Path | Status Codes |
|--------|------|-------------|
| POST | `/clientes/{id}/transacoes` | 200, 404, 422 |
| GET | `/clientes/{id}/extrato` | 200, 404 |
| GET | `/healthz` | 200 |

---

## Project Structure

```
rinha2-back-end-python/
├── src/WebApi/
│   ├── app.py             # Complete API (Flask application)
│   ├── requirements.txt   # Flask, psycopg2-binary, gunicorn
│   └── Dockerfile          # python:3.14-slim, non-root user
├── docker-entrypoint-initdb.d/
│   └── rinha.dump.sql      # Schema + stored procedures + seed data
├── docker-compose.yml      # Dev stack with observability
├── prod/docker-compose.yml # Prod stack with GHCR images
├── nginx.conf              # Load balancer config
└── .github/workflows/      # CI/CD
```

---

## CI/CD

- **PR:** Docker build + health check (20 retries)
- **Main:** Multi-platform Docker push (amd64/arm64) to GHCR + k6 load test + GitHub Pages report
- **Image:** `ghcr.io/jonathanperis/rinha2-back-end-python:latest`

---

## Environment Variables

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgres://postgres:postgres@db:5432/rinha?sslmode=disable` |

---

## Workflow Conventions

- **Branch + PR strategy**: All changes must go through a feature branch and pull request — never commit directly to main
- **Rebase-only merges**: PRs use rebase merge strategy (no merge commits, no squash)
- **GitHub CLI**: Always use `gh` CLI for GitHub operations (repos, PRs, issues, releases, checks)
- **Community health files**: Repo-wide files (CODE_OF_CONDUCT, CONTRIBUTING, SECURITY, PR templates) live in the `jonathanperis/.github` org repo — do not create them in this repository

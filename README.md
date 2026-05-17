# rinha2-back-end-python

> High-performance banking API built with Python, Flask, and PostgreSQL for the Rinha de Backend 2024/Q1 challenge

[![Build Check](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/build-check.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/build-check.yml) [![Main Release](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/main-release.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/main-release.yml) [![CodeQL](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/codeql.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/codeql.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Live demo →](https://jonathanperis.github.io/rinha2-back-end-python/reports/)** | **[Documentation →](https://jonathanperis.github.io/rinha2-back-end-python/)**

---

## About

Python implementation of the Brazilian backend challenge [Rinha de Backend 2024/Q1](https://github.com/zanfranceschi/rinha-de-backend-2024-q1), where a fictional bank API must handle concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM total). Uses PostgreSQL stored procedures for atomic business logic and Nginx for load balancing across two API instances.

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.14 | Language runtime |
| Flask | 3.1.3 | Web framework |
| Gunicorn | 25.3.0 | WSGI HTTP server (4 workers, 2 threads) |
| psycopg2-binary | 2.9.12 | PostgreSQL adapter |
| PostgreSQL | 16.7 | Database with stored procedures |
| NGINX | 1.27 | Reverse proxy / load balancer (least_conn) |
| Docker | - | Containerization and orchestration |
| k6 | - | Load / stress testing |

## Architecture

```
NGINX (:9999, least_conn)
├── webapi1-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w x 2t
├── webapi2-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w x 2t
└── PostgreSQL (0.5 CPU, 330MB)
    ├── InsertTransacao() — atomic balance + validation
    └── GetSaldoClienteById() — statement with JSONB
```

## Features

- PostgreSQL stored procedures for atomic server-side business logic
- PostgreSQL tuned for throughput: `synchronous_commit=0`, `fsync=0`, `full_page_writes=0`
- UNLOGGED tables for maximum write performance
- Nginx least_conn load balancing across two API instances
- SimpleConnectionPool (1-10) for efficient connection management
- Historical k6 HTML reports are published under the GitHub Pages report index for source-backed performance review

## Getting Started

### Prerequisites

- Docker with Docker Compose

### Quick Start

```bash
git clone https://github.com/jonathanperis/rinha2-back-end-python.git
cd rinha2-back-end-python
docker compose up nginx -d --build
```

API available at `http://localhost:9999`

### Run Stress Tests

```bash
docker compose up k6 --build --force-recreate
```

## API Endpoints

| Method | Path | Description | Status Codes |
|--------|------|-------------|-------------|
| POST | `/clientes/{id}/transacoes` | Submit debit or credit transaction | 200, 404, 422 |
| GET | `/clientes/{id}/extrato` | Get account balance statement | 200, 404 |
| GET | `/healthz` | Health check | 200 |

## Project Structure

```
rinha2-back-end-python/
├── src/WebApi/
│   ├── app.py             # Complete API (Flask application)
│   ├── requirements.txt   # Flask, psycopg2-binary, gunicorn
│   └── Dockerfile         # python:3.14-slim, non-root user
├── docker-entrypoint-initdb.d/
│   └── rinha.dump.sql     # Schema + stored procedures + seed data
├── docker-compose.yml     # Dev stack with observability
├── prod/docker-compose.yml # Prod stack with GHCR images
├── nginx.conf             # Load balancer config
└── .github/workflows/     # CI/CD pipelines
```

## CI/CD

| Workflow | Trigger | Description |
|----------|---------|-------------|
| Build Check | Pull requests | Docker Compose build/start via `up nginx --wait` + `/healthz` smoke check |
| Main Release | Push to main except `docs/**` | Multi-platform Docker push (`latest`/`latest-arm64` → multi-arch `latest`), production compose health check, and k6 report artifact upload |
| CodeQL | Push to main, PRs, weekly | Security and quality analysis |
| Deploy to GitHub Pages | Push to main | Reusable Pages workflow builds and deploys `docs/` with Bun |

Container images: `ghcr.io/jonathanperis/rinha2-back-end-python:latest` (multi-arch manifest) and `:latest-arm64` (arm64 source image).

## License

MIT — see [LICENSE](LICENSE)

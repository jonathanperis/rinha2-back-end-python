# Architecture

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.14 | Language runtime |
| Flask | 3.1.3 | Web framework |
| Gunicorn | 25.3.0 | WSGI HTTP server (4 workers, 2 threads) |
| psycopg2-binary | 2.9.11 | PostgreSQL adapter |
| PostgreSQL | 16.7 | Database with stored procedures |
| NGINX | 1.27 | Reverse proxy / load balancer (least_conn) |
| Docker | - | Containerization (python:3.14-slim base) |
| k6 | - | Load / stress testing |

## Overview

```text
NGINX (:9999, least_conn)
├── webapi1-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w x 2t
├── webapi2-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w x 2t
└── PostgreSQL (0.5 CPU, 330MB)
    ├── InsertTransacao() — atomic balance + validation
    └── GetSaldoClienteById() — statement with JSONB
```

## Services

| Service | Role | CPU | RAM |
|---------|------|-----|-----|
| webapi1 | Python API instance (Gunicorn 4w x 2t) | 0.4 | 100MB |
| webapi2 | Python API instance (Gunicorn 4w x 2t) | 0.4 | 100MB |
| nginx | Reverse proxy / load balancer (least_conn) | 0.2 | 20MB |
| postgresql | Database with stored procedures | 0.5 | 330MB |
| k6 | Load testing | (not counted) | (not counted) |
| grafana + influxdb | Observability dashboards | (not counted) | (not counted) |

## Load Balancing

Nginx uses `least_conn` strategy to distribute requests across the two API instances.

## Database

Business logic is implemented in PostgreSQL stored procedures (`InsertTransacao`, `GetSaldoClienteById`). The database uses UNLOGGED tables and is tuned for maximum write performance:

- `synchronous_commit=0` — no wait for WAL flush
- `fsync=0` — skip fsync on writes
- `full_page_writes=0` — skip full page writes

## Connection Management

The API uses psycopg2 `SimpleConnectionPool` with 1-10 connections per instance for efficient database access.

## Gunicorn Configuration

```text
--workers=4 --threads=2 --worker-class=sync --bind=0.0.0.0:8080 --timeout=30
```

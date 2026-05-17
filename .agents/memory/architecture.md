---
name: Python Rinha Architecture
description: Flask/Gunicorn single-file API, psycopg2 connection pooling, worker/thread configuration
type: project
---

## Design Decisions

**Single-file API (src/WebApi/app.py):**
- Flask routes + psycopg2 connection pool in one file
- Gunicorn WSGI server with tuned worker config

**Why:** Python's simplicity makes a single-file approach natural. Gunicorn's prefork model handles concurrency without async complexity.

**How to apply:** Keep it single-file. Don't add Flask blueprints or application factories unless the file grows unwieldy.

## Key Technical Choices

- **SimpleConnectionPool(1, 10)**: psycopg2 pool with 1-10 connections. Prevents connection exhaustion.
- **Gunicorn config**: `--workers=4 --threads=2 --worker-class=sync --timeout=30` — 8 concurrent connections per instance.
- **Hardcoded client dict**: `{1: 100000, 2: 80000, ...}` — same pattern as other rinha implementations.
- **python:3.14-slim**: Minimal Docker base image.
- **Non-root user**: `groupadd -r app && useradd -r -g app app` in Dockerfile.

## Shared Infrastructure

Same PostgreSQL schema, stored procedures, NGINX config, and k6 tests as Rust, .NET, and Go implementations.

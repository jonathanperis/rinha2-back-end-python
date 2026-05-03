---
title: Home
---

# Home

Python 3.14 implementation for the Rinha de Backend 2024/Q1 challenge. Manages a fictional bank API with transaction processing and balance statements under strict resource constraints (1.5 CPU, 550MB RAM total across all containers). Built with Flask 3.1, Gunicorn, and psycopg2.

## Wiki Pages

| Page | Description |
|------|-------------|
| [Challenge](challenge) | What is Rinha de Backend 2024/Q1 |
| [Architecture](architecture) | Stack, services, resource constraints |
| [Getting Started](getting-started) | Prerequisites and how to run |
| [Performance](performance) | Results, benchmarks, resource usage |
| [CI/CD Pipeline](ci-cd-pipeline) | GitHub Actions workflows |

## Key Features

- Python 3.14 with Flask 3.1 for lightweight HTTP routing
- Gunicorn WSGI server for multi-worker concurrency
- psycopg2 for efficient PostgreSQL connectivity
- PostgreSQL stored procedures for server-side business logic
- Consistent throughput under strict resource constraints

---

*[GitHub](https://github.com/jonathanperis/rinha2-back-end-python) · [Jonathan Peris](https://jonathanperis.github.io/)*

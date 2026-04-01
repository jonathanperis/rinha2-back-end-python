# rinha2-back-end-python

> Python implementation for the Rinha de Backend 2024/Q1 challenge with PostgreSQL stored procedures and Nginx load balancing

[![CI](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/build-check-webapi.yml/badge.svg)](https://github.com/jonathanperis/rinha2-back-end-python/actions/workflows/build-check-webapi.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## About

A Python implementation of the Brazilian backend challenge Rinha de Backend 2024/Q1, where a fictional bank API must handle concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM total). Uses PostgreSQL stored procedures for business logic and Nginx for load balancing across two API instances. Built for learning purposes.

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | - | API implementation |
| PostgreSQL | - | Database with stored procedures |
| Nginx | - | Reverse proxy and load balancer (least-conn) |
| Docker | - | Containerization and orchestration |
| k6 | - | Stress testing |

## Features

- PostgreSQL stored procedures for server-side business logic
- PostgreSQL tuned with synchronous_commit=0, fsync=0, full_page_writes=0
- Nginx least-conn load balancing across two API instances
- All requests under 800ms at 250MB RAM usage (60% below limit)

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

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/clientes/{id}/transacoes` | POST | Submit debit or credit transaction |
| `/clientes/{id}/extrato` | GET | Get account balance statement |

## Project Structure

```
rinha2-back-end-python/
├── src/WebApi/         — API implementation
├── docker-compose.yml  — Full stack: API x2, Nginx, PostgreSQL, k6, observability
└── .github/workflows/  — CI/CD pipelines
```

## CI/CD

Two GitHub Actions workflows: `build-check-webapi.yml` runs on pull requests to build and health-check the API, and `main-release-webapi.yml` runs on the main branch to build a multi-platform Docker image and push it to GHCR.

## License

MIT — see [LICENSE](LICENSE)

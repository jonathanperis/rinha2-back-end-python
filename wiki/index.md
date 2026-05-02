# rinha2-back-end-python

High-performance banking API built with Python, Flask, and PostgreSQL for the Rinha de Backend 2024/Q1 challenge. Handles concurrent transactions under strict resource constraints (1.5 CPU, 550MB RAM total).

## Wiki Pages

| Page | Description |
|------|-------------|
| [Challenge](Challenge) | What is Rinha de Backend 2024/Q1 |
| [Architecture](Architecture) | Stack, services, resource constraints |
| [Getting StartedL(Getting-Started.md) | Prerequisites and how to run |
| [Performance](Performance) | Results, benchmarks, resource usage |
| [CI/CD PipelineL(CI-CD-Pipeline.md) | GitHub Actions workflows |

## Key Features

- PostgreSQL stored procedures for atomic server-side business logic
- Nginx least_conn load balancing across two API instances
- SimpleConnectionPool (1-10) for efficient connection management
- UNLOGGED tables for maximum write performance
- PostgreSQL tuned for throughput: `synchronous_commit=0`, `fsync=0`, `full_page_writes=0`
- Non-root Docker user for security
- All requests under 800ms at ~250MB RAM usage (60% below limit)

---

*[GitHubL(https://github.com/jonathanperis/rinha2-back-end-python.md) · [Jonathan Peris](https://jonathanperis.github.io/)*

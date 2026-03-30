# rinha2-back-end-python

High-performance backend implementation for the **Rinha de Backend** challenge (2nd Edition, 2024/Q1) — built with **Python**, **PostgreSQL**, and **Nginx**.

**Live results:** [jonathanperis.github.io/rinha2-back-end-python](https://jonathanperis.github.io/rinha2-back-end-python/)

---

## About

A Python implementation of the Brazilian backend programming challenge that pushes API performance under strict resource constraints. The API manages fictional bank clients with credit/debit transactions and balance statements.

### Endpoints

- `POST /clientes/{id}/transacoes` — Create a transaction (credit or debit)
- `GET /clientes/{id}/extrato` — Get client balance and recent transactions

### Results

All requests completed under 800ms using only **250MB of RAM** — 60% less than the challenge allows.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | API implementation |
| PostgreSQL | Database with stored procedures |
| Nginx | Reverse proxy / load balancer |
| Docker | Containerization and orchestration |
| Prometheus + Grafana | Observability |
| k6 | Stress testing |

## Architecture

- **2 API instances** behind Nginx
- **1 PostgreSQL** database (tuned for max throughput)
- **1 Nginx** load balancer
- Business logic pushed into PostgreSQL stored procedures

## Getting Started

```bash
docker compose up nginx -d --build
```

The API will be available at `http://localhost:9999`.

## Other Implementations

- [rinha2-back-end-dotnet](https://github.com/jonathanperis/rinha2-back-end-dotnet) — C# / .NET
- [rinha2-back-end-go](https://github.com/jonathanperis/rinha2-back-end-go) — Go
- [rinha2-back-end-rust](https://github.com/jonathanperis/rinha2-back-end-rust) — Rust
- [rinha2-back-end-k6](https://github.com/jonathanperis/rinha2-back-end-k6) — k6 stress tests

## License

Licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

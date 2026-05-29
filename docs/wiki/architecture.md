# Architecture

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.14 | Language runtime |
| Flask | 3.1.3 | Lightweight HTTP routing and JSON responses |
| Gunicorn | 25.3.0 | WSGI HTTP server (`4` workers, `2` threads) |
| psycopg2-binary | 2.9.12 | PostgreSQL adapter and connection pool |
| PostgreSQL | 16.7 | Database with stored procedures and row-level locking |
| NGINX | 1.27 | Reverse proxy / load balancer (`least_conn`) |
| Docker | - | Containerization (`python:3.14-slim` base) |
| k6 | - | Load / stress testing |

## Runtime Topology

```text
client / k6
   │
   ▼
NGINX (:9999, least_conn, 0.2 CPU, 20MB)
├── webapi1-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w × 2t
├── webapi2-python (:8080, 0.4 CPU, 100MB) — Gunicorn 4w × 2t
└── PostgreSQL 16.7 (0.5 CPU, 330MB)
    ├── InsertTransacao() — atomic balance update + limit validation
    └── GetSaldoClienteById() — statement projection with JSONB
```

## Request Flow

1. NGINX receives traffic on `:9999` and routes to the API instance with the fewest active connections.
2. Flask validates the route, client ID, JSON payload shape, transaction type, and description length.
3. psycopg2 checks out a connection from a `SimpleConnectionPool(1, 10)` inside the API process.
4. PostgreSQL stored procedures perform the balance mutation or statement projection.
5. The API commits successful transactions, rolls back failures, returns the compact response, and releases the connection.

## Services and Resource Envelope

| Service | Role | CPU | RAM |
|---------|------|-----|-----|
| `webapi1-python` | Python API instance (Gunicorn `4w × 2t`) | `0.4` | `100MB` |
| `webapi2-python` | Python API instance (Gunicorn `4w × 2t`) | `0.4` | `100MB` |
| `nginx` | Reverse proxy / load balancer (`least_conn`) | `0.2` | `20MB` |
| `db` | PostgreSQL 16.7 with stored procedures | `0.5` | `330MB` |
| `k6` | Load testing runner | not counted | not counted |
| `grafana`, `influxdb`, `prometheus` | Local observability loop | not counted | not counted |

## Database Responsibilities

Business logic is implemented in PostgreSQL stored procedures (`InsertTransacao`, `GetSaldoClienteById`). The database owns the race-sensitive parts of the challenge:

- Atomic debit/credit application.
- Credit-limit rejection for invalid debit outcomes.
- Recent-transaction selection for statement responses.
- JSON-shaped statement data returned to the API.

The physical schema is also tuned for the benchmark workload:

| Element | Source-backed behavior |
|---------|------------------------|
| `Clientes` table | `CREATE UNLOGGED TABLE`, seeded with five fixed client IDs and limits. |
| `Transacoes` table | `CREATE UNLOGGED TABLE ... WITH (fillfactor = 90)` for write-heavy inserts. |
| `InsertTransacao()` | Uses `SELECT ... FOR UPDATE` on the client row to serialize concurrent balance changes for the same client. |
| `GetSaldoClienteById()` | Returns the current balance plus the latest `10` transactions as `jsonb`. |
| `IX_Transacoes_ClienteId_Id_Desc` | Composite index on `(ClienteId, Id DESC)` so statement reads can fetch recent transactions for one client efficiently. |

For benchmark speed, the database is tuned with durability trade-offs:

- `synchronous_commit=0` — do not wait for WAL flush.
- `fsync=0` — skip fsync on writes.
- `full_page_writes=0` — skip full-page writes.

These settings are useful for the contest-style load test and are not production-safe for real banking data.

## Gunicorn Configuration

```bash
--workers=4 --threads=2 --worker-class=sync --bind=0.0.0.0:8080 --timeout=30
```

Each API container therefore exposes multiple synchronous workers while keeping the Python layer intentionally small: validation, stored-procedure calls, response mapping, and connection cleanup.

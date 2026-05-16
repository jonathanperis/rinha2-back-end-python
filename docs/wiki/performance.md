# Performance

## Resource Constraints

The challenge allows a total of `1.5` CPU and `550MB` RAM across the application containers. This repository spends that budget on two API instances, PostgreSQL, and NGINX:

| Component | CPU | RAM | Performance role |
|-----------|-----|-----|------------------|
| Two API containers | `0.8` total | `200MB` total | Parallel request handling and validation |
| PostgreSQL | `0.5` | `330MB` | Atomic balance mutation and statement projection |
| NGINX | `0.2` | `20MB` | Low-overhead load balancing |

## Optimization Shape

The implementation optimizes for the contest workload by keeping each layer focused:

- **Thin Python path:** Flask validates input and delegates consistency-sensitive work to SQL.
- **Database-owned invariants:** `InsertTransacao()` handles balance updates and limit rejection atomically.
- **Compact statement reads:** `GetSaldoClienteById()` returns statement data already shaped for the API response.
- **Two API replicas:** NGINX uses `least_conn` so a busy worker pool does not become the only ingress path.
- **Durability trade-offs:** PostgreSQL write-safety settings are relaxed for benchmark throughput, not for production banking data.

## Reading the Reports

Published reports are the source of truth for run-level performance evidence:

- [Stress test report index](/rinha2-back-end-python/reports/) lists every archived HTML report.
- The latest entries come from the mainline release workflow after container verification.
- Compare reports by commit context and workflow timing, not just by a single latency number.

When evaluating a run, inspect:

| Signal | Why it matters |
|--------|----------------|
| HTTP failure rate | Validates that concurrency did not break the API contract |
| Request duration percentiles | Shows tail behavior under contention |
| Transaction throughput | Reveals whether app/DB coordination is saturated |
| Statement latency | Confirms reads stay responsive while writes are active |
| Report timestamp | Connects the result to the release workflow and code state |

## Benchmark Interpretation

This is a deliberately constrained system, so performance conclusions should stay tied to the workload:

1. Local Docker and GitHub-hosted runners can be noisy.
2. PostgreSQL tuning favors contest throughput over durability.
3. The Python layer is intentionally not a business-logic engine; moving limit checks out of SQL would change the contention model.
4. A good report is both fast and correct: successful status codes and stable statement semantics matter as much as latency.

## Useful Next Reads

- [Architecture](/rinha2-back-end-python/docs/architecture/) for the runtime and stored-procedure boundaries.
- [CI/CD Pipeline](/rinha2-back-end-python/docs/ci-cd-pipeline/) for how reports are produced and published.
- [Reports](/rinha2-back-end-python/reports/) for archived k6 HTML output.

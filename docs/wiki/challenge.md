# Challenge

## Rinha de Backend 2024/Q1

The Rinha de Backend is a Brazilian backend programming challenge. The 2024/Q1 edition simulates a fictional bank called "Rinha Financeira" that manages up to 5 named clients, each seeded at startup with a credit limit and initial balance.

The interesting part is not the endpoint count; it is the combination of high write contention, strict response semantics, and a shared container budget small enough to punish waste.

## Endpoint Contract

| Endpoint | Method | Success | Validation / rejection |
|----------|--------|---------|------------------------|
| `/clientes/{id}/transacoes` | `POST` | `200` with `limite` and updated `saldo` | `400` for a missing JSON payload, `404` for unknown client, `422` for invalid transaction fields or exceeded limit |
| `/clientes/{id}/extrato` | `GET` | `200` with `saldo` and recent transactions | `404` for unknown client |
| `/healthz` | `GET` | `200` with `Healthy` | Used by container and CI smoke checks |

### Transaction payload

```json
{
  "valor": 1000,
  "tipo": "c",
  "descricao": "deposito"
}
```

Runtime validation in `src/WebApi/app.py` keeps the contract narrow:

- `valor` must be a positive integer value.
- `tipo` must be `c` for credit or `d` for debit.
- `descricao` must be a non-empty string with at most 10 characters.
- Client IDs are fixed to `1` through `5`.

The runtime client table is intentionally static and mirrors the seed data in `docker-entrypoint-initdb.d/rinha.dump.sql`:

| Client ID | Credit limit | Initial balance |
|-----------|--------------|-----------------|
| `1` | `100000` | `0` |
| `2` | `80000` | `0` |
| `3` | `1000000` | `0` |
| `4` | `10000000` | `0` |
| `5` | `500000` | `0` |

## Consistency Requirement

Debit requests must never push a client past their configured credit limit. This implementation keeps that invariant in the database by calling `InsertTransacao()` for the balance update and limit check in one atomic operation.

## Constraints

The challenge imposes strict resource limits across all containers combined:

| Resource | Total budget | Where it goes in this repo |
|----------|--------------|----------------------------|
| CPU | `1.5` | API instances, PostgreSQL, and NGINX |
| Memory | `550MB` | API instances, PostgreSQL, and NGINX |
| Load | k6 stress script | Concurrent transactions and statement requests |

The observability sidecars and k6 runner are useful during local experiments, but the challenge budget centers on the application stack under test.

## Source

Full specification: [github.com/zanfranceschi/rinha-de-backend-2024-q1](https://github.com/zanfranceschi/rinha-de-backend-2024-q1)

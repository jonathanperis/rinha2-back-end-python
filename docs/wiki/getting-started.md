# Getting Started

## Prerequisites

- Docker with Docker Compose
- A local clone of this repository

## Clone and Run

```bash
git clone https://github.com/jonathanperis/rinha2-back-end-python.git
cd rinha2-back-end-python
docker compose up nginx -d --build
```

The `nginx` service depends on the two API containers, and each API waits for PostgreSQL health before starting.

## Access

The API is available at `http://localhost:9999`.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/clientes/{id}/transacoes` | `POST` | Submit debit or credit transaction |
| `/clientes/{id}/extrato` | `GET` | Get account balance statement |
| `/healthz` | `GET` | Health check |

## Smoke Check

```bash
curl http://localhost:9999/healthz
```

Expected response:

```text
Healthy
```

## Example Requests

### Create Transaction

```bash
curl -X POST http://localhost:9999/clientes/1/transacoes \
  -H "Content-Type: application/json" \
  -d '{"valor": 1000, "tipo": "c", "descricao": "deposito"}'
```

The response includes the client's credit limit and updated balance:

```json
{
  "limite": 100000,
  "saldo": 1000
}
```

### Get Statement

```bash
curl http://localhost:9999/clientes/1/extrato
```

The statement response contains the current balance envelope and the recent transaction list:

```json
{
  "saldo": {
    "total": 1000,
    "limite": 100000,
    "data_extrato": "2026-04-01T07:36:51"
  },
  "ultimas_transacoes": [
    { "valor": 1000, "tipo": "c", "descricao": "deposito" }
  ]
}
```

## Run Stress Tests

```bash
docker compose up k6 --build --force-recreate
```

The compose file supports a local observability loop with InfluxDB, Prometheus, Grafana, postgres-exporter, and the k6 web dashboard. The k6 service defaults to `MODE=dev` for local dashboard/export behavior; the production compose file uses `MODE=prod` and writes `./prod/conf/stress-test/reports/stress-test-report.html`, which `main-release.yml` uploads as the `stress-test-report` workflow artifact.

### Dev vs Production Compose

| Concern | `docker-compose.yml` | `prod/docker-compose.yml` |
|---------|----------------------|---------------------------|
| API image source | Builds from `./src/WebApi` | Pulls `ghcr.io/jonathanperis/rinha2-back-end-python:latest` |
| API host ports | `6665:8080` and `6666:8080` for direct instance access | `8081:8080` and `8082:8080` for direct instance access |
| Public ingress | NGINX on `9999:9999` | NGINX on `9999:9999` |
| k6 mode | `MODE=dev`, InfluxDB export enabled | `MODE=prod`, HTML report export enabled |
| Report output | local k6 dashboard / InfluxDB data | `./prod/conf/stress-test/reports/stress-test-report.html` |

### Local Observability Ports and Credentials

| Service | Port | Notes |
|---------|------|-------|
| Grafana | `3000` | Anonymous admin is enabled for the local dashboard loop. |
| Prometheus | `9090` | Reads `./prometheus/prometheus.yml`. |
| InfluxDB | `8086` | Requires `INFLUXDB_PASSWORD` and `INFLUXDB_TOKEN`. |
| postgres-exporter | `9187` | Exposes PostgreSQL metrics to Prometheus. |
| k6 web dashboard | `5665` | Enabled by `K6_WEB_DASHBOARD=true`. |

Set the InfluxDB values before starting k6/observability services, for example:

```bash
export INFLUXDB_PASSWORD=local-rinha-password
export INFLUXDB_TOKEN=local-rinha-token
```

## Troubleshooting Checklist

| Symptom | Check |
|---------|-------|
| `nginx` does not respond | `docker compose ps` and API container logs |
| API containers restart | PostgreSQL health, `DATABASE_URL`, and init scripts |
| Transactions return `422` | Payload type/description rules or credit-limit rejection |
| k6 cannot connect | Confirm `BASE_URL=http://nginx:9999` inside the compose network |
| Observability stack fails | Provide the required InfluxDB environment values before starting those services |

## Stop the Stack

```bash
docker compose down
```

Add `-v` when you intentionally want to remove the PostgreSQL volume and start from a fresh seed state.

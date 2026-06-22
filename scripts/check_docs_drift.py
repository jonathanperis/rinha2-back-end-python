#!/usr/bin/env python3
"""Source-backed README/wiki drift checks for rinha2-back-end-python.

This is intentionally lightweight: it parses the actual manifests, Docker/Compose
files, workflows, and docs text for high-value facts that have drifted before.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise AssertionError(message)


def require(text: str, needle: str, where: str) -> None:
    if needle not in text:
        fail(f"{where}: missing expected text: {needle!r}")


def forbid(text: str, needle: str, where: str) -> None:
    if needle in text:
        fail(f"{where}: stale text still present: {needle!r}")


def package_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for line in read("src/WebApi/requirements.txt").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            fail(f"requirements.txt line is not pinned: {line}")
        name, version = line.split("==", 1)
        versions[name] = version
    return versions


def app_clients() -> dict[int, int]:
    tree = ast.parse(read("src/WebApi/app.py"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "clientes":
                    value = ast.literal_eval(node.value)
                    return {int(k): int(v) for k, v in value.items()}
    fail("src/WebApi/app.py: clientes dict not found")


def sql_seed_clients(sql: str) -> dict[int, int]:
    match = re.search(
        r'COPY public\."Clientes" \("Id", "Limite", "SaldoInicial"\) FROM stdin;\n(.*?)\n\\\.',
        sql,
        re.S,
    )
    if not match:
        fail('rinha.dump.sql: Clientes seed COPY block not found')
    assert match is not None
    clients: dict[int, int] = {}
    for line in match.group(1).splitlines():
        client_id, limit, initial_balance = line.split("\t")
        if int(initial_balance) != 0:
            fail(f"rinha.dump.sql: expected zero initial balance for client {client_id}")
        clients[int(client_id)] = int(limit)
    return clients


def require_client_limit_table(text: str, where: str, clients: dict[int, int]) -> None:
    for client_id, limit in clients.items():
        require(text, f"| `{client_id}` | `{limit}`", where)


def main() -> int:
    versions = package_versions()
    dockerfile = read("src/WebApi/Dockerfile")
    compose = read("docker-compose.yml")
    prod_compose = read("prod/docker-compose.yml")
    sql = read("docker-entrypoint-initdb.d/rinha.dump.sql")
    docs_package = read("docs/package.json")
    astro_config = read("docs/astro.config.mjs")
    build_check = read(".github/workflows/build-check.yml")
    main_release = read(".github/workflows/main-release.yml")
    deploy = read(".github/workflows/deploy.yml")
    sidebar = read("docs/src/lib/sidebar.config.ts")
    docs_route = read("docs/src/pages/docs/[...slug].astro")

    docs = {
        "README.md": read("README.md"),
        "docs/README.md": read("docs/README.md"),
        "AGENTS.md": read("AGENTS.md"),
        "docs/wiki/home.md": read("docs/wiki/home.md"),
        "docs/wiki/architecture.md": read("docs/wiki/architecture.md"),
        "docs/wiki/getting-started.md": read("docs/wiki/getting-started.md"),
        "docs/wiki/performance.md": read("docs/wiki/performance.md"),
        "docs/wiki/ci-cd-pipeline.md": read("docs/wiki/ci-cd-pipeline.md"),
        "docs/wiki/challenge.md": read("docs/wiki/challenge.md"),
        "docs/src/components/home/Hero.astro": read("docs/src/components/home/Hero.astro"),
        "docs/src/components/home/Dashboard.astro": read("docs/src/components/home/Dashboard.astro"),
        "docs/src/pages/reports/index.astro": read("docs/src/pages/reports/index.astro"),
    }

    # Dependency versions reflected in public/operator docs.
    expected_versions = {
        "Flask": versions["Flask"],
        "Gunicorn": versions["gunicorn"],
        "psycopg2-binary": versions["psycopg2-binary"],
    }
    for label, version in expected_versions.items():
        for where in ["README.md", "AGENTS.md", "docs/wiki/architecture.md"]:
            require(docs[where], version, where)

    # Runtime shape from source/config.
    require(dockerfile, "python:3.14-slim", "src/WebApi/Dockerfile")
    require(dockerfile, '"--workers=4", "--threads=2"', "src/WebApi/Dockerfile")
    for where in ["README.md", "AGENTS.md", "docs/wiki/home.md", "docs/wiki/architecture.md"]:
        if where in {"README.md", "docs/wiki/architecture.md"}:
            require(docs[where], "| Python | 3.14 |", where)
        else:
            require(docs[where], "Python 3.14", where)
        require(docs[where], "4", where)
        require(docs[where], "2", where)

    clients = app_clients()
    if clients != {1: 100000, 2: 80000, 3: 1000000, 4: 10000000, 5: 500000}:
        fail(f"src/WebApi/app.py: unexpected clientes dict: {clients}")
    if sql_seed_clients(sql) != clients:
        fail("rinha.dump.sql: seeded client limits do not match app.py clientes dict")
    require(docs["docs/wiki/challenge.md"], "Client IDs are fixed to `1` through `5`", "docs/wiki/challenge.md")
    require(docs["README.md"], "| POST | `/clientes/{id}/transacoes` | Submit debit or credit transaction | 200, 400, 404, 422 |", "README.md")
    require(docs["docs/wiki/challenge.md"], "`400` for a missing JSON payload", "docs/wiki/challenge.md")
    for where in ["README.md", "docs/wiki/challenge.md"]:
        require_client_limit_table(docs[where], where, clients)

    # SQL physical design and stored-procedure semantics reflected in docs.
    for needle in [
        'CREATE UNLOGGED TABLE public."Clientes"',
        'CREATE UNLOGGED TABLE public."Transacoes"',
        'WITH (fillfactor = 90)',
        'CREATE INDEX "IX_Transacoes_ClienteId_Id_Desc"',
        'FOR UPDATE',
        'ORDER BY "Id" DESC',
        'LIMIT 10',
    ]:
        require(sql, needle, "docker-entrypoint-initdb.d/rinha.dump.sql")
    for needle in ["CREATE UNLOGGED TABLE", "IX_Transacoes_ClienteId_Id_Desc", "FOR UPDATE", "latest `10`"]:
        require(docs["docs/wiki/architecture.md"], needle, "docs/wiki/architecture.md")
    for needle in ["UNLOGGED hot tables", "IX_Transacoes_ClienteId_Id_Desc", "latest `10`"]:
        require(docs["docs/wiki/performance.md"], needle, "docs/wiki/performance.md")

    # Docs package metadata should reflect the Astro 7 static Pages upgrade.
    require(docs_package, '"astro": "7.0.0"', "docs/package.json")
    require(docs_package, '"vite": "^8.0.13"', "docs/package.json")
    forbid(docs_package, '"@astrojs/markdown-satteri"', "docs/package.json")
    require(docs_package, '"dev:background": "astro dev --background"', "docs/package.json")
    require(astro_config, "output: 'static'", "docs/astro.config.mjs")
    forbid(astro_config, "processor: satteri()", "docs/astro.config.mjs")
    forbid(astro_config, "src/fetch", "docs/astro.config.mjs")
    require(docs["docs/README.md"], "Astro `7.0.0`", "docs/README.md")
    require(docs["docs/README.md"], "Vite `8`", "docs/README.md")
    require(docs["docs/README.md"], "default Rust-powered Sätteri pipeline", "docs/README.md")
    require(docs["docs/README.md"], "server routing/cache providers and `src/fetch.ts` are intentionally not configured", "docs/README.md")

    # Compose resource envelope and service behavior.
    for needle in ['cpus: "0.4"', 'memory: "100MB"', 'cpus: "0.5"', 'memory: "330MB"', 'cpus: "0.2"', 'memory: "20MB"']:
        require(compose, needle, "docker-compose.yml")
    require(compose, "postgres:16.7-alpine", "docker-compose.yml")
    require(compose, "nginx:1.27-alpine", "docker-compose.yml")
    require(compose, "MODE=dev", "docker-compose.yml")
    for needle in ["6665:8080", "6666:8080", "9187:9187", "9090:9090", "3000:3000", "8086:8086", "5665:5665", "INFLUXDB_PASSWORD", "INFLUXDB_TOKEN"]:
        require(compose, needle, "docker-compose.yml")
    require(prod_compose, "MODE=prod", "prod/docker-compose.yml")
    for needle in ["8081:8080", "8082:8080", "9999:9999"]:
        require(prod_compose, needle, "prod/docker-compose.yml")
    require(prod_compose, "K6_WEB_DASHBOARD_EXPORT=./reports/stress-test-report.html", "prod/docker-compose.yml")
    for needle in [
        "Dev vs Production Compose",
        "6665:8080",
        "8081:8080",
        "INFLUXDB_PASSWORD",
        "INFLUXDB_TOKEN",
        "postgres-exporter",
        "k6 web dashboard",
    ]:
        require(docs["docs/wiki/getting-started.md"], needle, "docs/wiki/getting-started.md")

    # Workflow facts that docs should not overstate.
    require(build_check, "docker compose -f ./docker-compose.yml up nginx --wait", "build-check.yml")
    require(main_release, "paths-ignore:", "main-release.yml")
    require(main_release, "'docs/**'", "main-release.yml")
    require(main_release, "latest-arm64", "main-release.yml")
    require(main_release, "actions/upload-artifact@v7", "main-release.yml")
    require(main_release, "path: ./prod/conf/stress-test/reports/stress-test-report.html", "main-release.yml")
    require(deploy, "jonathanperis/.github/.github/workflows/pages-docs-deploy.yml@main", "deploy.yml")
    for needle in ["docs/**", "latest-arm64", "stress-test-report", "artifact"]:
        require(docs["docs/wiki/ci-cd-pipeline.md"], needle, "docs/wiki/ci-cd-pipeline.md")

    # Docs route and sidebar must cover every wiki file that should publish.
    wiki_slugs = {p.stem for p in (ROOT / "docs/wiki").glob("*.md")}
    sidebar_ids = set(re.findall(r'"([a-z0-9-]+)"', sidebar))
    if wiki_slugs - sidebar_ids:
        fail(f"docs/src/lib/sidebar.config.ts omits wiki slugs: {sorted(wiki_slugs - sidebar_ids)}")
    require(docs_route, "SECTION_CATEGORIES references id", "docs route build-time assertion")

    # Known stale phrases from older docs.
    stale_phrases = [
        "psycopg2-binary | 2.9.11",
        "psycopg2-binary 2.9.11",
        "All requests under 800ms at 250MB RAM usage",
        "health check (20 retries)",
        "k6 load test + GitHub Pages report",
        "archives report under `docs/public/reports/`",
        "archives HTML output under the public reports directory",
        "latest entries come from the mainline release workflow",
        "k6 load tests executed on every push to",
        "archived in CI reports",
        "CI stress tests · report archive",
    ]
    for where, text in docs.items():
        for phrase in stale_phrases:
            forbid(text, phrase, where)

    print("docs drift checks passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"docs drift check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)

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


def main() -> int:
    versions = package_versions()
    dockerfile = read("src/WebApi/Dockerfile")
    compose = read("docker-compose.yml")
    prod_compose = read("prod/docker-compose.yml")
    build_check = read(".github/workflows/build-check.yml")
    main_release = read(".github/workflows/main-release.yml")
    deploy = read(".github/workflows/deploy.yml")
    sidebar = read("docs/src/lib/sidebar.config.ts")
    docs_route = read("docs/src/pages/docs/[...slug].astro")

    docs = {
        "README.md": read("README.md"),
        "CLAUDE.md": read("CLAUDE.md"),
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
        for where in ["README.md", "CLAUDE.md", "docs/wiki/architecture.md"]:
            require(docs[where], version, where)

    # Runtime shape from source/config.
    require(dockerfile, "python:3.14-slim", "src/WebApi/Dockerfile")
    require(dockerfile, '"--workers=4", "--threads=2"', "src/WebApi/Dockerfile")
    for where in ["README.md", "CLAUDE.md", "docs/wiki/home.md", "docs/wiki/architecture.md"]:
        if where in {"README.md", "docs/wiki/architecture.md"}:
            require(docs[where], "| Python | 3.14 |", where)
        else:
            require(docs[where], "Python 3.14", where)
        require(docs[where], "4", where)
        require(docs[where], "2", where)

    clients = app_clients()
    if clients != {1: 100000, 2: 80000, 3: 1000000, 4: 10000000, 5: 500000}:
        fail(f"src/WebApi/app.py: unexpected clientes dict: {clients}")
    require(docs["docs/wiki/challenge.md"], "Client IDs are fixed to `1` through `5`", "docs/wiki/challenge.md")

    # Compose resource envelope and service behavior.
    for needle in ['cpus: "0.4"', 'memory: "100MB"', 'cpus: "0.5"', 'memory: "330MB"', 'cpus: "0.2"', 'memory: "20MB"']:
        require(compose, needle, "docker-compose.yml")
    require(compose, "postgres:16.7-alpine", "docker-compose.yml")
    require(compose, "nginx:1.27-alpine", "docker-compose.yml")
    require(compose, "MODE=dev", "docker-compose.yml")
    require(prod_compose, "MODE=prod", "prod/docker-compose.yml")
    require(prod_compose, "K6_WEB_DASHBOARD_EXPORT=./reports/stress-test-report.html", "prod/docker-compose.yml")

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

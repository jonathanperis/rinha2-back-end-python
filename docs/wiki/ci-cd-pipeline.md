# CI/CD Pipeline

## Workflows

This repository uses four GitHub Actions workflows:

| Workflow | File | Trigger | Description |
|----------|------|---------|-------------|
| Build Check | `build-check.yml` | Pull requests | Docker build + health check before merge |
| Main Release | `main-release.yml` | Push to `main` | Multi-platform Docker push to GHCR, container test, and k6 report generation |
| CodeQL | `codeql.yml` | Push, PRs, weekly | Security and code-quality analysis |
| Deploy | `deploy.yml` | Push to `main` | Deploy `docs/` to GitHub Pages |

## Pull Request Gate

PRs validate the container path before merge:

1. Build the production compose stack.
2. Start the service set required for the API.
3. Probe `/healthz` with retries until the application is ready.
4. Run CodeQL for Python/security analysis.

This catches container build failures, dependency regressions, and startup problems before they reach `main`.

## Main Release

`main-release.yml` is the evidence-producing workflow. On a push to `main`, it:

1. Builds a multi-platform Docker image (`linux/amd64`, `linux/arm64`).
2. Pushes the image to GitHub Container Registry.
3. Runs a container health check against the production compose stack.
4. Runs k6 load tests.
5. Archives the stress-test report under `docs/public/reports/` so it can be published by GitHub Pages.

Published image:

```text
ghcr.io/jonathanperis/rinha2-back-end-python:latest
```

## Pages Deployment

`deploy.yml` publishes the static documentation site to GitHub Pages from the `docs/` package. The published site includes:

- The docs hub and wiki pages.
- The homepage proof narrative.
- The stress-test report index.
- Archived k6 HTML reports.

After a docs PR merges to `main`, the deployment run should complete before the live URL is treated as updated.

## Release Evidence Loop

```text
PR branch
  ├─ build-check.yml validates container startup
  └─ codeql.yml scans the change
       │
       ▼
main merge
  ├─ main-release.yml builds image + runs k6 + archives report
  └─ deploy.yml publishes docs and report archive to Pages
```

## Where to Look

- [GitHub Actions](https://github.com/jonathanperis/rinha2-back-end-python/actions) for workflow status.
- [Stress test reports](/rinha2-back-end-python/reports/) for archived k6 output.
- [GHCR package](https://github.com/jonathanperis/rinha2-back-end-python/pkgs/container/rinha2-back-end-python) for published images.

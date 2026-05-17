# CI/CD Pipeline

## Workflows

This repository uses four GitHub Actions workflows:

| Workflow | File | Trigger | Description |
|----------|------|---------|-------------|
| Build Check | `build-check.yml` | Pull requests to `main` and manual dispatch | Builds/starts the development Compose stack with `docker compose -f ./docker-compose.yml up nginx --wait`, then probes `/healthz`. |
| Main Release | `main-release.yml` | Pushes to `main` except `docs/**`, plus manual dispatch | Builds/pushes GHCR images, creates the multi-arch `latest` manifest, runs the production compose health check, runs k6, and uploads the HTML report as an artifact. |
| CodeQL | `codeql.yml` | Pushes to `main`, PRs to `main`, weekly schedule | Runs Python security-and-quality analysis. |
| Deploy to GitHub Pages | `deploy.yml` | Pushes to `main` and manual dispatch | Calls the shared `jonathanperis/.github` Pages workflow to build and deploy `docs/` with Bun. |

## Pull Request Gate

PRs validate the container path before merge:

1. Check out the full repository.
2. Build and start the development Compose stack with `docker compose -f ./docker-compose.yml up nginx --wait`.
3. Probe `http://localhost:9999/healthz` once after Compose reports the service ready.
4. Run CodeQL for Python security-and-quality analysis.

This catches container build failures, dependency regressions, and startup problems before they reach `main`.

## Main Release

`main-release.yml` is the image-and-artifact workflow. On a non-doc push to `main`, it:

1. Builds and pushes the amd64 image as `ghcr.io/jonathanperis/rinha2-back-end-python:latest`.
2. Builds and pushes the arm64 image as `ghcr.io/jonathanperis/rinha2-back-end-python:latest-arm64`.
3. Merges both digests into the multi-architecture `latest` manifest.
4. Starts the production compose stack and retries `/healthz` up to 20 times.
5. Runs k6 with `prod/docker-compose.yml` (`MODE=prod`).
6. Uploads `./prod/conf/stress-test/reports/stress-test-report.html` as the `stress-test-report` Actions artifact.

The workflow intentionally ignores `docs/**` pushes, so documentation-only merges deploy Pages without rebuilding images or running k6.

## Report Publication Model

There are two report lanes:

| Lane | Source | Where to inspect |
|------|--------|------------------|
| Latest release artifact | `main-release.yml` k6 job output | The `stress-test-report` artifact attached to the workflow run |
| Published historical archive | Committed files under `docs/public/reports/*.html` | [Stress test reports](/rinha2-back-end-python/reports/) on GitHub Pages |

A release artifact does not automatically rewrite the committed Pages archive. Promote a new artifact into `docs/public/reports/` only when it should become part of the public historical record.

## Pages Deployment

`deploy.yml` publishes the static documentation site to GitHub Pages from the `docs/` package. The published site includes:

- The homepage proof narrative.
- The docs hub and wiki pages.
- The stress-test report index.
- Committed historical k6 HTML reports.

After a docs PR merges to `main`, the deployment run should complete before the live URL is treated as updated.

## Release Evidence Loop

```text
PR branch
  ├─ build-check.yml validates container startup
  └─ codeql.yml scans the change
       │
       ▼
main merge
  ├─ main-release.yml builds images + runs k6 + uploads report artifact
  │   └─ skipped for docs/**-only pushes
  └─ deploy.yml publishes docs and committed report archive to Pages
```

## Where to Look

- [GitHub Actions](https://github.com/jonathanperis/rinha2-back-end-python/actions) for workflow status.
- [Stress test reports](/rinha2-back-end-python/reports/) for committed historical k6 output.
- [GHCR package](https://github.com/jonathanperis/rinha2-back-end-python/pkgs/container/rinha2-back-end-python) for published images.

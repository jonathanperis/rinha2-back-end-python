# CI/CD Pipeline

## Workflows

This repository uses four GitHub Actions workflows:

| Workflow | File | Trigger | Description |
|----------|------|---------|-------------|
| Build Check | `build-check.yml` | Pull requests | Docker build + health check (20 retries) |
| Main Release | `main-release.yml` | Push to main | Multi-platform Docker push (amd64/arm64) to GHCR + container test + k6 load test |
| CodeQL | `codeql.yml` | Push to main, PRs, weekly | Security and code quality analysis |
| Deploy | `deploy.yml` | Push to main | Deploy docs to GitHub Pages via Actions |

### build-check.yml

- **Trigger:** Pull requests
- **Steps:** Builds the API container with Docker Compose and runs a health check endpoint test (20 retries) to verify the service starts correctly
- **Purpose:** Catch build failures and regressions before merging

### main-release.yml

- **Trigger:** Push to main branch
- **Steps:**
  1. Builds a multi-platform Docker image (linux/amd64, linux/arm64) and pushes to GitHub Container Registry (GHCR)
  2. Runs a container health check test against the production compose stack
  3. Runs k6 load tests and commits the stress test report to `docs/reports/`
- **Purpose:** Automated release of production-ready container images with verification
- **Image:** `ghcr.io/jonathanperis/rinha2-back-end-python:latest`

### codeql.yml

- **Trigger:** Push to main, pull requests, weekly schedule
- **Steps:** Runs GitHub CodeQL analysis for security vulnerabilities and code quality
- **Purpose:** Continuous security scanning

### deploy.yml

- **Trigger:** Push to main branch
- **Steps:** Deploys the `docs/` directory to GitHub Pages using `actions/deploy-pages`
- **Purpose:** Publish documentation and stress test reports to GitHub Pages

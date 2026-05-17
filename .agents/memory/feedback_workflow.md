---
name: Workflow Conventions
description: Branch+PR strategy, rebase-only merges, gh CLI preference for all repo changes
type: feedback
---

All changes to repositories must go through a feature branch + pull request. Never commit directly to main.

**Why:** User enforces a strict branch protection workflow across all repos to maintain clean history and code review.

**How to apply:**
- Always create a feature branch before making changes
- Open a PR using `gh pr create` (never push directly to main)
- PRs use rebase-only merge strategy — no merge commits, no squash
- Use `gh` CLI for all GitHub operations (repos, PRs, issues, releases, checks)

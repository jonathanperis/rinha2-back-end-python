# Docs

Astro static site deployed to GitHub Pages.

## Commands

Run from this directory (`docs/`):

| Command | Action |
|---|---|
| `bun install` | Install dependencies |
| `bun run dev` | Start dev server |
| `bun run build` | Build to `./out/` |
| `bun run preview` | Preview production build locally |
| `bun run lint` | Run `astro check` diagnostics |
| `bun run check:drift` | Verify README/wiki source facts against code, Compose, and workflows |

## Environment

Copy `.env.example` to `.env` and fill in local values when needed.

| Variable | Description |
|---|---|
| `PUBLIC_GA_ID` | Optional Google Analytics 4 Measurement ID |

# Docs

Astro `7.0.0` static site deployed to GitHub Pages with Vite `8`. Markdown pages use Astro 7's default Rust-powered Sätteri pipeline; the site stays `output: 'static'` for GitHub Pages, so server routing/cache providers and `src/fetch.ts` are intentionally not configured here.

## Commands

Run from this directory (`docs/`):

| Command | Action |
|---|---|
| `bun install` | Install dependencies |
| `bun run dev` | Start dev server |
| `bun run dev:background` | Start Astro 7's managed background dev server for agent-friendly local previews |
| `bun run build` | Build to `./out/` |
| `bun run preview` | Preview production build locally |
| `bun run lint` | Run `astro check` diagnostics |
| `bun run check:drift` | Verify README/wiki source facts against code, SQL, Compose, workflows, and docs package metadata |

## Environment

Copy `.env.example` to `.env` and fill in local values when needed.

| Variable | Description |
|---|---|
| `PUBLIC_GA_ID` | Optional Google Analytics 4 Measurement ID |

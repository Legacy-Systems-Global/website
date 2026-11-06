# AGENTS.md

Guidance for any coding agent (Claude Code, Codex, Cursor…) and humans working in this repo. This file is authoritative; `CLAUDE.md` just imports it.

**Read first:** `PROJECT.md` (what we're building and why) and `STATUS.md` (current state, blockers, next action). Update `STATUS.md` whenever you change infrastructure, CI, hosting or setup.

## Project
The public website for Legacy Systems Global.
Platform: web · Stack: HTML + Tailwind CSS v4, built with Vite (npm)

## Commands
- Install: `npm install` (CI uses `npm ci`)
- Run / preview: `npm run dev` (serves at `/website/`, e.g. http://localhost:5173/website/)
- Regenerate content: `npm run content` (Python 3, no third-party packages)
- Build: `npm run build` (regenerates content, then static output in `dist/`)
- Verify built links/assets: `python3 scripts/verify-site.py`
- Lint: none configured yet
- Test: none configured yet

## Layout
- Top-level `*.html` — generated static Vite entries
- `content/editorial-copy.md` — source copy; `content/layout-source.html` — retained approved layout
- `content/extensions.css` and `content/experiences.css` — additional page styles
- `scripts/build-pages.py` — page generator; `scripts/experiences.py` — audience and concept templates
- `src/experiences.js` — audience navigation, dialogs, stepped assessment, preference/newsletter/contact prototypes
- `src/site.js` — shared browser interactions; `src/site.css` and `src/products.json` — generated
- `COPY_REVIEW.md` — editorial decisions and demonstration boundaries
- `public/` — static files copied as-is
- `vite.config.js` — Tailwind plugin and `base: '/website/'` (switch to `'/'` if a custom domain is added)
- `.github/workflows/` — `ci.yml` (build on push/PR), `deploy.yml` (manual Pages deploy from `main`)

## Environment variables
None yet.
Names only — values live in `.env.local` (git-ignored). `.env.example` lists them with placeholders.

## Branches and releases
- `dev` is the default branch: do all work there or on short-lived branches off it.
- `main` is production and is protected: changes reach it only by a pull request from `dev`.
- **Never release to production unless a human explicitly asks.** Production deploys run manually from `main` (`gh workflow run deploy.yml --ref main`).
- CI must pass before merging.

## Rules
- Never commit secrets, keys, certificates or signing assets.
- Don't discard or overwrite someone's uncommitted changes; ask first.
- Match the existing code style and run the build before committing.

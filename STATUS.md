# Status

_Last updated: 2026-10-08 17:51 EDT · branch `dev` · commit `5d1726b` (plus this update)_
_Set up from: Claude Code on Alex's Mac (directly)_

## Done and verified
- Repo created: https://github.com/Legacy-Systems-Global/website (public; org is on GitHub Free)
- Branches `main` and `dev` pushed; `dev` is the default branch
- `main` protected: PR required (0 approvals), no force-push or deletion, admins can bypass
- Dependabot alerts + security updates on; version updates target `dev` weekly (npm, GitHub Actions)
- CI (`npm ci` + `npm run build`) passed on `dev` for the initial commit
- Production build verified locally: `dist/` with assets under `/website/`
- GitHub Pages enabled (source: GitHub Actions); `github-pages` environment restricted to `main`
- Local preview served and returned HTTP 200

## Preview
- Command: `npm run dev -- --host 127.0.0.1 --port 5173 --strictPort`
- URL: http://127.0.0.1:5173/website/
- PID / log: 16628 (at setup; may no longer be running) · `~/Library/Logs/website-dev.log`
- Restart: `cd ~/Documents/GitHub/website && nohup npm run dev -- --host 127.0.0.1 --port 5173 > ~/Library/Logs/website-dev.log 2>&1 &`

## Production
Not deployed. When released it will be at https://legacy-systems-global.github.io/website/ (no custom domain).
Release: PR `dev` → `main`, then `gh workflow run deploy.yml --ref main`.

## Pending and blockers
- Custom domain: none chosen; if added, switch `base` in `vite.config.js` to `'/'`
- Rams.ai GitHub App: not installed (no install URL configured) — add this repo manually
- Pushing: SSH to GitHub was denied from the setup shell (key not loaded in ssh-agent), so this repo's remote uses HTTPS
- No lint or tests configured yet

## Next action
Landing page (from claude.ai design "Legacy Systems Landing v2") built and merged to `main`; not yet deployed. Open question: contact address — page uses `submit@legacysystems.global` (design linked `touch@`).

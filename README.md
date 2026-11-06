# Legacy Systems Global — Website

Static multi-page website built with Vite. Local checkout: `~/Documents/GitHub/website`.

```sh
npm install
npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Preview: http://127.0.0.1:5173/website/

```sh
npm run build
python3 scripts/verify-site.py
```

Python 3 is used for dependency-free content generation. Vite emits all top-level HTML entries for direct navigation on GitHub Pages. The `/website/` base is intentional.

See `COPY_REVIEW.md` for copy decisions, editing instructions, and prototype boundaries. Read `AGENTS.md`, `PROJECT.md`, and `STATUS.md` before making changes. Develop on `dev`; release to production only when explicitly requested.

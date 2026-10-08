# Legacy Systems Global — Website

The public website for Legacy Systems Global.

## Brief
"Create a new project for Legacy Systems" — the organization's website, living in the `Legacy-Systems-Global` GitHub org. No further brief was supplied at setup.

## Audience and purpose
The public website for Legacy Systems Global. Specific audience, goals and content are pending.

## Platform and stack
- Platform: web
- Stack: HTML + Tailwind CSS v4, built with Vite; npm
- Why: chosen by Alex — a simple, fast static site with no framework overhead; easy to move to Astro or Next.js if it grows into a multi-page or content-heavy site.

## Hosting and domain
GitHub Pages, deployed manually from `main` only. No custom domain: the site will be served at `https://legacy-systems-global.github.io/website/` once released (hence `base: '/website/'` in `vite.config.js`). If a domain is added later, set `base: '/'` and follow the custom-domain steps.

## Setup scope
Setup created the repo, starter, CI, preview and these records. It did **not** build product features.

## Open assumptions
- Repo is public (org is on GitHub Free; public was chosen so Pages and branch protection work).
- Audience, content, sections and brand are unknown.
- Whether a custom domain will be used is unknown.

## First-build plan (for the next agent — not part of setup)
1. Gather from Alex: who the site is for, what Legacy Systems Global does, key pages/sections, brand (logo, colors, type), and contact method.
2. Build the home page in `index.html` with Tailwind; add more pages as extra Vite inputs if needed (or move to Astro if content grows).
3. Add basic SEO/meta (title, description, Open Graph image) and a favicon.
4. Release only when Alex asks.

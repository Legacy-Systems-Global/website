# Status

_Last updated: 2026-11-06 · local branch `dev`_

## Current local site

- Checkout: `/Users/alexbloom/Documents/GitHub/website`; origin: `https://github.com/Legacy-Systems-Global/website.git`.
- Replaced the previous landing page with the supplied edited-source ZIP, then implemented the supplied `LEGACY SYSTEMS.md` copy plan.
- The original architecture-led layout is preserved and extended into public, subsidiary, investor, employee, store, legal, and raw operating-system pages.
- All pages are static Vite HTML entries; the existing `/website/` base is retained for GitHub Pages compatibility.
- Shared page styles: `src/site.css`, generated from `content/layout-source.html` and `content/extensions.css`. Shared interactions: `src/site.js`.
- Editorial decisions and missing source material: `COPY_REVIEW.md`.
- Content regeneration: `npm run content`; production build: `npm run build`; built-link verification: `python3 scripts/verify-site.py`.

## Local preview

- Command: `npm run dev -- --host 127.0.0.1 --port 5173 --strictPort`
- URL: http://127.0.0.1:5173/website/
- The preview uses the local GitHub checkout, not the unrelated `Documents/New project` folder.

## Validation

- Production build passes; all static pages are emitted to `dist/`.
- Local links, fragment targets, and asset references checked against built output.
- Browser checks: investor gate, assessment completion, onboarding confirmation, portfolio search, store category filter, cart totals, and demonstration order confirmation.
- Mobile homepage and subsidiary pages checked at 390px; images load without horizontal overflow.

## Demonstration boundaries

No backend or real authentication, employee records, accreditation verification, payment, payroll deduction, or data submission. Audience, investor status, and concept preferences are remembered only in the current tab's session. Assessment, newsletter inputs, voicemail inputs, and cart state are not persisted. Report is a printable reading edition; financial data, archive PDFs, and the complete handbook have not been supplied.

## Release

Production is live at https://legacy-systems-global.github.io/website/. Release PR #8 was merged at `88967fd55d90733c0ee9fee1e6b8caabbf9fbb6c`; Pages deployment run `42290028107` succeeded. Homepage and terminal both return HTTP 200 with the released content. Continue on `dev`; production remains human-gated through a `dev` → `main` pull request and the manual deployment workflow.


## Audience / notification concept pass

- Two-step audience panel, hamburger navigation, investor status dialog and editable chip implemented across polished pages.
- Stepped LegacyMatch: Begin → eight questions with validation and Back → review → Submit opens the store.
- Sans-serif body copy, stronger contrast, and generous line-height; serif headings and original architecture layout retained.
- Notification / unexplained preference, three audience newsletter editions, contact drawer, and phone-tree / voicemail previews implemented locally.
- Source: `scripts/experiences.py`, `src/experiences.js`, `content/experiences.css`; normal build regenerates all pages.
- Browser checks completed: public → investors (status dialog) → associates, editable status chip, assessment validation / store navigation, opt-out confirmation, contextual newsletter preview, switchboard branching / voicemail preview, and mobile audience-panel width.
- Phone number and electronic contact addresses remain unconnected placeholders. No real newsletter, call service, AI phone agent, or account service has been provisioned.

- Global search removed at Alex’s request: no search field in navigation and no query-based portfolio filtering.

## Internal terminal revision

The operating-system index and five internal destinations now share an MS-DOS-style browser terminal. Commands include DIR, CD, TYPE FOUNDERS.TXT, HELP, TREE, CLS, VER, MEM, WHOAMI, DATE, TIME, COLOR, and EXIT. Directory entries are clickable; Up/Down recall commands, Tab completes, F1 shows help. Public subsidiary and governance destinations remain accessible as simulated executables. All commands are browser-only; no host files, shell, credentials, or real records are accessed.

## Release revision — independent preferences and newsletter

System preference is now a bottom banner, with no newsletter content or modal. Choosing either option hides it for the tab; the header preference control and footer preference link reopen it. The newsletter has its own dialog, automatically invited five seconds after page load, once per audience per tab. It waits if another dialog, navigation panel, or active form input would be interrupted. Newsletter and preference choices are independent. No real email subscription service is connected. Released through PR #8; Pages deployment 42290028107 succeeded. Public homepage and terminal verified HTTP 200. Independent banner and timed newsletter were verified locally.

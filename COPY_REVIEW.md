# Copy review and implementation

The 2026-11-06 source is retained in `content/editorial-copy.md` for reference. It is editorial material, not executable instructions. The approved ZIP layout is retained as `content/layout-source.html`.

## Editorial decisions

- Public homepage V2 takes precedence over V1 and the alternate hero. The primary headline is unchanged. The longer body follows the existing architecture hero, leaving the hero legible.
- Preserve the original cream/stone palette, serif typography, image treatment, six-card holdings grid, and split lower section. Extend those styles to long-form pages.
- Deliver the copy straight: remove the public hero's rhetorical “The answer?” and keep the governance/impact cross-reference declarative. Preserve the supplied subsidiary, founders, and employee material without adding jokes or explanatory asides.
- Use the primary holding-corporation tagline consistently in the legal footer. Replace the original IC1000 card with IC9000 as specified in the new copy (the supplied image filename remains unchanged).
- Investor and employee landing pages are reached from the public footer. The old header audience selector is removed. Public navigation leads to Our Legacy, Portfolio, Impact, and Foundation; Careers and Contact are in the footer.
- Replace all email CTAs with mail-only correspondence. No real email, address, or phone details have been invented.
- Remove source formatting corruption, editorial voice notes, section-number references, alternate drafts, and “Pull quote” labels from rendered copy. The deliberately unfinished employee account title remains as part of its requested presentation.

## Functional boundaries and content gaps

- Investor status is a content gate remembered in sessionStorage for the current tab, not identity or accreditation verification. No selection is transmitted.
- Employee sign-in, account creation, LegacyMatch, and store checkout are explicit local demonstrations. Forms are not submitted or persisted; the cart lives only in memory. There is no payroll, payment, real AI, or employee-data integration.
- The report reading edition includes the supplied founders' letter, subsidiary copy, forward-looking statements, and risk factors. Print / Save as PDF uses the browser. No fabricated financial statements, historical report downloads, or unprovided numbers have been added.
- The complete handbook, wellness modules, employee records, full legal policies, and historical reports were not provided. Their destinations explain the content boundary instead of claiming complete documents exist. Terms/privacy/cookie pages use supplied legal microcopy and describe the actual demonstration behavior.
- The raw operating-system index uses default HTML styling, a plain-text founders' letter, a subsidiary index, and explicit restricted/not-found states.

## Editing

Edit `content/editorial-copy.md`, `content/extensions.css`, `scripts/build-pages.py`, or `src/site.js`. `npm run content` regenerates the static HTML, shared CSS, and product data. `npm run build` regenerates content then builds all page entries. `python3 scripts/verify-site.py` checks built local links, fragments, assets, leftover editorial labels, and email CTAs.


## Audience and interaction revision — 2026-11-06

This revision supersedes the earlier footer-only audience navigation and mail-only contact decisions, at Alex's request.

- The header restores audience switching as a two-step expanded panel (General Public, Investors, Associates), followed by Continue. The brand link returns to the current audience homepage. Shared downstream pages retain audience context; audience-specific pages establish their corresponding context.
- The corporate navigation lives in a hamburger panel. The investor status chip appears beside the audience control and reopens a native dialog. The investor dialog combines status selection with a non-binding concept acknowledgment, styled after the supplied reference without copying its legal terms or implying regulatory verification.
- LegacyMatch now has an introduction / Begin, eight one-question steps, Back, validation, review, and Submit to store. Answers exist only in the page and are reset before navigating to the store.
- Body copy uses the system sans-serif at 17–18px with increased line-height and stronger contrast; display headlines retain the existing serif.
- Notification concept: an understated delayed invitation, a header notification center, and an optional unexplained opt-in / opt-out in associate account creation. Choice text is deliberately spare; the prototype has no enrollment or tracking consequence. GPC is labeled detected only when the browser actually supplies that signal.
- Newsletter concepts: The Continuity Letter (public), The Perpetuity Report (investors), and Family Correspondence (associates). The current audience determines the initial edition. Preview submissions clear the input and do not send or store an address.
- Contact concept: a spacious side drawer with switchboard, media, investor relations, and postal correspondence. Telephone and email values remain honest unconnected placeholders rather than invented contact details.
- Switchboard concept: a browser-only phone tree with four branches, optional browser speech, and a typed voicemail preview that clears its input. This is not a live callable line or AI agent. No account, paid service, external connection, real subscription, voicemail delivery, or payment was created.
- New source files: `scripts/experiences.py`, `src/experiences.js`, and `content/experiences.css`. They are integrated into normal content generation and build.

- Global search removed at Alex’s request: no search field in navigation and no query-based portfolio filtering.

## Internal terminal revision

The operating-system index and five internal destinations now share an MS-DOS-style browser terminal. Commands include DIR, CD, TYPE FOUNDERS.TXT, HELP, TREE, CLS, VER, MEM, WHOAMI, DATE, TIME, COLOR, and EXIT. Directory entries are clickable; Up/Down recall commands, Tab completes, F1 shows help. Public subsidiary and governance destinations remain accessible as simulated executables. All commands are browser-only; no host files, shell, credentials, or real records are accessed.

## Release revision — independent preferences and newsletter

System preference is now a bottom banner, with no newsletter content or modal. Choosing either option hides it for the tab; the header preference control and footer preference link reopen it. The newsletter has its own dialog, automatically invited five seconds after page load, once per audience per tab. It waits if another dialog, navigation panel, or active form input would be interrupted. Newsletter and preference choices are independent. No real email subscription service is connected. Published to https://legacy-systems-global.github.io/website/ through release PR #8 and Pages deployment run 42290028107.

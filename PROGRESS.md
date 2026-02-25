# Progress Log

## Project Status: COMPLETE — Site is live and deployed at https://www.andrew-mceachin.com

---

## Phase 5: Final Polish, Deployment & Go-Live (2026-02-24)

### Completed — Site-Wide Visual Consistency
- [x] Applied mountain sketch backdrop to ALL pages (previously publications-only)
- [x] Widened all content pages (not just publications) with left-alignment and matching font size (1.05rem)
- [x] Right-aligned navigation menu items
- [x] Removed CV page from nav menu (redundant — Download CV button exists on profile section)

### Completed — Bug Fixes
- [x] Fixed news coverage section on Commentary & Media page — was displaying publication IDs instead of human-readable titles. Built a title lookup from publications data to resolve references correctly.
- [x] Fixed invisible bold text in prose sections — Tailwind dark mode was overriding `<strong>` tag color. Added `.prose strong { color: #1b4965 !important }` to custom CSS.
- [x] Fixed Hugo dev server rendering corruption — stopped old server process, performed clean rebuild

### Completed — Deployment & Domain Configuration
- [x] Made GitHub repository public
- [x] Enabled GitHub Pages with GitHub Actions as build source
- [x] Configured custom domain: `www.andrew-mceachin.com`
- [x] DNS configured via Squarespace: CNAME record + A records pointing to GitHub Pages IPs
- [x] HTTPS enforcement enabled on GitHub Pages
- [x] Site is LIVE at https://www.andrew-mceachin.com

---

## Phase 4b: Publications Page Polish (completed prior to Phase 5)

### Completed — Theme Reorganization
All 63 publications grouped into 4 collapsible research themes using native `<details>/<summary>`. Themes sorted by publication count (largest first).

### Completed — Page Polish
- [x] Research agenda introduction paragraph above theme sections
- [x] Mountain sketch backdrop on publications page (fixed positioning, persists on expand)
- [x] Reduced whitespace between nav header and content
- [x] Fixed article width so collapsed/expanded sections match
- [x] Always-visible theme descriptions (2-3 sentences each) inside `<summary>`
- [x] Cleaned up 131 macOS Finder duplicate files
- [x] All changes committed and pushed

### Files Modified (Phase 4b)
- `data/publications.yaml` — `theme_order` with `description` field, `theme` on all 63 entries
- `scripts/utils.py` — Theme validation + `filter_pubs_by_theme()` helper
- `scripts/sync_hugo.py` — Collapsible themes, intro text, theme descriptions in summary, type badges
- `site/assets/css/custom.css` — Theme sections, mountain backdrop (fixed), spacing, descriptions, responsive
- `README.md` — Updated to reflect themed layout
- `PROCESS-LOG.md` — Added Phase 4b entry

---

## Session 2026-02-24 (final): Code Review, Hardening & Deploy Optimization

### Completed — Code Review & Engineering Fixes
- [x] Ran `/datascience-reviewer` code review on the full project
- [x] Removed dead `format_citation()` function from `scripts/utils.py`
- [x] Hardened `_yaml_escape` in `scripts/sync_hugo.py` for control characters (`\n`, `\r`, `\t`)
- [x] Consolidated duplicate CSS `:root` blocks in `site/assets/css/custom.css`
- [x] Added `site/.hugo_build.lock` and `*.Rhistory` to `.gitignore`

### Completed — Test Suite
- [x] Added 27 tests in `tests/test_citations.py` covering `format_authors`, `_format_citation_html`, `_html_escape`, `_yaml_escape`, and `latex_escape`

### Completed — Branding Assets
- [x] Added mountain backdrop as favicon (`site/assets/media/icon.png`)
- [x] Added mountain backdrop as social sharing image (`site/assets/media/sharing.png`)

### Completed — Deploy Workflow Simplification
- [x] Simplified GitHub Actions deploy workflow: removed TeX Live installation step
- [x] CI now runs only `sync_hugo.py` + Hugo build; pre-built CV PDF is committed to repo
- [x] Deploy time reduced from ~10 min to ~2 min
- [x] Cancelled stuck GitHub Actions deploy that was blocking the queue for 40+ minutes

### Completed — Mountain Backdrop Positioning
- [x] Fixed mountain backdrop positioning: fixed 2200px width (no rescaling), anchored below navbar with z-index layering, peaks always visible via top-anchoring

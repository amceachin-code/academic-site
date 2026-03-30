# Progress Log

## Project Status: COMPLETE — Add Focus Columns to Article Tracking System

---

## Previous Task: COMPLETE — Add "Focus" Columns to Article Tracking System (2026-03-16)

### Objective
Add two Focus columns (Primary Focus and Secondary Foci) to the article tracking system. This includes updating the Excel workbook, the init script, the /split-pdf skill, and the duplicate checker.

### Plan
1. Add two Focus columns to `articles/articles.xlsx` (insert after Outcome col G, backfill 7 existing rows)
2. Update `scripts/init_articles_workbook.py` (add FOCUS_CODES, update headers, column widths, Codes sheet, auto-filter)
3. Update `/split-pdf` SKILL.md (add Focus to Steps 6 and 7)
4. Update `scripts/check_duplicate.py` (update Source Link column index)

### Progress
- [x] Step 1: Add two Focus columns to `articles/articles.xlsx`
- [x] Step 2: Update `scripts/init_articles_workbook.py`
- [x] Step 3: Update `/split-pdf` SKILL.md
- [x] Step 4: Update `scripts/check_duplicate.py`

### Status: ALL 4 STEPS COMPLETED SUCCESSFULLY.

### Step Details

**Step 1 (DONE):** Added Primary Focus (col H) and Secondary Foci (col I) columns to `articles/articles.xlsx`. Backfilled all 7 existing rows with correct focus codes. Updated auto-filter range to E1:J1000. Added Focus code comments to headers. Added Focus table to Codes reference sheet.

**Step 2 (DONE):** Updated `scripts/init_articles_workbook.py`. Added FOCUS_CODES dict, updated ARTICLES_HEADERS and ARTICLES_COL_WIDTHS, updated auto-filter range, added data validation for Focus columns, added cell comments, updated seed row, and added Focus table to Codes sheet.

**Step 3 (DONE):** Updated `/split-pdf` SKILL.md. Added Primary Focus and Secondary Foci to Step 6 (auto-assign codes) and Step 7 (add row to xlsx with correct column indices).

**Step 4 (DONE):** Updated `scripts/check_duplicate.py`. Changed Source Link from col J (index 9) to col L (index 11) in both `check_by_filename` and `check_by_title` functions.

### Key Decisions
- Primary Focus: single value from a defined code list
- Secondary Foci: comma-separated values from the same code list
- Columns inserted after Outcome (col G), shifting Source Link and other columns right

### Files Modified
- `articles/articles.xlsx` (in ed-in-america project; added Focus columns, backfilled existing rows)
- `scripts/init_articles_workbook.py` (in ed-in-america project; FOCUS_CODES, headers, column widths, Codes sheet, auto-filter)
- `/Users/andrewmceachin/Desktop/.claude/skills/split-pdf/SKILL.md` (added Focus to Steps 6 and 7)
- `scripts/check_duplicate.py` (in ed-in-america project; updated Source Link column index)

---

## Previous Task: COMPLETE — Implement Article Tracking System (2026-03-15)

### Objective
Build an article tracking system for the Education in America report project. This includes an Excel workbook with tracking and codes reference sheets, a PDF splitting script, a `/split-pdf` Claude Code skill, and CLAUDE.md documentation updates.

### Plan
1. Create `scripts/init_articles_workbook.py` and run it to produce `articles.xlsx`
2. Create `scripts/split_pdf.py` for splitting multi-article PDFs into individual files
3. Test `split_pdf.py` against existing `A_Nation_At_Risk_1983.pdf`
4. Create `/split-pdf` skill at `/Users/andrewmceachin/Desktop/.claude/skills/split-pdf/SKILL.md`
5. Update project `CLAUDE.md` with new workflow documentation

### Status: ALL 5 STEPS COMPLETED SUCCESSFULLY.

---

## Previous Task: COMPLETE — Restructured positions.yaml to employer-first format (2026-03-14)

### Objective
The user edited `cv/output/McEachin_CV.tex` directly (commit e7dbed3) to group positions under employers instead of listing them flat. Now the source of truth (YAML, template, build scripts) needs to be updated to match that output.

### Plan
1. Rewrite `data/positions.yaml` from flat positions list to employers list with nested roles
2. Update `cv/template/cv_template.tex.j2` Employment section template to iterate employers then roles
3. Update `scripts/build_cv.py` data extraction key (positions -> employers or similar)
4. Update `scripts/utils.py` validation to match new YAML schema

### Progress
- [x] Step 1: Rewrite `data/positions.yaml` to employer-first nested format
- [x] Step 2: Update `cv/template/cv_template.tex.j2` Employment section
- [x] Step 3: Update `scripts/build_cv.py` data extraction
- [x] Step 4: Update `scripts/utils.py` validation

### Status: ALL 4 STEPS COMPLETED SUCCESSFULLY.

### Step Details

**Step 1 (DONE):** Rewrote `data/positions.yaml`. Changed top-level key from `positions` (flat list) to `employers` (list with nested `roles`). 5 employers: ETS, NWEA, RAND, NC State, UVA. Multi-role employers (NWEA, RAND) have per-role start/end years.

**Step 2 (DONE):** Updated `cv/template/cv_template.tex.j2` lines 76-84. Replaced flat position loop with nested employer/role loop. Single-role employers show employer+dates then role. Multi-role employers show employer+dates then each role with its own dates.

**Step 3 (DONE):** Updated `scripts/build_cv.py` line 86. Changed data extraction from `data.get("positions", {}).get("positions", [])` to `data.get("positions", {}).get("employers", [])`.

**Step 4 (DONE):** Updated `scripts/utils.py` lines 200-214. Replaced simple list check with validation of employer name (str), roles (non-empty list), and each role's title (str).

### Verification
- `make validate` passed with no errors
- `make build` succeeded (PDF 170.5 KB)
- Generated Employment section matches target from commit e7dbed3

### Key Decisions
- Matching the employer groupings from commit e7dbed3 of the edited .tex file
- YAML is the source of truth; the hand-edited .tex file is reference only
- Multi-role employers (NWEA, RAND) display an overall date range plus per-role date ranges
- Single-role employers display just the employer date range with the role title

### Files Modified
- `data/positions.yaml` (rewritten from flat to employer-first nested format)
- `cv/template/cv_template.tex.j2` (Employment section, lines 76-84)
- `scripts/build_cv.py` (line 86, data extraction key)
- `scripts/utils.py` (lines 200-214, validation logic)

### Files Regenerated by Build
- `cv/output/McEachin_CV.tex`
- `cv/output/McEachin_CV.pdf`
- `site/static/uploads/McEachin_CV.pdf`

---

## Phase 5: Final Polish, Deployment & Go-Live (2026-02-24)

### Completed — Site-Wide Visual Consistency
- [x] Applied mountain sketch backdrop to ALL pages (previously publications-only)
- [x] Widened all content pages (not just publications) with left-alignment and matching font size (1.05rem)
- [x] Right-aligned navigation menu items
- [x] Removed CV page from nav menu (redundant -- Download CV button exists on profile section)

### Completed — Bug Fixes
- [x] Fixed news coverage section on Commentary & Media page -- was displaying publication IDs instead of human-readable titles. Built a title lookup from publications data to resolve references correctly.
- [x] Fixed invisible bold text in prose sections -- Tailwind dark mode was overriding `<strong>` tag color. Added `.prose strong { color: #1b4965 !important }` to custom CSS.
- [x] Fixed Hugo dev server rendering corruption -- stopped old server process, performed clean rebuild

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
- `data/publications.yaml` -- `theme_order` with `description` field, `theme` on all 63 entries
- `scripts/utils.py` -- Theme validation + `filter_pubs_by_theme()` helper
- `scripts/sync_hugo.py` -- Collapsible themes, intro text, theme descriptions in summary, type badges
- `site/assets/css/custom.css` -- Theme sections, mountain backdrop (fixed), spacing, descriptions, responsive
- `README.md` -- Updated to reflect themed layout
- `PROCESS-LOG.md` -- Added Phase 4b entry

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

---

## Session 2026-02-24: Publication Updates & CV Citation Fix

### Completed — Diliberti et al. (2025)
- [x] Fixed id typo (`dilberti` -> `diliberti`)
- [x] Updated title to published version
- [x] Added full author initials (M.K., J.D., L.T.)
- [x] Added volume/issue/pages, DOI, summary, figure image, and PDF link
- [x] Replaced incorrect image with correct event study coefficient plot

### Completed — Bolyard et al. (2025)
- [x] Removed "Revisions Requested at Education Finance and Policy" status
- [x] Added summary, figure image, and PDF link

### Completed — Kuhfeld et al. (2025) NAE Report
- [x] Added summary (revised with writing-style skill principles), figure image, and PDF link

### Completed — Carbonari et al. (2024)
- [x] Updated title to published version ("The Impact and Implementation of Academic Interventions During COVID-19")
- [x] Added DOI, issue/pages, summary, figure image, and PDF link
- [x] Replaced initial image with correct forest plot

### Completed — CV Citation Consistency Fix
- [x] Fixed CV template (`cv_template.tex.j2`) to show `(Accepted)` instead of `(2025)` for publications with `status: "Accepted"`, matching the website's existing behavior in `sync_hugo.py`
- [x] When status is "Accepted", the redundant status annotation after the journal name is also omitted

### Completed — Performance & Visual Fixes
- [x] Compressed mountain backdrop from 6.7 MB PNG to 748 KB JPEG (9x smaller), updated CSS reference
- [x] Removed HugoBlox "Powered by" footer via custom `site/layouts/_partials/site_footer.html` override
- [x] Fixed duplicate mountain backdrop (bio section had its own `::before` pseudo-element on top of the fixed page-body one)
- [x] Made biography section fully transparent so mountain backdrop shows through (required targeting `.blox-resume-biography`, `.home-section-bg`, `.hbb-section`, and `section#about`)
- [x] Cleaned up macOS Finder duplicate files (`.generated 2`, `index 2.md`, etc.)

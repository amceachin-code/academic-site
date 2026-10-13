# Progress Log

## Project Status: COMPLETE: Media Additions, Publication Updates, CV Header, CV Build-Order Fix, and Claude Code Skills

---

## Previous Task: COMPLETE: Media Additions, Publication Updates, CV Header, CV Build-Order Fix, and Claude Code Skills (2026-10-11 to 2026-10-13)

### Objective
Add two recent articles that quote McEachin, bring two publications up to date, tidy the CV header (add GitHub, drop labels and `https://`), fix a build-order bug that left the site's downloadable CV one build behind, and list three public Claude Code skills on the Code page and the CV, with markdown italics in descriptions carried through to LaTeX.

### Progress
- [x] Step 1: Add The 74 and Scientific American articles to `data/media.yaml` (commit c7551bf)
- [x] Step 2: Mark Bolyard et al. summer 2023 paper as accepted at Education Finance and Policy (commit fb1c37c)
- [x] Step 3: Update Carbonari et al. to its published EEPA citation (commit 75769e6)
- [x] Step 4: Revise CV header contact line and add GitHub link (commits 75769e6, 7155947)
- [x] Step 5: Fix CV PDF copy order in `build_all.py` and add a regression test (commit 75769e6)
- [x] Step 6: Add Claude Code skills to `data/software.yaml`, the Code page, and the CV (uncommitted)
- [x] Step 7: Support markdown `*emphasis*` in descriptions on the CV via a `md_italic` filter (uncommitted)
- [x] Step 8: Add tests for the skills section and the italics filter (uncommitted)

### Status: ALL 8 STEPS COMPLETED SUCCESSFULLY.

### Step Details

**Step 1 (DONE):** Added the first two entries to `podcasts_interviews` in `data/media.yaml`: The 74 Million (2026-10-09) and Scientific American (2026-08-28). Both render on the website media page under "Podcasts & Interviews" and do not appear on the CV.

**Step 2 (DONE):** Moved `bolyard-2025-summer-2023` in `data/publications.yaml` from `working_paper` to `journal`, journal Education Finance and Policy, `status: "Accepted"`, year 2026. Kept the id unchanged so the publication URL and PDF path stay stable.

**Step 3 (DONE):** Updated `carbonari-2025-recovery-interventions` to its published citation: EEPA 48(3), 1045-1072, DOI `10.3102/01623737251400377`, year 2026, title ending "in 2022 to 2023". Removed the `status` field.

**Step 4 (DONE):** Edited `cv/template/cv_template.tex.j2` header. Removed the "Email:" label; added a GitHub link from `profile.social.github` after the website; separators are now `\enspace$\vert$\enspace`; wrapped the contact line in `{\small ...}` with trailing `%` to avoid stray spaces; displayed URLs strip `https://` via the Jinja `replace` filter while each `\href` keeps the full URL.

**Step 5 (DONE):** `scripts/build_all.py` used to run `sync_hugo` (which copies `cv/output/McEachin_CV.pdf` to `site/static/uploads/`) before `build_cv`, so the site's CV was always the previous build's. `sync_hugo.main` now takes `copy_pdf` (default `True` for standalone runs and CI); `build_all` passes `copy_pdf=False` and calls `sync_hugo.copy_cv_pdf()` after `build_cv`. Added `tests/test_build_order.py` to lock in the order.

**Step 6 (DONE):** Added a `claude_skills` list to `data/software.yaml` with three skills from the public repo https://github.com/amceachin-code/claude_skills: `writing-style`, `datascience-reviewer`, and `methods-reviewer`. Each entry has `id`, `name`, `description`, and `github` (link to the skill's folder). `sync_hugo.py` gained `_format_claude_skills(skills)`, which `generate_code_page` calls after Software Packages to render a "## Claude Code Skills" section on `site/content/code/_index.md`: one heading per skill, its description, `**Usage:** /name`, and a GitHub link. The section is omitted when the list is empty. `utils.validate_data` checks that `claude_skills` is a list. On the CV, `build_cv.py` passes `claude_skills` into the template context, and `cv_template.tex.j2` renders a `\subsection{Claude Code Skills}` itemize under the Software section, emitting `\section{Software}` itself if there are no software packages.

**Step 7 (DONE):** YAML descriptions can now use markdown `*emphasis*`, first used for the book title *Several Short Sentences About Writing* in the `writing-style` description. Hugo renders it natively. For the CV, new `md_italic_to_latex()` in `utils.py` converts `*x*` to `\textit{x}`, registered in `build_cv.py` as the Jinja filter `md_italic`. It runs after `latex_escape` (`latex_escape|md_italic`) because `latex_escape` would escape the braces it adds. Currently applied only to skill descriptions.

**Step 8 (DONE):** Added `tests/test_code_page.py` (3 tests for `_format_claude_skills`: empty list, full render, no GitHub link) and a `TestMdItalicToLatex` class (5 tests) in `tests/test_citations.py`.

### Verification
- `python3 -m pytest -q tests` passes: 38 tests (34 in `test_citations.py`, 1 in `test_build_order.py`, 3 in `test_code_page.py`)
- `make build` regenerated the CV PDF, site content, and the site's CV copy
- Code page shows the Claude Code Skills section after Software Packages; the CV shows the Claude Code Skills subsection under Software with the book title in italics

### Key Decisions
- Articles that quote McEachin go in `podcasts_interviews`, not `commentary`. `commentary` is reserved for pieces he authored and feeds the CV.
- Publication ids stay fixed when a paper changes type or status, so URLs and PDF links do not break.
- `copy_pdf` defaults to `True` so standalone `sync_hugo.py` runs (including CI, which does not compile LaTeX) still publish the committed PDF.
- Claude Code skills live in a separate `claude_skills` key rather than in `software`, so the CV's software package list format stays unchanged. They still appear on both outputs: the Code page and a CV subsection under Software.
- Italics are written once in YAML as markdown `*emphasis*` and converted for LaTeX by a filter, rather than storing separate HTML and LaTeX versions of a description. The filter must follow `latex_escape`.

### Files Modified
- `data/media.yaml` (two `podcasts_interviews` entries)
- `data/publications.yaml` (Bolyard et al. accepted; Carbonari et al. published citation)
- `cv/template/cv_template.tex.j2` (header contact line)
- `scripts/sync_hugo.py` (`copy_pdf` parameter, `copy_cv_pdf()` helper)
- `scripts/build_all.py` (copy CV PDF after `build_cv`)
- `tests/test_build_order.py` (new)
- `data/software.yaml` (`claude_skills` list)
- `scripts/sync_hugo.py` (`_format_claude_skills()`, called from `generate_code_page`)
- `scripts/utils.py` (`claude_skills` validation, `md_italic_to_latex()`)
- `scripts/build_cv.py` (`md_italic` filter, `claude_skills` in template context)
- `cv/template/cv_template.tex.j2` (Claude Code Skills subsection)
- `tests/test_code_page.py` (new)
- `tests/test_citations.py` (`TestMdItalicToLatex`)

### Files Regenerated by Build
- `cv/output/McEachin_CV.tex`
- `cv/output/McEachin_CV.pdf`
- `site/static/uploads/McEachin_CV.pdf`
- `site/content/media/_index.md`
- `site/content/code/_index.md`
- `site/content/publications/` (affected publication pages and index)

### Next Steps
- CV contact line is still `\small`; it likely fits at normal size now that labels and `https://` are gone.
- Add volume, issue, and pages for Bolyard et al. once it is published in Education Finance and Policy.
- Hugo emits deprecation warnings for top-level `doi` in publication front matter; move it to `hugoblox.ids: { doi: ... }` in `sync_hugo.py`.
- `news_coverage` entries in `data/media.yaml` lack URLs.
- Apply `md_italic` to software package descriptions in the CV template too, so italics work there as well.

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

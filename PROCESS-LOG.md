# Process Log

Running log of project progress, decisions, and to-do items for the academic-site project.

---

## To-Do List

### Completed
- [x] **Phase 1: Foundation** — Created project structure, installed Hugo + Go, scaffolded HugoBlox theme, verified `hugo build` succeeds
- [x] **Phase 2: Data Layer** — Created all 10 YAML data files with Andrew's full CV data (36 journal articles, working papers, reports, book chapters, grants, awards, service, media, software)
- [x] **Phase 3: Python Build Scripts** — Created `utils.py`, `sync_hugo.py`, `build_cv.py`, `build_all.py`, `requirements.txt`
- [x] **Phase 5: LaTeX CV Template** — Created `cv_template.tex.j2` with angle-bracket Jinja2 delimiters
- [x] **Phase 6: Deployment** — Created `.github/workflows/deploy.yml`, `Makefile`, `.gitignore`
- [x] Created `/academic-branding` skill for reviewing public-facing materials

- [x] **Phase 4: Hugo Customization** — Full build pipeline working, homepage renders, publications page with collapsible theme sections
- [x] **Phase 4b: Publications Theme Reorganization** — Reorganized all 63 publications into 4 collapsible research themes

### Remaining
- [ ] Test CV PDF compilation with special characters (`&` in titles, accented names)
- [ ] Add avatar photo and hero image
- [ ] Fill in Google Scholar URL, any missing URLs in media.yaml
- [x] Phase 7: Custom domain DNS configuration — www.andrew-mceachin.com live with HTTPS
- [x] Verify GitHub Actions workflow succeeds — site deployed via GitHub Pages
- [ ] Run `/academic-branding` audit on final site

---

## Phase 1: Foundation (Completed 2026-02-24)

**What was done:**
- Created project directory at `/Users/andrewmceachin/Desktop/projects/academic-site/`
- Installed Hugo Extended v0.156.0 and Go v1.26.0 via Homebrew
- Scaffolded Hugo site in `site/` subdirectory
- Installed HugoBlox theme via Go modules (`github.com/HugoBlox/kit/modules/blox`)
  - **Key discovery:** The module path changed from `hugo-blox-builder/modules/blox-tailwind` to `kit/modules/blox` in 2025
- Installed TailwindCSS + typography plugin in `site/node_modules/`
- Created author profile at `site/content/authors/admin/_index.md`
- Verified `hugo build` produces 11 pages in 526ms

**Decisions:**
- Used `github.com/HugoBlox/kit/modules/blox` (not the old `hugo-blox-builder` path)
- Tailwind v4 installed via npm (required by HugoBlox theme)
- Simplified Hugo output formats to `[HTML, RSS]` (dropped `headers, redirects, backlinks` which required Netlify plugin)

---

## Phase 2: Data Layer (Completed 2026-02-24)

**What was done:**
- Created all 10 YAML data files in `data/`
- Populated from actual CV PDF (AJM_CV.pdf, last updated Feb 23, 2026):
  - `profile.yaml` — bio, contact, research interests
  - `education.yaml` — 3 degrees (Ph.D. Ed Policy USC 2012, M.A. Econ USC 2012, A.B. History Cornell 2006)
  - `positions.yaml` — 9 positions from UVA postdoc (2012) to ETS (2024-present)
  - `publications.yaml` — 36 journal articles, 2 working papers, 10 reports, 12 book chapters/other
  - `media.yaml` — 9 commentary pieces, news coverage references, empty podcasts list
  - `grants.yaml` — 17 grants totaling ~$12M
  - `awards.yaml` — 14 awards/honors
  - `service.yaml` — 6 editorial boards, 9 committee positions, 19 journals reviewed
  - `software.yaml` — 2 packages (horseshoe, rdtp)
  - `presentations.yaml` — empty list (placeholder for future)

**Data quality notes:**
- All data sourced from actual CV PDF, not AI-generated guesses
- Google Scholar URL is placeholder — needs real URL
- Media URLs are empty strings — need to be filled in
- Publications list uses `id` field for unique identification

---

## Phase 3: Python Build Scripts (Completed 2026-02-24)

**What was done:**
- `scripts/utils.py` — Path constants, explicit YAML file list loading, `validate_data()`, `latex_escape()`, citation formatting, pub filtering
- `scripts/sync_hugo.py` — Generates publication pages (one dir per pub), publications index, media page, code page. Uses `.generated` markers for safe cleanup.
- `scripts/build_cv.py` — Renders Jinja2 template with angle-bracket delimiters, compiles with pdflatex (2 passes), verifies PDF exists and >0 bytes
- `scripts/build_all.py` — Orchestrator that imports both above as functions, shares loaded data, supports `--validate` dry-run
- `scripts/requirements.txt` — Pinned: `PyYAML==6.0.2`, `Jinja2==3.1.5`

**Engineering safeguards implemented:**
1. `latex_escape()` handles `& % $ # _ { } ~ ^`, passes UTF-8 through
2. Angle-bracket Jinja2 delimiters in build_cv.py
3. YAML validation checks required fields, types, unique IDs
4. `.generated` marker-based cleanup (preserves hand-created dirs)
5. PDF existence + size check after pdflatex
6. Explicit YAML file list (not glob)
7. Direct Python imports (no subprocess)

---

## Phase 5: LaTeX CV Template (Completed 2026-02-24)

**What was done:**
- Created `cv/template/cv_template.tex.j2` with:
  - Angle-bracket delimiters throughout (`<< >>`, `<% %>`, `<# #>`)
  - `|latex_escape` filter on ALL text fields
  - Sections: Research Interests, Education, Employment, Journal Articles (numbered), Working Papers, Reports, Book Chapters, Commentary, Grants, Awards, Editorial Service, Professional Service, Journal Reviewer, Software
  - Professional formatting: 11pt, letterpaper, 1in margins, hyperlinks, running header

---

## Phase 6: Deployment Infrastructure (Completed 2026-02-24)

**What was done:**
- `.github/workflows/deploy.yml` — Full CI/CD: Python setup, pip install, TeX Live, Hugo, Node, build_all.py, hugo --minify, deploy to GitHub Pages
- `Makefile` — targets: `validate`, `build`, `preview`, `clean`, `install`
- `.gitignore` — Ignores LaTeX artifacts, node_modules, __pycache__, Hugo public/, editor files
- `site/static/CNAME` — `www.andrew-mceachin.com`
- GitHub repo: `https://github.com/amceachin-code/academic-site.git` (public — changed 2026-02-24 for GitHub Pages)

---

## Phase 4b: Publications Theme Reorganization (Completed 2026-02-24)

**What was done:**
- Reorganized publications page from flat type-grouped list into 4 collapsible research themes
- All 63 publications assigned to a theme via `theme` field in `publications.yaml`
- Native HTML `<details>/<summary>` for collapsible sections — no JavaScript
- Type badges ("Journal Article", "Working Paper", etc.) on each card since type grouping was removed
- Themes sorted by publication count (largest first):
  1. Out-of-School or Disrupted Learning (24)
  2. Accountability (22)
  3. Exclusionary Practices, Discipline, Tracking & Segregation (9)
  4. School Choice (8)

**Files modified:**
- `data/publications.yaml` — Added `theme_order` list + `theme` field on all 63 entries
- `scripts/utils.py` — Theme validation for all pub types + `filter_pubs_by_theme()` helper
- `scripts/sync_hugo.py` — Rewrote `generate_publications_index()` for collapsible themes, added type badge, cascade frontmatter
- `site/assets/css/custom.css` — Collapsible section styles, CSS chevron, type badge, responsive rules
- `README.md` — Updated to reflect theme-based layout

**Bugs fixed:**
- Ghost card rendering: Hugo auto-listed child pages as dark gradient cards after custom HTML. Fixed with `cascade: build: list: never` frontmatter.
- Hugo deprecation: `_build` → `build` in cascade frontmatter (Hugo 0.145+)
- Collapsed/expanded width mismatch: Added `width: 100%` to `.pub-theme-section`

**Code review:** `/datascience-reviewer` issued "Satisfied" verdict. Minor cleanup: removed unused imports (`filter_pubs_by_type`, `format_citation`).

---

## Phase 4c: Publications Page Polish (Completed 2026-02-24)

**What was done:**
- Added research agenda introduction paragraph above collapsible theme sections
- Added mountain sketch backdrop to publications page using `position: fixed` so it persists when sections expand
- Reduced whitespace between nav header and publications content (zeroed page-header padding, removed page-body top margin, tightened h1)
- Fixed article container width (`width: 100%`) so collapsed and expanded sections match
- Added 2-3 sentence theme descriptions inside `<summary>` elements, always visible even when collapsed
- Cleaned up 131 macOS Finder duplicate files (`.generated 2`, `index 2.md`, etc.)
- Added `description` field to each theme in `theme_order` in `publications.yaml`

**Files modified:**
- `data/publications.yaml` — Added `description` field to each theme in `theme_order`
- `scripts/sync_hugo.py` — Added intro text generation, theme descriptions inside `<summary>`, vertical header layout
- `site/assets/css/custom.css` — Mountain backdrop (fixed positioning), page spacing overrides, `.pub-theme-description` styles, `.pub-theme-header-top` row layout, `.pub-intro` styles

---

## Session — 2026-02-24 (continued): Site-wide polish and deployment

**What was done:**
- Applied mountain backdrop to all pages (changed CSS from targeting `.page-body:has(.pub-theme-section)` to all `.page-body` elements)
- Removed CV page and nav menu item (Download CV button already on profile makes standalone page redundant)
- Right-aligned navigation menu (CSS: `nav.navbar justify-content: space-between`, `.navbar-nav margin-left: auto`)
- Widened all content pages to 1100px max-width with left alignment and 1.05rem font (was publications-only, now applies to Commentary & Media and Code pages too)
- Fixed Commentary & Media page: news coverage was showing publication IDs instead of titles — passed `pubs` list to `generate_media_page()` and built title lookup dict
- Fixed invisible bold text: Tailwind `dark:prose-invert` was making `<strong>` tags invisible against backdrop — added `.prose strong { color: #1b4965 !important }`
- Fixed Hugo dev server rendering corruption (deferred content hashes, dark mountain bands) — stopped old server, clean rebuild on new port
- Made repo public (was private, GitHub Pages requires public on free plan)
- Enabled GitHub Pages with GitHub Actions source via `gh api`
- Configured custom domain `www.andrew-mceachin.com` — CNAME and A records in Squarespace DNS pointing to GitHub Pages IPs
- Enabled HTTPS enforcement
- Site is now **LIVE** at https://www.andrew-mceachin.com

**Files modified:**
- `scripts/sync_hugo.py` — Media page title lookup (passed pubs to `generate_media_page()`, built ID-to-title dict)
- `site/assets/css/custom.css` — Mountain backdrop on all pages, nav right-alignment, content page widening, bold text color fix
- `site/config/_default/menus.yaml` — Removed CV nav item
- `site/content/cv/_index.md` — Deleted
- `site/content/media/_index.md` — Regenerated with correct publication titles in news coverage section
- All `site/content/publications/*/.generated` — Regenerated timestamps

**Bugs fixed:**
- News coverage on Media page showed raw publication IDs (e.g., `mceachin2015`) instead of human-readable titles. Root cause: `generate_media_page()` had no access to the publications data. Fix: passed the loaded pubs list and built a `{id: title}` lookup dict.
- Bold text (`<strong>`) invisible on all pages. Root cause: Tailwind's `dark:prose-invert` was setting text to white, which was invisible against the light mountain backdrop. Fix: explicit `.prose strong { color: #1b4965 !important }`.
- Hugo dev server showing deferred content hashes and dark mountain bands. Root cause: stale server process on port 1313. Fix: killed old process, ran clean `hugo server` on fresh port.

**Deployment milestones:**
- Repository visibility changed from private to public (required for GitHub Pages on free tier)
- GitHub Pages enabled with GitHub Actions as build/deployment source
- Custom domain `www.andrew-mceachin.com` configured with DNS records at Squarespace
- HTTPS enforced via GitHub Pages settings
- Site verified live and accessible

---

## Files Created

| File | Status |
|------|--------|
| `data/profile.yaml` | Created |
| `data/education.yaml` | Created |
| `data/positions.yaml` | Created |
| `data/publications.yaml` | Created |
| `data/presentations.yaml` | Created (empty stub) |
| `data/media.yaml` | Created |
| `data/grants.yaml` | Created |
| `data/awards.yaml` | Created |
| `data/service.yaml` | Created |
| `data/software.yaml` | Created |
| `scripts/utils.py` | Created |
| `scripts/sync_hugo.py` | Created |
| `scripts/build_cv.py` | Created |
| `scripts/build_all.py` | Created |
| `scripts/requirements.txt` | Created |
| `cv/template/cv_template.tex.j2` | Created |
| `site/config/_default/hugo.yaml` | Created |
| `site/config/_default/params.yaml` | Created |
| `site/config/_default/menus.yaml` | Created |
| `site/config/_default/module.yaml` | Created |
| `site/content/_index.md` | Created |
| `site/content/authors/admin/_index.md` | Created |
| `site/content/cv/_index.md` | Deleted (2026-02-24 — redundant with profile Download CV button) |
| `site/assets/css/custom.css` | Created |
| `site/static/CNAME` | Created |
| `.github/workflows/deploy.yml` | Created |
| `Makefile` | Created |
| `.gitignore` | Created |
| `README.md` | Created |
| `CLAUDE.md` | Created |
| `PROCESS-LOG.md` | Created |

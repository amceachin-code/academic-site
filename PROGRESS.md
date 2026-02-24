# Progress Log

## Current Task: Reorganize Publications by Theme with Collapsible Sections

### Objective
Reorganize the publications page from a flat type-grouped list into collapsible theme sections using native HTML `<details>/<summary>`. All 63 publications grouped into 4 research themes, sorted by publication count (largest first).

### Plan
1. Update `data/publications.yaml` — Add `theme_order` list + `theme` field on all 63 entries
2. Update `scripts/utils.py` — Theme validation for all types + `filter_pubs_by_theme()` helper
3. Update `scripts/sync_hugo.py` — Rewrite index: 4 collapsible themes + type badge + cascade frontmatter
4. Update `site/assets/css/custom.css` — Collapsible section styles, chevron, type badge, responsive
5. Verify — `make build` passes, output correct

### Status
- [x] Step 1: Added `theme_order` (4 themes) + `theme` field on all 63 publications
- [x] Step 2: Theme validation (all types) + `filter_pubs_by_theme()` helper
- [x] Step 3: Collapsible `<details>/<summary>` sections, type badges, `cascade: build: list: never`
- [x] Step 4: CSS for collapsible sections, chevron indicator, type badge, `width: 100%`, responsive
- [x] Step 5: `make build` passes, 4 theme sections render correctly

### Refinements Applied
- All publications (not just journals/WPs) grouped into themes
- Ghost card bug fixed via `cascade: build: list: never` frontmatter
- Themes sorted by publication count: disrupted_learning (24), accountability (22), exclusionary_practices (9), school_choice (8)
- Collapsed/expanded width mismatch fixed with `width: 100%`
- Unused imports cleaned up (`filter_pubs_by_type`, `format_citation`)
- Hugo deprecation fixed: `_build` → `build` in cascade frontmatter

### Files Modified
- `data/publications.yaml`
- `scripts/utils.py`
- `scripts/sync_hugo.py`
- `site/assets/css/custom.css`
- `README.md`
- `PROCESS-LOG.md`

# CLAUDE.md — Project-specific instructions for Claude Code

## Project Overview

This is an academic personal website + CV pipeline for Andrew McEachin. YAML data files in `data/` are the single source of truth. Python scripts generate both Hugo website content and a LaTeX CV PDF.

## Architecture

- `data/*.yaml` — Source of truth. NEVER hand-edit generated files in `site/content/`; edit YAML instead.
- `scripts/` — Python build pipeline. `build_all.py` is the orchestrator.
- `cv/template/cv_template.tex.j2` — LaTeX template with **angle-bracket Jinja2 delimiters** (`<< >>`, `<% %>`, `<# #>`). NEVER use standard `{{ }}` or `{% %}` in this file.
- `site/` — Hugo site using HugoBlox Academic theme (Go module: `github.com/HugoBlox/kit/modules/blox`).

## Critical Rules

1. **YAML is the source of truth.** To change website content, edit the YAML file, then run `make build`. Do NOT edit generated markdown files directly.

2. **LaTeX template uses ONLY angle-bracket delimiters.** The Jinja2 environment in `build_cv.py` is configured with `<<`, `<%`, `<#`. Standard delimiters will silently fail.

3. **`latex_escape` filter is REQUIRED** on every text field in the CV template. Without it, any `&` in a paper title breaks the entire PDF build. Example: `<< pub.title|latex_escape >>`.

4. **`.generated` marker files** protect hand-created content. The `sync_hugo.py` script only deletes directories containing a `.generated` file. Never remove these markers manually.

5. **Generated Hugo content is committed to git.** This is intentional — it enables `hugo server` preview without running Python first, and makes `git diff` show content changes.

## Build Commands

```bash
make validate    # Validate YAML only (no files generated)
make build       # Full build: YAML → Hugo content + CV PDF + hugo --minify
make preview     # Build + launch local dev server at localhost:1313
make clean       # Remove LaTeX build artifacts
make install     # Install Python + Node dependencies
```

## Key Files

| File | Purpose |
|------|---------|
| `scripts/utils.py` | Path constants, YAML loading, validation, `latex_escape()` |
| `scripts/sync_hugo.py` | YAML → Hugo markdown (publications, media, code pages) |
| `scripts/build_cv.py` | YAML → LaTeX → PDF |
| `scripts/build_all.py` | Orchestrator; `--validate` for dry-run |
| `cv/template/cv_template.tex.j2` | LaTeX template (angle-bracket Jinja2) |
| `site/config/_default/hugo.yaml` | Hugo main config |
| `site/config/_default/params.yaml` | Theme params (dark nav, fonts) |
| `site/config/_default/menus.yaml` | Navigation menu |

## Adding a New Publication

1. Add entry to `data/publications.yaml` with required fields: `id`, `type`, `title`, `authors`, `year`
2. Run `make validate` to check for errors
3. Run `make build` to regenerate everything
4. `git diff` to review changes, then commit

## Dependencies

- Python: `PyYAML==6.0.2`, `Jinja2==3.1.5`
- Hugo Extended 0.150+ with Go modules
- Node.js (TailwindCSS for HugoBlox theme)
- TeX Live (pdflatex for CV)

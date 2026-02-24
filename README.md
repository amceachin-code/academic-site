# Academic Website + CV Pipeline

A single set of YAML data files powers both a [Hugo](https://gohugo.io/) website (hosted on GitHub Pages) and a LaTeX CV (auto-compiled to PDF). One update to the YAML, one command regenerates everything.

**Live site:** [www.andrew-mceachin.com](https://www.andrew-mceachin.com)
**GitHub repo:** [github.com/amceachin-code/academic-site](https://github.com/amceachin-code/academic-site) (public)

---

## Table of Contents

- [Quick Start](#quick-start)
- [Dependencies](#dependencies)
- [Make Commands](#make-commands)
- [Project Structure](#project-structure)
- [Key Files](#key-files)
- [How It Works](#how-it-works)
- [Content Workflow](#content-workflow)
- [Adding a New Publication](#adding-a-new-publication)
- [Publication Card Layout](#publication-card-layout)
- [Deployment](#deployment)
- [Design Notes](#design-notes)
- [License](#license)

---

## Quick Start

```bash
# 1. Install all dependencies (Python packages + Node modules)
make install

# 2. Validate YAML data (no files generated -- just checks for errors)
make validate

# 3. Full build: YAML -> Hugo content + CV PDF -> static site
make build

# 4. Build + launch local preview at localhost:1313
make preview

# 5. Clean LaTeX build artifacts
make clean
```

---

## Dependencies

### Python 3.12

- `PyYAML==6.0.2` -- YAML parsing for data files
- `Jinja2==3.1.5` -- Template rendering for LaTeX CV

Install: `pip install -r scripts/requirements.txt`

### Hugo Extended v0.150+

The site uses [HugoBlox](https://hugoblox.com/) (formerly Hugo Academic / Wowchemy) via Go modules. Hugo Extended is required for SCSS/PostCSS processing.

- Module: `github.com/HugoBlox/kit/modules/blox`
- Go 1.23+ is required for Hugo module resolution

Install (macOS): `brew install hugo`
Install (other): see [Hugo installation docs](https://gohugo.io/installation/)

### Node.js 18+

Required for TailwindCSS, which the HugoBlox theme uses for styling.

- `tailwindcss@^4.2.1`
- `@tailwindcss/cli@^4.2.1`
- `@tailwindcss/typography@^0.5.19`

Install: `cd site && npm install`

### TeX Live

Required for compiling the LaTeX CV to PDF. The build script calls `pdflatex` directly.

- Packages needed: `texlive-latex-base`, `texlive-latex-extra`, `texlive-fonts-recommended`, `texlive-fonts-extra`

Install (macOS): `brew install --cask mactex` or install [BasicTeX](https://www.tug.org/mactex/morepackages.html) with additional packages via `tlmgr`
Install (Ubuntu): `sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra`

---

## Make Commands

| Command | Description |
|---|---|
| `make install` | Install Python packages (`pip install -r scripts/requirements.txt`) and Node modules (`cd site && npm install`) |
| `make validate` | Run `build_all.py --validate` to check YAML data for errors (required fields, types, unique IDs). No files are generated. |
| `make build` | Full pipeline: validate YAML, generate Hugo content, compile CV PDF, then `hugo --minify` to produce the static site in `site/public/` |
| `make preview` | Run `make build` then launch `hugo server` at `localhost:1313` for local development |
| `make clean` | Remove LaTeX build artifacts (`.aux`, `.log`, `.out`, `.fls`, `.fdb_latexmk`, `.synctex.gz`) and generated `.tex` from `cv/output/` |

---

## Project Structure

```
academic-site/
├── data/                              # YAML single source of truth (10 files)
│   ├── profile.yaml                   # Name, title, bio, contact, social links
│   ├── education.yaml                 # Degrees (Ph.D., M.A., A.B.)
│   ├── positions.yaml                 # Employment history
│   ├── publications.yaml              # All pubs: 63 entries (journal articles,
│   │                                  #   working papers, reports, book chapters)
│   │                                  #   Optional per-pub: summary, links, image
│   ├── presentations.yaml             # Conference talks, invited seminars (stub)
│   ├── media.yaml                     # Commentary, op-eds, media coverage
│   ├── grants.yaml                    # Grants and funding
│   ├── awards.yaml                    # Honors and awards
│   ├── service.yaml                   # Editorial boards, referee work, committees
│   └── software.yaml                  # Stata/R packages (horseshoe, rdtp)
│
├── scripts/                           # Python build pipeline
│   ├── utils.py                       # YAML loading, validation, latex_escape(),
│   │                                  #   path constants, citation formatting
│   ├── sync_hugo.py                   # YAML -> Hugo content (publications as HTML
│   │                                  #   card layout, media, code pages). Uses
│   │                                  #   .generated markers for safe cleanup
│   ├── build_cv.py                    # YAML -> Jinja2 (angle-bracket delimiters)
│   │                                  #   -> LaTeX -> pdflatex (2 passes) -> PDF
│   ├── build_all.py                   # Orchestrator; imports sync_hugo + build_cv
│   │                                  #   as functions. Supports --validate flag
│   └── requirements.txt               # Pinned: PyYAML==6.0.2, Jinja2==3.1.5
│
├── cv/                                # LaTeX CV pipeline
│   ├── template/
│   │   └── cv_template.tex.j2         # Jinja2 template with angle-bracket
│   │                                  #   delimiters (<< >>, <% %>, <# #>)
│   └── output/                        # Generated .tex, .pdf, and build artifacts
│       ├── McEachin_CV.tex            # Generated LaTeX source (committed)
│       └── McEachin_CV.pdf            # Compiled PDF (committed; also copied to
│                                      #   site/static/uploads/ for download)
│
├── site/                              # Hugo site (HugoBlox Academic theme)
│   ├── config/_default/               # Hugo configuration
│   │   ├── hugo.yaml                  # Main config (title, baseURL, build opts)
│   │   ├── params.yaml                # Theme params (appearance, SEO, header)
│   │   ├── menus.yaml                 # Navigation: Home, Publications,
│   │   │                              #   Commentary & Media, Code
│   │   └── module.yaml                # HugoBlox module import
│   ├── content/                       # Pages (mix of hand-edited + generated)
│   │   ├── _index.md                  # Homepage (biography block, Download CV btn)
│   │   ├── publications/              # Generated: 1 dir per pub + index page
│   │   ├── media/                     # Generated: Commentary & Media listing
│   │   └── code/                      # Generated: Software packages listing
│   ├── assets/
│   │   └── css/custom.css             # Full custom theme: white bg, dark teal
│   │                                  #   (#1b4965) accents, side-by-side bio
│   │                                  #   layout, mountain backdrop, pub-card
│   │                                  #   styles, responsive
│   ├── data/authors/admin.yaml        # Author metadata for HugoBlox
│   ├── assets/media/authors/          # Avatar images (admin.jpg)
│   ├── static/
│   │   ├── CNAME                      # Custom domain: www.andrew-mceachin.com
│   │   ├── uploads/McEachin_CV.pdf    # CV PDF for download
│   │   ├── uploads/publications/      # PDF files for individual papers
│   │   ├── images/mountains-backdrop.png  # Decorative bio section background
│   │   └── images/publications/       # Article images for publication cards
│   ├── go.mod / go.sum                # Go module deps (HugoBlox theme)
│   ├── package.json                   # Node deps (Tailwind CSS v4, typography)
│   └── hugo.yaml                      # Root Hugo config (imports _default/)
│
├── .github/workflows/
│   └── deploy.yml                     # GitHub Actions: Python + TeX Live + Hugo
│                                      #   + Node -> build -> deploy to GH Pages
│
├── Makefile                           # build, preview, clean, validate, install
├── LICENSE                            # GPL-3.0
├── CLAUDE.md                          # Project-specific instructions for Claude
├── PROCESS-LOG.md                     # Running development log and to-do list
├── PROGRESS.md                        # Task-level progress journal
├── .gitignore                         # Ignores: LaTeX artifacts, node_modules,
│                                      #   __pycache__, Hugo public/, editor files
└── README.md                          # This file
```

---

## Key Files

### Data Layer (`data/`)

| File | Contents |
|---|---|
| `profile.yaml` | Name, title, bio paragraph, contact info, social links (Google Scholar, GitHub, email) |
| `education.yaml` | 3 degrees: Ph.D. Education Policy (USC), M.A. Economics (USC), A.B. History (Cornell) |
| `positions.yaml` | Employment history from UVA postdoc (2012) through ETS Senior Research Director (2024--present) |
| `publications.yaml` | 63 entries across journal articles, working papers, reports, and book chapters. Organized by 4 research themes via `theme_order` list + per-entry `theme` field. Optional per-entry fields: `summary` (string), `links` (list of `{label, url}` dicts), and `image` (filename for article image) |
| `presentations.yaml` | Placeholder (empty list) for future conference talks and invited seminars |
| `media.yaml` | Commentary/op-ed pieces and news coverage references |
| `grants.yaml` | Grants and funding |
| `awards.yaml` | Honors and awards |
| `service.yaml` | Editorial boards, committee positions, journals reviewed for |
| `software.yaml` | 2 packages (Stata + R): `horseshoe` (Bayesian horseshoe prior) and `rdtp` (regression discontinuity) |

### Build Scripts (`scripts/`)

| File | Purpose |
|---|---|
| `utils.py` | Path constants (`PROJECT_ROOT`, `DATA_DIR`, etc.), YAML loading with explicit file list, `validate_data()` for schema checking (including theme validation, optional `summary`, `links`, and `image` fields), `latex_escape()` filter, citation string formatting, publication filtering helpers (`filter_pubs_by_type`, `filter_pubs_by_theme`) |
| `sync_hugo.py` | Generates Hugo content from YAML: one directory per publication (with `.generated` marker for safe cleanup), publications index page with collapsible theme sections using `<details>/<summary>` HTML and type badges on each card, media listing page, code/software page |
| `build_cv.py` | Renders the Jinja2 LaTeX template with angle-bracket delimiters (`<< >>`, `<% %>`, `<# #>`), compiles with `pdflatex` (2 passes for cross-references), verifies PDF output exists and is non-empty |
| `build_all.py` | Orchestrator that imports `sync_hugo.py` and `build_cv.py` as modules, loads YAML data once, passes it to both. Supports `--validate` flag for dry-run validation only |
| `requirements.txt` | Pinned dependencies: `PyYAML==6.0.2`, `Jinja2==3.1.5` |

### CV Template (`cv/template/`)

| File | Purpose |
|---|---|
| `cv_template.tex.j2` | Full LaTeX CV template using angle-bracket Jinja2 delimiters to avoid `{}` escaping conflicts. Sections: Research Interests, Education, Employment, Journal Articles (numbered), Working Papers, Reports, Book Chapters, Commentary, Grants, Awards, Editorial Service, Professional Service, Journal Reviewer, Software. All text fields use the `\|latex_escape` filter. |

### Site Theme (`site/assets/css/`)

| File | Purpose |
|---|---|
| `custom.css` | Complete custom theme overriding HugoBlox defaults. White background, dark teal (`#1b4965`) accent color, Inter font stack, side-by-side biography layout (avatar pinned left, text flowing right), mountain sketch backdrop on bio section, outlined "Download CV" button, `.pub-card-*` component styles for publication cards, `.pub-theme-*` styles for collapsible theme sections with chevron indicators, `.pub-card-type-badge` pill styles, responsive stacking on mobile. |

### Deployment

| File | Purpose |
|---|---|
| `.github/workflows/deploy.yml` | GitHub Actions workflow: sets up Python 3.12, installs pip deps, installs TeX Live, sets up Hugo Extended 0.156.0, installs Node 20 + npm deps, runs `build_all.py` (YAML to Hugo content + CV PDF), runs `hugo --minify`, then deploys to GitHub Pages |
| `site/static/CNAME` | Custom domain configuration: `www.andrew-mceachin.com` |

---

## How It Works

```
                    +-----------------------+
                    |   data/*.yaml         |
                    |  (source of truth)    |
                    +-----------+-----------+
                                |
                       validate_data()
                                |
                 +--------------+--------------+
                 |                             |
          sync_hugo.py                  build_cv.py
                 |                             |
        Hugo markdown files         Jinja2 -> LaTeX -> pdflatex
                 |                             |
          hugo --minify              McEachin_CV.pdf
                 |
        Static HTML site
        (site/public/)
```

The `build_all.py` orchestrator imports both `sync_hugo` and `build_cv` as Python functions (no subprocess calls), loads the YAML data once, and passes it to both pipelines.

---

## Content Workflow

### Updating existing content

1. Edit the relevant YAML file in `data/` (e.g., add a publication to `publications.yaml`)
2. Run `make validate` to catch errors early
3. Run `make preview` to see changes locally at `localhost:1313`
4. Commit and push to `main` -- GitHub Actions auto-deploys

### Adding a new section/page

Hand-create the page under `site/content/`. Only generated content (publications, media, code) goes through the Python pipeline. The homepage (`site/content/_index.md`) is hand-edited.

---

## Adding a New Publication

1. **Add the YAML entry.** Open `data/publications.yaml` and add an entry with the required fields:

   ```yaml
   - id: lastname-2026           # Unique ID (used as directory name)
     type: journal                # One of: journal, working_paper, report, book_chapter
     theme: disrupted_learning    # One of: disrupted_learning, accountability,
                                  #   exclusionary_practices, school_choice
     title: "Your Paper Title"
     authors:
       - "LastName, F."
       - "CoAuthor, A. B."
     year: 2026
     journal: "Journal Name"     # Or book/publisher for non-journal types
     volume: "12"
     issue: "3"
     pages: "100-125"
     doi: "10.1234/example"

     # Optional fields for the website card layout:
     summary: "A one-sentence plain-language description of this paper."
     image: "lastname-2026.png"  # Article image (place in site/static/images/publications/)
     links:
       - label: "PDF"
         url: "https://example.com/paper.pdf"
       - label: "Replication Code"
         url: "https://github.com/example/repo"
   ```

2. **Add an article image (optional).** Place a PNG or JPG image at `site/static/images/publications/<filename>`. The filename must match the `image` field in the YAML entry. Only publications with an `image` field display the image column; publications without it show a text-only card.

3. **Validate.** Run `make validate` to check for schema errors (required fields, types, unique IDs).

4. **Build and preview.** Run `make preview` to regenerate everything and view locally at `localhost:1313`. The build creates a new directory under `site/content/publications/<id>/` with a `.generated` marker and an `index.md`.

5. **Commit.** Review with `git diff`, then commit and push to `main`. GitHub Actions auto-deploys.

---

## Publication Card Layout

The Publications page organizes all 63 publications into 4 collapsible research themes using native HTML `<details>/<summary>` elements (no JavaScript required). Themes are sorted by publication count, largest first:

1. **Out-of-School or Disrupted Learning** -- research on summer learning loss, summer school programs, and COVID-19 educational impacts
2. **Accountability** -- federal and state accountability policy effects on teacher quality, school improvement, and education reform
3. **Exclusionary Practices, Discipline, Tracking & Segregation** -- how school structures and practices sort students and reinforce inequality
4. **School Choice** -- charter school performance, virtual schooling, cream-skimming, and competitive effects on traditional public schools

The page opens with a brief research agenda introduction, followed by the collapsible sections. Each section header shows the theme name, publication count, and a 2-3 sentence description that remains visible even when collapsed. A mountain sketch backdrop stays fixed in the viewport as the user scrolls and expands sections.

Each section starts collapsed; clicking expands to reveal cards sorted by year descending. Each card shows:

- **Type badge** (e.g., "Journal Article", "Report") as a small pill
- **Title** displayed as a heading
- **Summary** (optional short description, populated from the `summary` field in `publications.yaml`)
- **Article image** (optional, from the `image` field) showing a figure, cover page, or screenshot from the paper. Only publications with an `image` field display the image column.
- **Citation** string formatted inline, with status badges for working papers and award highlights
- **Action-button links** for DOI, PDF, and other external resources (populated from the optional `links` field; DOI buttons are auto-generated from the `doi` field if present)

### Alternating image layout

Publication cards with images use an alternating layout: odd-numbered cards show the image on the right, even-numbered cards show it on the left. This creates visual variety as the user scrolls through a theme section.

### Data fields

Each entry in `data/publications.yaml` supports these optional fields for the card layout:

```yaml
- id: example-2024
  type: journal
  title: "Example Paper Title"
  authors: "Smith, J., & Doe, A."
  year: 2024
  journal: "Journal of Examples"
  # ... other standard fields ...

  # Optional card-layout fields:
  summary: "A one-sentence plain-language description of this paper."
  image: "example-2024.png"      # Place file in site/static/images/publications/
  links:
    - label: "PDF"
      url: "https://example.com/paper.pdf"
    - label: "Replication Code"
      url: "https://github.com/example/repo"
```

All three fields (`summary`, `image`, `links`) are fully optional and backward-compatible. Publications without them render a text-only card with title, citation, and auto-generated DOI button (if a `doi` field exists).

### Implementation

The card layout is implemented across three files:

| File | Role |
|------|------|
| `scripts/utils.py` | Validates the optional `summary` (must be a string), `image` (must be a string), and `links` (must be a list of dicts, each with `label` and `url` keys) fields during `validate_data()` |
| `scripts/sync_hugo.py` | Generates HTML card markup (`.pub-card` divs with type badge, title, summary, optional article image, citation, and link buttons) in the publications `_index.md`, organized into collapsible `<details>/<summary>` theme sections with `cascade: build: list: never` to suppress Hugo's default child page listing |
| `site/assets/css/custom.css` | Provides `.pub-card-*` component styles: card container with border and hover shadow, title and summary typography, article image positioning, citation formatting, status/award badges, and responsive link buttons |

---

## Deployment

The site is hosted on **GitHub Pages** with a custom domain at `www.andrew-mceachin.com`. It auto-deploys on every push to `main` via the GitHub Actions workflow at `.github/workflows/deploy.yml`.

The CI pipeline runs:

1. Python 3.12 setup + pip install
2. TeX Live install (latex-base, latex-extra, fonts-recommended, fonts-extra)
3. Hugo Extended 0.156.0 setup
4. Node 20 + npm install
5. `build_all.py` (YAML to Hugo content + CV PDF)
6. `hugo --minify` with production baseURL
7. Upload artifact + deploy to GitHub Pages

**Manual deployment steps (if needed):**

```bash
make build                     # Generate everything
cd site && hugo --minify       # Build static site (already part of make build)
# Push to main branch -- GitHub Actions handles the rest
```

**Custom domain:** `www.andrew-mceachin.com` (configured via `site/static/CNAME`)

---

## Design Notes

### YAML is the single source of truth

All content originates in `data/*.yaml`. The Python scripts generate Hugo markdown and LaTeX from these files. Never hand-edit generated files in `site/content/publications/` -- edit the YAML and rebuild.

### Angle-bracket Jinja2 delimiters

The LaTeX template uses `<< >>` (variable), `<% %>` (block), and `<# #>` (comment) instead of standard Jinja2 `{{ }}` / `{% %}`. This avoids escaping conflicts with LaTeX's heavy use of curly braces.

### `.generated` marker files

The `sync_hugo.py` script places a `.generated` file inside each auto-created publication directory. On rebuild, only directories containing this marker are deleted and recreated. Hand-created content directories are never touched.

### Generated Hugo content is committed

The generated markdown files under `site/content/` are committed to git. This is intentional:
- Enables `hugo server` preview without running the Python pipeline
- Makes content changes visible in `git diff`
- Simplifies CI (Hugo build does not depend on Python for content)

### Collapsible sections use native HTML

The collapsible theme sections on the Publications page use `<details>` and `<summary>` elements. No JavaScript is required -- the browser handles expand/collapse natively.

### Mountain backdrop

A mountain sketch image (`site/static/images/mountains-backdrop.png`) appears as a fixed background on all pages, providing a consistent visual anchor as the user scrolls.

### Custom theme

The site uses a clean academic aesthetic: white background, dark teal (`#1b4965`) accents, Inter font stack, side-by-side biography layout with a mountain sketch backdrop, and alternating gray/white section backgrounds.

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

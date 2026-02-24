"""
utils.py — Shared utilities for academic-site build pipeline.

Provides:
  - Path constants for the project
  - YAML data loading (explicit file list, not glob)
  - Data validation (validate_data)
  - LaTeX special character escaping (latex_escape)
  - Citation formatting helpers
  - Publication filtering helpers
"""

import os
import sys
import re
import yaml
from pathlib import Path


# ---------------------------------------------------------------------------
# Path constants
# ---------------------------------------------------------------------------

# Project root: two levels up from this script
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SITE_DIR = PROJECT_ROOT / "site"
CV_DIR = PROJECT_ROOT / "cv"
CV_TEMPLATE_DIR = CV_DIR / "template"
CV_OUTPUT_DIR = CV_DIR / "output"
CONTENT_DIR = SITE_DIR / "content"
STATIC_DIR = SITE_DIR / "static"

# Explicit list of expected YAML data files (not glob)
EXPECTED_YAML_FILES = [
    "profile.yaml",
    "education.yaml",
    "positions.yaml",
    "publications.yaml",
    "presentations.yaml",
    "media.yaml",
    "grants.yaml",
    "awards.yaml",
    "service.yaml",
    "software.yaml",
]


# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------

def load_all_data() -> dict:
    """
    Load all expected YAML data files from DATA_DIR.

    Returns a dict keyed by filename stem (e.g., 'profile', 'publications').
    Missing files produce a warning on stderr and load as empty dicts.
    Unexpected files in the directory are ignored.
    """
    data = {}
    for filename in EXPECTED_YAML_FILES:
        filepath = DATA_DIR / filename
        stem = filepath.stem  # e.g., 'profile'
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                contents = yaml.safe_load(f)
                # yaml.safe_load returns None for empty files
                data[stem] = contents if contents is not None else {}
        else:
            print(f"WARNING: Expected data file not found: {filepath}", file=sys.stderr)
            data[stem] = {}
    return data


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_data(data: dict) -> list:
    """
    Validate loaded YAML data. Returns a list of error strings.
    An empty list means all checks passed.

    Checks:
      - profile.yaml: has name.display, title, organization, email
      - publications.yaml: every entry has id (str), type (in known set),
        title (str), authors (list), year (int). All IDs are unique.
      - Other files: required top-level keys exist and contain lists.
    """
    errors = []

    # --- profile ---
    profile = data.get("profile", {})
    if not profile:
        errors.append("profile.yaml: file is empty or missing")
    else:
        name = profile.get("name", {})
        if not name.get("display"):
            errors.append("profile.yaml: missing 'name.display'")
        if not profile.get("title"):
            errors.append("profile.yaml: missing 'title'")
        if not profile.get("organization"):
            errors.append("profile.yaml: missing 'organization'")
        if not profile.get("email"):
            errors.append("profile.yaml: missing 'email'")

    # --- publications ---
    pubs_data = data.get("publications", {})
    pubs = pubs_data.get("publications", [])
    if not isinstance(pubs, list):
        errors.append("publications.yaml: 'publications' should be a list")
    else:
        known_types = {
            "journal", "working_paper", "report", "book_chapter",
            "commentary", "policy_brief",
        }
        seen_ids = set()
        for i, pub in enumerate(pubs):
            prefix = f"publications.yaml[{i}]"
            pub_id = pub.get("id")
            if not pub_id or not isinstance(pub_id, str):
                errors.append(f"{prefix}: missing or non-string 'id'")
            elif pub_id in seen_ids:
                errors.append(f"{prefix}: duplicate id '{pub_id}'")
            else:
                seen_ids.add(pub_id)

            pub_type = pub.get("type")
            if pub_type not in known_types:
                errors.append(
                    f"{prefix} (id={pub_id}): type '{pub_type}' not in {known_types}"
                )
            if not pub.get("title") or not isinstance(pub.get("title"), str):
                errors.append(f"{prefix} (id={pub_id}): missing or non-string 'title'")
            if not isinstance(pub.get("authors"), list):
                errors.append(f"{prefix} (id={pub_id}): 'authors' must be a list")
            year = pub.get("year")
            if not isinstance(year, int):
                errors.append(f"{prefix} (id={pub_id}): 'year' must be an integer")

            # Optional fields: summary (str), image (str), and links (list of dicts)
            summary = pub.get("summary")
            if summary is not None and not isinstance(summary, str):
                errors.append(f"{prefix} (id={pub_id}): 'summary' must be a string if provided")

            image = pub.get("image")
            if image is not None and not isinstance(image, str):
                errors.append(f"{prefix} (id={pub_id}): 'image' must be a string if provided")

            links = pub.get("links")
            if links is not None:
                if not isinstance(links, list):
                    errors.append(f"{prefix} (id={pub_id}): 'links' must be a list if provided")
                else:
                    for j, link in enumerate(links):
                        if not isinstance(link, dict):
                            errors.append(f"{prefix} (id={pub_id}): links[{j}] must be a dict")
                        elif not link.get("label") or not link.get("url"):
                            errors.append(f"{prefix} (id={pub_id}): links[{j}] must have 'label' and 'url'")

        # --- theme_order and theme fields ---
        theme_order = pubs_data.get("theme_order", [])
        valid_theme_keys = set()
        if not isinstance(theme_order, list):
            errors.append("publications.yaml: 'theme_order' should be a list")
        else:
            for i, theme in enumerate(theme_order):
                if not isinstance(theme, dict):
                    errors.append(f"publications.yaml: theme_order[{i}] must be a dict")
                else:
                    key = theme.get("key")
                    name = theme.get("name")
                    if not key or not isinstance(key, str):
                        errors.append(f"publications.yaml: theme_order[{i}] missing or non-string 'key'")
                    else:
                        valid_theme_keys.add(key)
                    if not name or not isinstance(name, str):
                        errors.append(f"publications.yaml: theme_order[{i}] missing or non-string 'name'")

        # Validate theme field on all publications
        for i, pub in enumerate(pubs):
            pub_id = pub.get("id", f"[{i}]")
            theme = pub.get("theme")
            if not theme or not isinstance(theme, str):
                errors.append(
                    f"publications.yaml (id={pub_id}): missing or non-string 'theme'"
                )
            elif valid_theme_keys and theme not in valid_theme_keys:
                errors.append(
                    f"publications.yaml (id={pub_id}): theme '{theme}' not in theme_order keys {valid_theme_keys}"
                )

    # --- education ---
    edu_data = data.get("education", {})
    edu = edu_data.get("education", [])
    if not isinstance(edu, list):
        errors.append("education.yaml: 'education' should be a list")

    # --- positions ---
    pos_data = data.get("positions", {})
    pos = pos_data.get("positions", [])
    if not isinstance(pos, list):
        errors.append("positions.yaml: 'positions' should be a list")

    # --- grants ---
    grants_data = data.get("grants", {})
    grants = grants_data.get("grants", [])
    if not isinstance(grants, list):
        errors.append("grants.yaml: 'grants' should be a list")

    # --- awards ---
    awards_data = data.get("awards", {})
    awards = awards_data.get("awards", [])
    if not isinstance(awards, list):
        errors.append("awards.yaml: 'awards' should be a list")

    # --- service ---
    service_data = data.get("service", {})
    for key in ["editorial_boards", "referee", "committees"]:
        val = service_data.get(key, [])
        if not isinstance(val, list):
            errors.append(f"service.yaml: '{key}' should be a list")

    # --- presentations ---
    pres_data = data.get("presentations", {})
    pres = pres_data.get("presentations", [])
    if not isinstance(pres, list):
        errors.append("presentations.yaml: 'presentations' should be a list")

    # --- media ---
    media_data = data.get("media", {})
    for key in ["commentary", "news_coverage", "podcasts_interviews"]:
        val = media_data.get(key, [])
        if not isinstance(val, list):
            errors.append(f"media.yaml: '{key}' should be a list")

    # --- software ---
    sw_data = data.get("software", {})
    sw = sw_data.get("software", [])
    if not isinstance(sw, list):
        errors.append("software.yaml: 'software' should be a list")

    return errors


# ---------------------------------------------------------------------------
# LaTeX escaping
# ---------------------------------------------------------------------------

# Characters that must be escaped for LaTeX
_LATEX_SPECIAL = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

# Compiled regex for the special characters
_LATEX_SPECIAL_RE = re.compile(
    "|".join(re.escape(k) for k in _LATEX_SPECIAL.keys())
)


def latex_escape(text) -> str:
    """
    Escape LaTeX special characters in text.

    Handles: & % $ # _ { } ~ ^
    Passes through UTF-8 characters (accented names like Hernández, Müller)
    untouched — LaTeX handles these via inputenc/fontenc.

    Returns empty string for None or non-string input.
    """
    if text is None:
        return ""
    text = str(text)
    return _LATEX_SPECIAL_RE.sub(lambda m: _LATEX_SPECIAL[m.group()], text)


# ---------------------------------------------------------------------------
# Citation formatting
# ---------------------------------------------------------------------------

def format_authors(authors: list, max_display: int = 0) -> str:
    """
    Format an author list as a string.
    If max_display > 0, truncates after that many authors with 'et al.'
    """
    if not authors:
        return ""
    if max_display > 0 and len(authors) > max_display:
        return ", ".join(authors[:max_display]) + ", et al."
    return ", ".join(authors[:-1]) + ", & " + authors[-1] if len(authors) > 1 else authors[0]


# ---------------------------------------------------------------------------
# Publication filtering
# ---------------------------------------------------------------------------

def filter_pubs_by_type(pubs: list, pub_type: str) -> list:
    """Filter publications list to those matching a given type."""
    return [p for p in pubs if p.get("type") == pub_type]


def filter_pubs_by_theme(pubs: list, theme_key: str) -> list:
    """Filter publications list to those matching a given theme."""
    return [p for p in pubs if p.get("theme") == theme_key]


def get_featured_pubs(pubs: list) -> list:
    """Return publications marked as featured, sorted by year descending."""
    featured = [p for p in pubs if p.get("featured")]
    return sorted(featured, key=lambda p: p.get("year", 0), reverse=True)


def format_amount(amount) -> str:
    """Format a dollar amount with commas for use in LaTeX (no curly braces)."""
    if amount is None:
        return ""
    return "{:,.0f}".format(amount)

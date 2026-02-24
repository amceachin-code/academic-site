"""
build_cv.py — Generate LaTeX CV from YAML data using Jinja2, then compile to PDF.

Key safeguards:
  - Angle-bracket Jinja2 delimiters (<< >>, <% %>, <# #>) to avoid LaTeX {} conflicts
  - latex_escape filter applied to ALL text fields in the template
  - PDF existence and size check after pdflatex
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Add parent to path so we can import utils
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    load_all_data,
    validate_data,
    latex_escape,
    format_authors,
    format_amount,
    filter_pubs_by_type,
    CV_TEMPLATE_DIR,
    CV_OUTPUT_DIR,
)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: Jinja2 is required. Install with: pip install Jinja2==3.1.5", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Jinja2 environment with angle-bracket delimiters
# ---------------------------------------------------------------------------

def create_jinja_env() -> Environment:
    """
    Create a Jinja2 environment with angle-bracket delimiters for LaTeX.

    Uses:
      << variable >>    instead of {{ variable }}
      <% block %>       instead of {% block %}
      <# comment #>     instead of {# comment #}
    """
    env = Environment(
        loader=FileSystemLoader(str(CV_TEMPLATE_DIR)),
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        comment_start_string="<#",
        comment_end_string="#>",
        # Strip whitespace around block tags for cleaner LaTeX output
        trim_blocks=True,
        lstrip_blocks=True,
        # Keep single trailing newline
        keep_trailing_newline=True,
        # Auto-escape is OFF (we use latex_escape filter explicitly)
        autoescape=False,
    )

    # Register the latex_escape filter
    env.filters["latex_escape"] = latex_escape

    return env


# ---------------------------------------------------------------------------
# Render LaTeX from template + data
# ---------------------------------------------------------------------------

def render_cv(data: dict) -> str:
    """Render the CV LaTeX template with the loaded YAML data."""
    env = create_jinja_env()
    template = env.get_template("cv_template.tex.j2")

    # Flatten data for easier template access
    context = {
        "profile": data.get("profile", {}),
        "education": data.get("education", {}).get("education", []),
        "positions": data.get("positions", {}).get("positions", []),
        "publications": data.get("publications", {}).get("publications", []),
        "grants": data.get("grants", {}).get("grants", []),
        "awards": data.get("awards", {}).get("awards", []),
        "service": data.get("service", {}),
        "presentations": data.get("presentations", {}).get("presentations", []),
        "media": data.get("media", {}),
        "software": data.get("software", {}).get("software", []),
    }

    # Add helper functions to template context
    context["filter_pubs_by_type"] = filter_pubs_by_type
    context["format_authors"] = format_authors
    context["format_amount"] = format_amount

    return template.render(**context)


# ---------------------------------------------------------------------------
# Compile LaTeX to PDF
# ---------------------------------------------------------------------------

def compile_pdf(tex_path: Path, output_dir: Path) -> bool:
    """
    Run pdflatex on the .tex file. Returns True if PDF was produced successfully.
    Runs twice to resolve cross-references.
    """
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-output-directory", str(output_dir),
        str(tex_path),
    ]

    first_run_output = ""
    for run_num in range(2):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(output_dir),
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            print(
                f"ERROR: pdflatex run {run_num + 1} timed out after 120 seconds",
                file=sys.stderr,
            )
            return False
        if run_num == 0:
            first_run_output = result.stdout
        if result.returncode != 0:
            print(
                f"WARNING: pdflatex run {run_num + 1} exited with code {result.returncode}",
                file=sys.stderr,
            )

    # Verify PDF exists and is non-empty (the definitive success check)
    pdf_path = output_dir / tex_path.with_suffix(".pdf").name
    if not pdf_path.exists():
        print(f"ERROR: PDF not found at {pdf_path} after pdflatex", file=sys.stderr)
        # Print last 30 lines of first run output for diagnostics
        log_lines = first_run_output.split("\n")
        for line in log_lines[-30:]:
            print(f"  {line}", file=sys.stderr)
        return False
    if pdf_path.stat().st_size == 0:
        print(f"ERROR: PDF at {pdf_path} is 0 bytes", file=sys.stderr)
        return False

    # Check the .log file for LaTeX errors (pdflatex can produce a PDF even with errors)
    log_path = output_dir / tex_path.with_suffix(".log").name
    if log_path.exists():
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
        if "! " in log_text:
            # LaTeX errors start with "! " — warn but don't fail (PDF may still be usable)
            error_lines = [l for l in log_text.split("\n") if l.startswith("! ")]
            if error_lines:
                print("WARNING: LaTeX errors detected in log:", file=sys.stderr)
                for line in error_lines[:5]:
                    print(f"  {line}", file=sys.stderr)

    return True


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main(data: dict = None):
    """
    Main entry point. Accepts pre-loaded data dict, or loads from YAML.
    When data is pre-provided (from build_all.py), validation is skipped
    since the orchestrator already validated.
    """
    if data is None:
        data = load_all_data()
        # Only validate when loading our own data
        errors = validate_data(data)
        if errors:
            print("Validation errors:", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            sys.exit(1)

    # Check template exists
    template_path = CV_TEMPLATE_DIR / "cv_template.tex.j2"
    if not template_path.exists():
        print(f"ERROR: CV template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    CV_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Render
    print("Building CV from YAML data...")
    tex_content = render_cv(data)
    tex_path = CV_OUTPUT_DIR / "McEachin_CV.tex"
    tex_path.write_text(tex_content, encoding="utf-8")
    print(f"  Generated LaTeX at {tex_path}")

    # Compile
    print("  Compiling PDF...")
    success = compile_pdf(tex_path, CV_OUTPUT_DIR)
    if success:
        pdf_path = CV_OUTPUT_DIR / "McEachin_CV.pdf"
        size_kb = pdf_path.stat().st_size / 1024
        print(f"  PDF compiled successfully: {pdf_path} ({size_kb:.1f} KB)")
    else:
        print("  ERROR: PDF compilation failed", file=sys.stderr)
        sys.exit(1)

    print("Done building CV.")


if __name__ == "__main__":
    main()

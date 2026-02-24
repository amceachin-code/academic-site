"""
build_all.py — Orchestrator for the academic-site build pipeline.

Imports and calls sync_hugo and build_cv as Python functions (no subprocess).
Supports --validate flag for dry-run validation only.

Usage:
    python scripts/build_all.py             # Full build
    python scripts/build_all.py --validate  # Validate only (no file generation)
"""

import sys
import argparse
from pathlib import Path

# Add parent to path so we can import sibling modules
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import load_all_data, validate_data


def main():
    parser = argparse.ArgumentParser(description="Build academic site + CV from YAML data")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Only validate YAML data, do not generate files",
    )
    args = parser.parse_args()

    # Load data once, share across both pipelines
    print("Loading YAML data...")
    data = load_all_data()

    # Validate
    errors = validate_data(data)
    if errors:
        print("Validation errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("  All data validated successfully.")

    if args.validate:
        print("Validation-only mode: exiting without generating files.")
        return

    # Import and run sync_hugo
    from sync_hugo import main as sync_hugo_main
    sync_hugo_main(data=data)

    # Import and run build_cv
    from build_cv import main as build_cv_main
    build_cv_main(data=data)

    print("\nAll builds completed successfully.")


if __name__ == "__main__":
    main()

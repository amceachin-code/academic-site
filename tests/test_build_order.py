"""
Tests for build_all.py step ordering.

Run with: python -m pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_all
import build_cv
import sync_hugo


def test_cv_pdf_copied_after_cv_is_built(monkeypatch):
    """The site's CV copy must come from this build, not the previous one."""
    calls = []
    monkeypatch.setattr(sys, "argv", ["build_all.py"])
    monkeypatch.setattr(build_all, "load_all_data", lambda: {})
    monkeypatch.setattr(build_all, "validate_data", lambda data: [])
    monkeypatch.setattr(
        sync_hugo, "main",
        lambda data=None, copy_pdf=True: calls.append(("sync", copy_pdf)),
    )
    monkeypatch.setattr(build_cv, "main", lambda data=None: calls.append(("cv",)))
    monkeypatch.setattr(sync_hugo, "copy_cv_pdf", lambda: calls.append(("copy",)))

    build_all.main()

    assert calls == [("sync", False), ("cv",), ("copy",)]

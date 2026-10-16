"""
Tests for the hand-made Students & Guardians tools page and its menu entry.

The page links to tools that live in their own repos and are served by
GitHub Pages under this domain, so these tests guard the pieces that
connect them: the page must survive sync_hugo.py, appear in the menu, and
link to each tool by its repo path.

Run with: python -m pytest tests/
"""

from pathlib import Path

import yaml

SITE = Path(__file__).resolve().parent.parent / "site"
TOOLS_DIR = SITE / "content" / "tools"
MENUS = SITE / "config" / "_default" / "menus.yaml"


def test_tools_page_is_hand_made():
    # sync_hugo.py deletes any content folder holding a .generated marker,
    # so this folder must never have one.
    assert (TOOLS_DIR / "_index.md").exists()
    assert not (TOOLS_DIR / ".generated").exists()


def test_menu_links_to_tools_page():
    menu = yaml.safe_load(MENUS.read_text())["main"]
    entry = next(m for m in menu if m["url"] == "/tools/")
    assert entry["name"] == "Students & Guardians"


def test_page_links_each_tool_by_repo_path():
    text = (TOOLS_DIR / "_index.md").read_text()
    for repo in ["grade-inflation", "multiplication-worksheet"]:
        assert f"](/{repo}/)" in text
    # Only the worksheets show their repo; grade-inflation links to the tool alone.
    assert "https://github.com/amceachin-code/multiplication-worksheet" in text
    assert "https://github.com/amceachin-code/grade-inflation" not in text


def test_page_links_division_worksheet():
    # The division tool lives in a subfolder of the multiplication-worksheet repo.
    text = (TOOLS_DIR / "_index.md").read_text()
    assert "](/multiplication-worksheet/division/)" in text

"""
Tests for the Claude Code Skills section of the Code page.

Run with: python -m pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from sync_hugo import _format_claude_skills


def test_no_skills_omits_section():
    assert _format_claude_skills([]) == []


def test_skill_renders_heading_usage_and_link():
    url = "https://github.com/example/skills/tree/main/demo"
    lines = _format_claude_skills(
        [{"name": "demo", "description": "Does a thing.\n", "github": url}]
    )
    assert lines[0] == "## Claude Code Skills"
    assert "### demo" in lines
    assert "Does a thing." in lines
    assert "**Usage:** `/demo`" in lines
    assert f"**GitHub:** [{url}]({url})" in lines


def test_skill_without_github_has_no_link_line():
    lines = _format_claude_skills([{"name": "demo", "description": "x"}])
    assert not any(line.startswith("**GitHub:**") for line in lines)

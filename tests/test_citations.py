"""
Tests for citation formatting and HTML escaping in the build pipeline.

Run with: python -m pytest tests/
"""

import sys
from pathlib import Path

# Add scripts/ to path so we can import the modules under test
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from utils import format_authors, latex_escape
from sync_hugo import _format_citation_html, _html_escape, _yaml_escape


# ---------------------------------------------------------------------------
# format_authors
# ---------------------------------------------------------------------------

class TestFormatAuthors:
    def test_single_author(self):
        assert format_authors(["McEachin, A."]) == "McEachin, A."

    def test_two_authors(self):
        result = format_authors(["McEachin, A.", "Atteberry, A."])
        assert result == "McEachin, A., & Atteberry, A."

    def test_three_authors(self):
        result = format_authors(["A", "B", "C"])
        assert result == "A, B, & C"

    def test_many_authors(self):
        authors = ["A", "B", "C", "D", "E"]
        result = format_authors(authors)
        assert result == "A, B, C, D, & E"

    def test_empty_list(self):
        assert format_authors([]) == ""

    def test_truncation(self):
        authors = ["A", "B", "C", "D", "E"]
        result = format_authors(authors, max_display=3)
        assert result == "A, B, C, et al."


# ---------------------------------------------------------------------------
# _format_citation_html
# ---------------------------------------------------------------------------

class TestFormatCitationHtml:
    def test_journal_article(self):
        pub = {
            "authors": ["McEachin, A.", "Atteberry, A."],
            "year": 2017,
            "title": "Summer learning loss",
            "journal": "Education Finance and Policy",
            "volume": "12",
            "issue": "4",
            "pages": "468-491",
        }
        result = _format_citation_html(pub)
        assert "(2017)." in result
        assert "Summer learning loss." in result
        assert "<em>Education Finance and Policy</em>" in result
        assert "12(4)" in result
        assert "468-491" in result

    def test_accepted_paper_no_year(self):
        """Accepted papers should show (Accepted) instead of year."""
        pub = {
            "authors": ["Carbonari, M.V.", "McEachin, A."],
            "year": 2025,
            "title": "Recovery interventions",
            "journal": "EEPA",
            "status": "Accepted",
        }
        result = _format_citation_html(pub)
        assert "(Accepted)." in result
        assert "(2025)" not in result

    def test_book_chapter(self):
        pub = {
            "authors": ["McEachin, A."],
            "year": 2014,
            "title": "Agency Theory",
            "book": "Encyclopedia of Education Economics and Finance",
            "editors": "Brewer, D.J., & Picus, L.",
            "publisher": "Sage",
        }
        result = _format_citation_html(pub)
        assert "In Brewer, D.J., &amp; Picus, L. (Eds.)," in result
        assert "<em>Encyclopedia of Education Economics and Finance</em>" in result
        assert "Sage." in result

    def test_report_with_publisher(self):
        pub = {
            "authors": ["Kuhfeld, M.", "McEachin, A."],
            "year": 2023,
            "title": "Benchmarks report",
            "publisher": "NWEA",
        }
        result = _format_citation_html(pub)
        assert "NWEA." in result

    def test_article_number_instead_of_pages(self):
        pub = {
            "authors": ["Yoo, P.", "McEachin, A."],
            "year": 2025,
            "title": "Virtual Charter",
            "journal": "Social Science Research",
            "volume": "132",
            "article_number": "103240",
        }
        result = _format_citation_html(pub)
        assert "103240" in result
        # pages not present, so article_number should appear
        assert "132" in result

    def test_missing_fields_no_crash(self):
        """Minimal pub with only required fields should not crash."""
        pub = {"authors": [], "year": 2020, "title": "Test"}
        result = _format_citation_html(pub)
        assert "(2020)." in result
        assert "Test." in result


# ---------------------------------------------------------------------------
# _html_escape
# ---------------------------------------------------------------------------

class TestHtmlEscape:
    def test_ampersand(self):
        assert _html_escape("A & B") == "A &amp; B"

    def test_angle_brackets(self):
        assert _html_escape("<script>") == "&lt;script&gt;"

    def test_quotes(self):
        assert _html_escape('"hello"') == "&quot;hello&quot;"

    def test_empty(self):
        assert _html_escape("") == ""

    def test_none(self):
        assert _html_escape(None) == ""


# ---------------------------------------------------------------------------
# _yaml_escape
# ---------------------------------------------------------------------------

class TestYamlEscape:
    def test_quotes(self):
        assert _yaml_escape('He said "hello"') == 'He said \\"hello\\"'

    def test_backslash(self):
        assert _yaml_escape("a\\b") == "a\\\\b"

    def test_newline(self):
        assert _yaml_escape("line1\nline2") == "line1\\nline2"

    def test_tab(self):
        assert _yaml_escape("a\tb") == "a\\tb"

    def test_empty(self):
        assert _yaml_escape("") == ""


# ---------------------------------------------------------------------------
# latex_escape
# ---------------------------------------------------------------------------

class TestLatexEscape:
    def test_ampersand(self):
        assert latex_escape("A & B") == r"A \& B"

    def test_percent(self):
        assert latex_escape("50%") == r"50\%"

    def test_hash(self):
        assert latex_escape("#1") == r"\#1"

    def test_none(self):
        assert latex_escape(None) == ""

    def test_passthrough_unicode(self):
        assert latex_escape("Hernández") == "Hernández"

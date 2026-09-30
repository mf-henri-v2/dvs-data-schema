"""Tests for tools/compare_with_govuk.py.

Run from the repository root:
    python -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import compare_with_govuk as cg  # noqa: E402

BANNER = (
    "<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->\n"
    "> [!CAUTION]\n> Working draft.\n<!-- caution-banner:end -->\n\n"
)
FOOTER = "\n---\n\n**Repository navigation**\n\n[Repository home](../../README.md)\n"
NBSP = " "

# One GOV.UK page, as its content API returns it: typographic quotes, non-breaking
# spaces for indentation, links within the page, and a table with row headings.
GOVUK = f"""<div class="govspeak"><h2 id="data-model">Data model</h2>
<p>The person’s claim (‘claims’), see the
<a href="https://www.gov.uk/guidance">guidance</a>.</p>
<ul>
  <li>their given name</li>
  <li><p>their date of birth</p></li>
</ul>
<h3 id="claims">Claims</h3>
<div class="example">
  <p>claims:</p>

  <p>{NBSP * 4} given_name: string</p>

  <p>{NBSP * 4} birthdate: <a href="#date">date</a></p>

  <p>{NBSP * 4} trust_framework: ‘uk_dvstf’</p>
</div>
<h2 id="data-dictionary">Data dictionary</h2>
<h3 id="date">Date</h3>
<p>Dates must be in ISO 8601 ‘YYYY-MM-DD’ format</p>
<h3 id="predefined-lists">Predefined lists</h3>
<table>
  <thead><tr><th scope="col">Element</th><th scope="col">Predefined values</th><th scope="col">Notes</th></tr></thead>
  <tbody>
    <tr><th scope="row">assurance_level</th><td>low, medium, high</td><td>Levels from GPG 45</td></tr>
    <tr><th scope="row">encoding_format</th><td>base64, byte_data</td><td>{NBSP}</td></tr>
  </tbody>
</table>
</div>"""

# The same text as three section files.
MODEL = """## Data model

The person's claim ('claims'), see the [guidance](https://www.gov.uk/guidance).

- their given name

- their date of birth

### Claims

<pre class="schema-example">
claims:
     given_name: string
     birthdate: <a href="04-data-dictionary.md#date">date</a>
     trust_framework: 'uk_dvstf'
</pre>
"""
DICTIONARY = """## Data dictionary

### Date

Dates must be in ISO 8601 'YYYY-MM-DD' format
"""
LISTS = """## Predefined lists

| Element | Predefined values | Notes |
| --- | --- | --- |
| **assurance_level** | low, medium, high | Levels from GPG 45 |
| **encoding_format** | base64, byte_data | |
"""


def files(model: str = MODEL, dictionary: str = DICTIONARY, lists: str = LISTS) -> list[tuple[str, str]]:
    sources = {"03-data-model.md": model, "04-data-dictionary.md": dictionary, "06-predefined-lists.md": lists}
    return [(name, BANNER + source + FOOTER) for name, source in sources.items()]


def problems(**changed: str) -> list[str]:
    """Differences reported when one or more of the section files is changed."""
    section_files = files(**changed)
    starts, count = set(), 0
    for name, source in section_files:
        starts.add(count)
        count += len(cg.parse_markdown([(name, source)]).headings)
    return cg.compare(cg.parse_govuk(GOVUK), cg.parse_markdown(section_files), starts)


class MatchingText(unittest.TestCase):
    def test_the_same_text_in_both_forms_has_no_differences(self):
        self.assertEqual(problems(), [])

    def test_the_comparison_covers_examples_tables_and_links(self):
        guide = cg.parse_govuk(GOVUK)
        kinds = {kind for kind, _ in guide.records}
        self.assertLessEqual({"heading", "paragraph", "list item", "example line", "table column headings", "table row"}, kinds)
        self.assertIn(("example line", "5|birthdate: date"), guide.records)
        self.assertIn(("table row", "assurance_level [row heading] | low, medium, high | Levels from GPG 45"), guide.records)
        self.assertEqual(guide.links, [("guidance", "https://www.gov.uk/guidance"), ("date", "#date")])


class Differences(unittest.TestCase):
    def assertReported(self, found: list[str], *fragments: str) -> None:
        text = "\n".join(found)
        self.assertTrue(found, "expected a difference to be reported")
        for fragment in fragments:
            self.assertIn(fragment, text)

    def test_a_changed_word(self):
        self.assertReported(problems(dictionary=DICTIONARY.replace("must be", "should be")), "paragraph: Dates should be")

    def test_a_name_that_differs_only_in_case(self):
        self.assertReported(problems(model=MODEL.replace("given_name", "Given_name")), "example line: 5|Given_name: string")

    def test_changed_indentation_in_an_example(self):
        self.assertReported(problems(model=MODEL.replace("     given_name", "    given_name")), "4|given_name: string")

    def test_a_removed_example_line(self):
        self.assertReported(problems(model=MODEL.replace("     given_name: string\n", "")), "repository: (nothing)")

    def test_example_lines_in_a_different_order(self):
        swapped = MODEL.replace("     given_name: string\n", "").replace("</pre>", "     given_name: string\n</pre>")
        self.assertReported(problems(model=swapped), "given_name")

    def test_a_changed_table_cell(self):
        self.assertReported(problems(lists=LISTS.replace("low, medium, high", "low, medium")), "table row: assurance_level")

    def test_a_missing_row_heading(self):
        self.assertReported(problems(lists=LISTS.replace("**encoding_format**", "encoding_format")),
                            "repository: table row: encoding_format | base64, byte_data |")

    def test_a_cell_added_where_gov_uk_has_none(self):
        self.assertReported(problems(lists=LISTS.replace("byte_data | |", "byte_data | Encodings |")), "Encodings")

    def test_a_paragraph_split_in_two(self):
        self.assertReported(problems(dictionary=DICTIONARY.replace("ISO 8601 ", "ISO 8601\n\n")),
                            "repository: paragraph: Dates must be in ISO 8601")

    def test_a_link_that_goes_somewhere_else(self):
        self.assertReported(problems(model=MODEL.replace("04-data-dictionary.md#date", "04-data-dictionary.md#timestamp")),
                            "link:", "[date] -> #timestamp")

    def test_a_link_that_was_removed(self):
        self.assertReported(problems(model=MODEL.replace("[guidance](https://www.gov.uk/guidance)", "guidance")), "link:")

    def test_a_renamed_heading(self):
        self.assertReported(problems(dictionary=DICTIONARY.replace("### Date", "### Dates")), "heading: Dates")

    def test_a_heading_at_a_different_depth(self):
        self.assertReported(problems(dictionary=DICTIONARY.replace("### Date", "#### Date")), "heading level", "Date: +2")

    def test_a_table_that_is_not_a_table(self):
        self.assertReported(problems(lists=LISTS.replace("| --- | --- | --- |\n", "")), "malformed table")


class Presentation(unittest.TestCase):
    """The differences in presentation that the tool treats as the same text."""

    def test_the_first_heading_of_a_file_may_be_promoted(self):
        # On GOV.UK "Predefined lists" is a level 3 heading. In its own file it is level 2.
        self.assertEqual(problems(), [])

    def test_typographic_quotes_match_straight_quotes(self):
        self.assertEqual(cg.clean("the person’s ‘claims’"), "the person's 'claims'")

    def test_example_indentation_counts_both_kinds_of_space(self):
        self.assertEqual(cg.example_line(f"{NBSP * 4} claims: object"), cg.example_line("     claims: object"))
        self.assertNotEqual(cg.example_line(f"{NBSP * 4}claims: object"), cg.example_line("     claims: object"))

    def test_heading_ids_are_the_ones_github_gives(self):
        self.assertEqual(cg.github_slug("GPG 45 Data model"), "gpg-45-data-model")
        self.assertEqual(cg.github_slug("Table D1: Data elements - descriptions"), "table-d1-data-elements---descriptions")


class RepositoryMaterial(unittest.TestCase):
    def test_only_the_banner_and_footer_are_removed(self):
        self.assertEqual(cg.strip_furniture(BANNER + DICTIONARY + FOOTER, "file.md").strip("\n"), DICTIONARY.strip("\n"))

    def test_a_horizontal_rule_in_the_text_is_kept(self):
        text = cg.strip_furniture(BANNER + "## Title\n\nBefore.\n\n---\n\nAfter.\n" + FOOTER, "file.md")
        self.assertIn("After.", text)

    def test_a_file_without_a_banner_or_footer_is_refused(self):
        for source in (DICTIONARY + FOOTER, BANNER + DICTIONARY):
            with self.assertRaises(ValueError):
                cg.strip_furniture(source, "file.md")


class CommandLine(unittest.TestCase):
    """Run the tool against saved pages and a temporary copy of the section files."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.saved = self.root / "saved"
        self.saved.mkdir()
        page = '<div class="govspeak"><h2 id="introduction">Introduction</h2><p>Text.</p></div>'
        for guide in cg.GUIDES:
            (self.saved / f"{guide}.html").write_text(page, encoding="utf-8")
            folder = self.root / cg.SCHEMA_DIR / guide
            folder.mkdir(parents=True)
            for name in cg.SECTION_FILES:
                body = "## Introduction\n\nText.\n" if name == cg.SECTION_FILES[0] else ""
                (folder / name).write_text(BANNER + body + FOOTER, encoding="utf-8")

    def run_tool(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return cg.main(["--html-dir", str(self.saved), "--root", str(self.root)])

    def test_matching_text_passes(self):
        self.assertEqual(self.run_tool(), 0)

    def test_a_difference_fails(self):
        path = self.root / cg.SCHEMA_DIR / "gpg-44" / cg.SECTION_FILES[0]
        path.write_text(path.read_text(encoding="utf-8").replace("Text.", "Other text."), encoding="utf-8")
        self.assertEqual(self.run_tool(), 1)

    def test_a_missing_file_is_an_error_not_a_pass(self):
        (self.root / cg.SCHEMA_DIR / "gpg-45" / cg.SECTION_FILES[2]).unlink()
        self.assertEqual(self.run_tool(), 2)


if __name__ == "__main__":
    unittest.main()

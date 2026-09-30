"""Tests for tools/check_links.py.

Run from the repository root:
    python -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import check_links as cl  # noqa: E402


class Slugs(unittest.TestCase):
    def test_matches_github_heading_ids(self):
        cases = {
            "GPG 45 Data model": "gpg-45-data-model",
            "Table D1: Data elements - descriptions": "table-d1-data-elements---descriptions",
            "GPG 45 — contents": "gpg-45--contents",
            "How it works": "how-it-works",
            "GitHub, GOV.UK and who decides": "github-govuk-and-who-decides",
            "Give feedback on `main`": "give-feedback-on-main",
            "snake_case stays": "snake_case-stays",
        }
        for heading, slug in cases.items():
            with self.subTest(heading=heading):
                self.assertEqual(cl.github_slug(heading), slug)

    def test_repeated_headings_are_numbered(self):
        ids = cl.anchors_in("## Back\n\ntext\n\n## Back\n")
        self.assertEqual({"back", "back-1"}, ids)

    def test_html_anchors_are_found(self):
        self.assertIn("date-format", cl.anchors_in('#### Date\n<a id="date-format"></a>\n'))

    def test_headings_inside_code_fences_are_ignored(self):
        self.assertNotIn("not-a-heading", cl.anchors_in("```\n# Not a heading\n```\n"))


class Links(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "part").mkdir()
        (self.root / "part" / "README.md").write_text('# Part 3\n<a id="part-3"></a>\n', encoding="utf-8")

    def problems(self, text: str) -> list[str]:
        (self.root / "page.md").write_text(text, encoding="utf-8")
        return [message for _, _, message in cl.check_links(self.root)]

    def test_valid_links_pass(self):
        self.assertEqual(self.problems("[Part](part/README.md#part-3) [Self](#page) [Folder](part/)\n\n# Page\n"), [])

    def test_missing_file_is_reported(self):
        self.assertEqual(self.problems("[Changes](CHANGELOG.md)\n"), ["target does not exist: CHANGELOG.md"])

    def test_missing_anchor_is_reported(self):
        self.assertEqual(self.problems("[Part](part/README.md#part-4)\n"), ["anchor not found: part/README.md#part-4"])

    def test_link_outside_the_repository_is_reported(self):
        self.assertEqual(self.problems("[New issue](../../issues/new/choose)\n"),
                         ["link leaves the repository: ../../issues/new/choose"])

    def test_external_links_are_not_checked(self):
        self.assertEqual(self.problems("[GOV.UK](https://www.gov.uk/) [Mail](mailto:someone@example.com)\n"), [])

    def test_links_in_code_are_not_checked(self):
        self.assertEqual(self.problems("`[x](missing.md)`\n\n```\n[x](missing.md)\n```\n"), [])

    def test_images_are_checked(self):
        self.assertEqual(self.problems("![Figure](media/missing.svg)\n"), ["target does not exist: media/missing.svg"])


CONTENTS_PAGE = (
    "## GPG 45: identity checking\n\n- [1. Introduction](gpg-45/01-introduction.md)\n- [2. Data model](gpg-45/02-data-model.md)\n\n"
    "## GPG 44: authentication\n\n- [1. Introduction](gpg-44/01-introduction.md)\n- [2. Data model](gpg-44/02-data-model.md)\n\n"
    "## Give feedback\n\n- [1. Not a section](../CONTRIBUTING.md)\n"
)
GUIDES = ["GPG 45: identity checking", "GPG 44: authentication", *cl.OTHER_GUIDES]
SECTIONS = ["1. Introduction", "2. Data model", cl.NO_SECTION]


class IssueForms(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "schema-1.0").mkdir()
        (self.root / "schema-1.0" / "README.md").write_text(CONTENTS_PAGE, encoding="utf-8")
        (self.root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)

    def form(self, guides: list[str] | None, sections: list[str] | None) -> list[str]:
        body = "body:\n"
        for field, options in (("guide", guides), ("section", sections)):
            if options is None:
                continue
            lines = "".join(f'        - "{o}"\n' for o in options)
            body += (f"  - type: dropdown\n    id: {field}\n    attributes:\n      label: \"Which {field}?\"\n"
                     f"      options:\n{lines}    validations:\n      required: true\n")
        body += '  - type: textarea\n    id: feedback\n    attributes:\n      label: "What is your feedback?"\n'
        (self.root / ".github" / "ISSUE_TEMPLATE" / "1-form.yml").write_text(body, encoding="utf-8")
        return [message for _, _, message in cl.check_issue_forms(self.root)]

    def test_matching_choices_pass(self):
        self.assertEqual(self.form(GUIDES, SECTIONS), [])

    def test_links_under_other_headings_are_not_sections(self):
        guides, sections, problems = cl.contents_choices(CONTENTS_PAGE)
        self.assertEqual(guides, GUIDES[:2])
        self.assertEqual(sections, SECTIONS[:2])
        self.assertEqual(problems, [])

    def test_missing_or_renamed_section_is_reported(self):
        self.assertEqual(len(self.form(GUIDES, ["1. Introduction", cl.NO_SECTION])), 1)
        self.assertEqual(len(self.form(GUIDES, ["1. Intro", "2. Data model", cl.NO_SECTION])), 1)

    def test_missing_guide_is_reported(self):
        problems = self.form(GUIDES[1:], SECTIONS)
        self.assertEqual(len(problems), 1)
        self.assertIn("'guide' choices", problems[0])

    def test_a_form_without_these_questions_is_not_checked(self):
        self.assertEqual(self.form(None, None), [])

    def test_guides_must_list_the_same_sections(self):
        (self.root / "schema-1.0" / "README.md").write_text(
            CONTENTS_PAGE.replace("- [2. Data model](gpg-44/02-data-model.md)\n", ""), encoding="utf-8")
        self.assertTrue(any("does not list the same sections" in p for p in self.form(GUIDES, SECTIONS)))


if __name__ == "__main__":
    unittest.main()

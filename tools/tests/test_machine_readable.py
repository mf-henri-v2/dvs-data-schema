"""Tests for tools/machine_readable.py.

Run from the repository root:
    python -m unittest discover -s tools/tests -v
"""

from __future__ import annotations

import csv
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))

import machine_readable as mr  # noqa: E402

try:
    import yaml
except ImportError:  # PyYAML is not part of Python; the round-trip test is skipped without it
    yaml = None

MODEL = """## Data model

<pre class="schema-example">
verification:
     trust_framework: 'uk_dvstf'
     evidence: array (<a href="#evidence">evidence</a>)
     assurance_level: <a href="06-predefined-lists.md#predefined-lists">assurance_level</a>
</pre>

<pre class="schema-example">
evidence:
     document: object (<a href="#document">document</a>)
</pre>
"""
VALUES = """## Predefined values

| Predefined value | Definition |
| --- | --- |
| bvp | Biometric verification, the use of a biometric modality (such as face) |
| kbv | Questions that only the owner "should know" |
"""
LISTS = """## Predefined lists

| Element | Type | Predefined values | Notes |
| --- | --- | --- | --- |
| **assurance_level** | string | low, medium, high | Confidence levels |
| **document_type** | string | bus_pass,education_certificate | |
"""
DICTIONARY = (
    "element,sub_element,type,description,source\n"
    "verification,trust_framework,'uk_dvstf',Fixed value,03-data-model.md\n"
    "verification,evidence,array,\"The evidence, as a list\",03-data-model.md\n"
    "verification,assurance_level,assurance_level,The level achieved,03-data-model.md\n"
    "evidence,document,object,A document,03-data-model.md\n"
)


def rows(text: str = DICTIONARY) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


class Tables(unittest.TestCase):
    def test_cells_are_copied_exactly(self):
        table = mr.markdown_tables(VALUES)[0]
        self.assertEqual(table[0], ["Predefined value", "Definition"])
        self.assertEqual(table[1], ["bvp", "Biometric verification, the use of a biometric modality (such as face)"])

    def test_bold_row_headings_lose_only_their_markers(self):
        table = mr.markdown_tables(LISTS)[0]
        self.assertEqual(table[1][0], "assurance_level")
        self.assertEqual(table[2], ["document_type", "string", "bus_pass,education_certificate", ""])

    def test_csv_can_be_read_back_as_the_same_cells(self):
        table = mr.markdown_tables(VALUES)[0]
        self.assertEqual(list(csv.reader(io.StringIO(mr.to_csv(table)))), table)

    def test_text_that_only_looks_like_a_table_row_is_not_a_table(self):
        self.assertEqual(mr.markdown_tables("| not a table |\n\nText.\n"), [])


class DataModel(unittest.TestCase):
    def test_every_example_line_is_read_with_its_published_type(self):
        self.assertEqual(mr.model_fields(MODEL), [
            ("verification", "trust_framework", "'uk_dvstf'"),
            ("verification", "evidence", "array (evidence)"),
            ("verification", "assurance_level", "assurance_level"),
            ("evidence", "document", "object (document)"),
        ])

    def test_an_element_name_without_a_colon_is_read(self):
        source = '<pre class="schema-example">\nauthentication\n    multifactor: string\n</pre>\n'
        self.assertEqual(mr.model_fields(source), [("authentication", "multifactor", "string")])

    def test_a_line_that_cannot_be_read_is_an_error(self):
        with self.assertRaises(mr.SourceError):
            mr.model_fields('<pre class="schema-example">\nclaims:\n     given_name string\n</pre>\n')


class HandWrittenDictionary(unittest.TestCase):
    def problems(self, text: str) -> list[str]:
        return mr.dictionary_problems(rows(text), mr.model_fields(MODEL))

    def test_a_file_that_matches_the_data_model_passes(self):
        self.assertEqual(self.problems(DICTIONARY), [])

    def test_an_element_missing_from_the_file(self):
        self.assertEqual(self.problems(DICTIONARY.replace("evidence,document,object,A document,03-data-model.md\n", "")),
                         ["evidence.document is in the data model but not in the file"])

    def test_an_element_that_is_not_in_the_data_model(self):
        extra = DICTIONARY + "evidence,vouch,object,A vouch,03-data-model.md\n"
        self.assertEqual(self.problems(extra), ["evidence.vouch is in the file but not in the data model"])

    def test_a_different_type(self):
        changed = DICTIONARY.replace("evidence,array,", "evidence,object,")
        self.assertEqual(self.problems(changed),
                         ["verification.evidence has type 'object'; the data model says 'array (evidence)'"])

    def test_a_name_that_differs_only_in_case(self):
        self.assertTrue(self.problems(DICTIONARY.replace("trust_framework", "Trust_framework")))

    def test_rows_in_a_different_order(self):
        lines = DICTIONARY.splitlines(keepends=True)
        reordered = "".join([lines[0], lines[2], lines[1], *lines[3:]])
        self.assertEqual(self.problems(reordered), ["the rows are not in the same order as the data model"])


class Yaml(unittest.TestCase):
    def test_values_that_yaml_would_change_are_quoted(self):
        self.assertEqual(mr.yaml_scalar("given_name"), "given_name")
        self.assertEqual(mr.yaml_scalar("03-data-model.md"), "03-data-model.md")
        self.assertEqual(mr.yaml_scalar("'uk_dvstf'"), "\"'uk_dvstf'\"")
        for risky in ("no", "true", "null", "123", "1e3", "0x1f"):
            self.assertEqual(mr.yaml_scalar(risky), f'"{risky}"')

    @unittest.skipIf(yaml is None, "PyYAML is not installed")
    def test_the_yaml_reads_back_as_the_rows_of_the_csv(self):
        loaded = yaml.safe_load(mr.to_yaml(rows()))
        flat = [
            {"element": element["element"], "sub_element": sub["name"], "type": sub["type"],
             "description": sub["description"], "source": sub["source"]}
            for element in loaded for sub in element["sub_elements"]
        ]
        self.assertEqual(flat, rows())


class CommandLine(unittest.TestCase):
    """Run the tool as a script against a temporary repository layout."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        for guide in mr.GUIDES:
            schema = self.root / mr.SCHEMA / guide
            schema.mkdir(parents=True)
            (schema / "03-data-model.md").write_text(MODEL, encoding="utf-8")
            (schema / "05-predefined-values.md").write_text(VALUES, encoding="utf-8")
            (schema / "06-predefined-lists.md").write_text(LISTS, encoding="utf-8")
            output = self.root / mr.OUTPUT / guide
            output.mkdir(parents=True)
            (output / "data-dictionary.csv").write_text(DICTIONARY, encoding="utf-8", newline="")

    def run_tool(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOLS / "machine_readable.py"), "--root", str(self.root), *args],
            capture_output=True, text=True, encoding="utf-8",
        )

    def output(self, name: str) -> Path:
        return self.root / mr.OUTPUT / "gpg-45" / name

    def test_missing_files_are_reported_then_written_then_pass(self):
        self.assertEqual(self.run_tool("--check").returncode, 1)
        self.assertFalse(self.output("predefined-values.csv").exists(), "--check must not write files")
        self.assertEqual(self.run_tool("--write").returncode, 0)
        self.assertEqual(self.run_tool("--check").returncode, 0)

    def test_a_file_that_no_longer_matches_the_schema_text_is_reported(self):
        self.run_tool("--write")
        schema = self.root / mr.SCHEMA / "gpg-45" / "05-predefined-values.md"
        schema.write_text(VALUES.replace("(such as face)", "(such as voice)"), encoding="utf-8")
        proc = self.run_tool("--check")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("gpg-45/predefined-values.csv", proc.stdout)
        self.assertNotIn("gpg-44/predefined-values.csv", proc.stdout)

    def test_written_files_hold_the_published_cells(self):
        self.run_tool("--write")
        with self.output("predefined-lists.csv").open(encoding="utf-8", newline="") as handle:
            self.assertEqual(list(csv.reader(handle))[2], ["document_type", "string", "bus_pass,education_certificate", ""])

    def test_writing_does_not_hide_a_problem_in_the_hand_written_file(self):
        self.output("data-dictionary.csv").write_text(
            DICTIONARY.replace("evidence,array,", "evidence,object,"), encoding="utf-8", newline="")
        proc = self.run_tool("--write")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("verification.evidence has type 'object'", proc.stdout)

    def test_a_section_file_with_two_tables_is_an_error(self):
        schema = self.root / mr.SCHEMA / "gpg-44" / "06-predefined-lists.md"
        schema.write_text(LISTS + "\nText.\n\n" + VALUES.split("\n\n", 1)[1], encoding="utf-8")
        self.assertEqual(self.run_tool("--check").returncode, 2)


if __name__ == "__main__":
    unittest.main()

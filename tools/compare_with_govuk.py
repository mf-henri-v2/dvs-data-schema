#!/usr/bin/env python3
"""Compare the schema text in this repository with the publication on GOV.UK.

GOV.UK publishes each guide (GPG 45 and GPG 44) as one page. This repository
holds the same text as six Markdown files per guide. This tool reads both,
reduces each to the text a reader sees, and reports every difference:

- headings, paragraphs and list items, in order;
- each line of each data model example, including its indentation;
- each table: its column headings, every cell, and which cells are row
  headings;
- each link: its text and where it goes;
- each heading's level, relative to the first heading of its file;
- each heading's ID, which links to that heading depend on.

Only the following are treated as the same on both sides, because they are
how the two systems present the same text rather than differences in it:

- GOV.UK shows typographic quotation marks (‘ ’ “ ”) where the Markdown has
  straight ones (' ");
- GOV.UK indents example lines with non-breaking spaces, and the Markdown
  uses ordinary spaces. The number of spaces is compared;
- runs of spaces and line breaks inside a paragraph, list item or table cell
  count as one space;
- a link to another part of the same GOV.UK page (#date) is a link to the
  file that now holds that part (04-data-dictionary.md#date).

The caution banner and the "Repository navigation" footer are repository
material and are removed before comparing. Nothing else is removed.

Usage:
    python tools/compare_with_govuk.py                  fetch GOV.UK and compare
    python tools/compare_with_govuk.py --save-html DIR  also keep what was fetched
    python tools/compare_with_govuk.py --html-dir DIR   compare with copies saved earlier

Exit status: 0 if the text matches, 1 if it differs, 2 if GOV.UK or a file
could not be read.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = "schema-1.0"
PUBLICATION = "/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0"
CONTENT_API = "https://www.gov.uk/api/content"

SECTION_FILES = (
    "01-introduction.md",
    "02-data-taxonomy.md",
    "03-data-model.md",
    "04-data-dictionary.md",
    "05-predefined-values.md",
    "06-predefined-lists.md",
)
GUIDES = {
    "gpg-45": f"{PUBLICATION}/data-taxonomy-data-model-and-data-dictionary-for-gpg-45",
    "gpg-44": f"{PUBLICATION}/data-taxonomy-data-model-and-data-dictionary-for-gpg-44",
}

BANNER = re.compile(r"\A<!-- caution-banner:start[^\n]*-->\n(?:>[^\n]*\n)+<!-- caution-banner:end -->\n")
FOOTER = re.compile(r"\n---\n+\*\*Repository navigation\*\*\n[\s\S]*\Z")

QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})
NBSP = " "
VOID_TAGS = {"br", "hr", "img", "input", "meta", "link"}
ROW_HEADING = " [row heading]"


@dataclass
class Guide:
    """One guide reduced to what a reader sees."""

    records: list[tuple[str, str]] = field(default_factory=list)
    links: list[tuple[str, str]] = field(default_factory=list)
    # (heading text, level)
    headings: list[tuple[str, int]] = field(default_factory=list)
    # The ID of each heading, which is what a link to that heading uses.
    heading_ids: list[str] = field(default_factory=list)


def clean(text: str) -> str:
    """Visible text: typographic quotes straightened, whitespace collapsed."""
    return re.sub(r"\s+", " ", text.replace(NBSP, " ").translate(QUOTES)).strip()


def example_line(text: str) -> str:
    """An example line as '<indent>|<text>', counting non-breaking and ordinary spaces alike."""
    text = text.replace(NBSP, " ").translate(QUOTES).strip("\r\n\t").rstrip()
    body = text.lstrip(" ")
    return f"{len(text) - len(body)}|{re.sub(r' +', ' ', body)}"


# --- GOV.UK ----------------------------------------------------------------


class Node:
    def __init__(self, tag: str, attrs: dict[str, str]) -> None:
        self.tag, self.attrs, self.children = tag, attrs, []

    def text(self) -> str:
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def find_all(self, *tags: str) -> list["Node"]:
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if child.tag in tags:
                    found.append(child)
                found.extend(child.find_all(*tags))
        return found


class TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: v or "" for k, v in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_govuk(html: str) -> Guide:
    builder = TreeBuilder()
    builder.feed(html)
    body = next((n for n in builder.root.find_all("div") if "govspeak" in n.attrs.get("class", "").split()), None)
    if body is None:
        raise ValueError("no <div class=\"govspeak\"> found in the GOV.UK page body")
    guide = Guide()

    def links_in(node: Node) -> None:
        for a in node.find_all("a"):
            if a.attrs.get("href"):
                guide.links.append((clean(a.text()), a.attrs["href"]))

    for node in body.children:
        if isinstance(node, str):
            if node.strip():
                guide.records.append(("text outside any element", clean(node)))
            continue
        classes = node.attrs.get("class", "").split()
        if re.fullmatch(r"h[1-6]", node.tag):
            guide.records.append(("heading", clean(node.text())))
            guide.headings.append((clean(node.text()), int(node.tag[1])))
            guide.heading_ids.append(node.attrs.get("id", ""))
        elif node.tag == "p":
            guide.records.append(("paragraph", clean(node.text())))
        elif node.tag in ("ul", "ol"):
            for item in (c for c in node.children if isinstance(c, Node) and c.tag == "li"):
                guide.records.append(("list item", clean(item.text())))
        elif node.tag == "div" and "example" in classes:
            guide.records.append(("example", "start"))
            for p in (c for c in node.children if isinstance(c, Node)):
                line: list[str] = []
                for child in [*p.children, Node("br", {})]:
                    if isinstance(child, Node) and child.tag == "br":
                        guide.records.append(("example line", example_line("".join(line))))
                        line = []
                    else:
                        line.append(child if isinstance(child, str) else child.text())
            guide.records.append(("example", "end"))
        elif node.tag == "table":
            for row in node.find_all("tr"):
                cells = [c for c in row.children if isinstance(c, Node) and c.tag in ("th", "td")]
                if all(c.tag == "th" and c.attrs.get("scope") == "col" for c in cells):
                    guide.records.append(("table column headings", " | ".join(clean(c.text()) for c in cells)))
                else:
                    guide.records.append(("table row", " | ".join(
                        clean(c.text()) + (ROW_HEADING if c.tag == "th" else "") for c in cells)))
            guide.records.append(("table", "end"))
        else:
            guide.records.append((f"unexpected <{node.tag}> element", clean(node.text())))
        links_in(node)
    return guide


# --- Repository Markdown ---------------------------------------------------

MD_LINK = re.compile(r"\[([^\]]*)\]\(\s*<?([^)\s>]+)>?\s*\)")
HTML_LINK = re.compile(r'<a\s+href="([^"]*)"\s*>(.*?)</a>')
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
CELL_SPLIT = re.compile(r"(?<!\\)\|")
DELIMITER_ROW = re.compile(r"^\|(\s*:?-+:?\s*\|)+$")
WHOLLY_BOLD = re.compile(r"^\*\*(.+)\*\*$")
ANCHOR_ONLY = re.compile(r'^(<a\s+id="[^"]+"\s*></a>\s*)+$')


def strip_furniture(source: str, name: str) -> str:
    """Remove the caution banner and the repository navigation footer, and nothing else."""
    text, banners = BANNER.subn("", source)
    text, footers = FOOTER.subn("\n", text)
    if banners != 1 or footers != 1:
        raise ValueError(
            f"{name}: expected one caution banner and one 'Repository navigation' footer, "
            f"found {banners} and {footers}")
    return text


def parse_markdown(files: list[tuple[str, str]]) -> Guide:
    """Read a guide from (file name, Markdown source) pairs, in reading order."""
    guide = Guide()

    def inline(text: str, source_file: str) -> str:
        def link(match: re.Match) -> str:
            guide.links.append((clean(match.group(1)), same_page(match.group(2), source_file)))
            return match.group(1)
        return MD_LINK.sub(link, text)

    for name, source in files:
        lines = strip_furniture(source, name).split("\n")
        paragraph: list[str] = []

        def flush() -> None:
            if paragraph:
                guide.records.append(("paragraph", clean(inline(" ".join(paragraph), name))))
                paragraph.clear()

        i = 0
        while i < len(lines):
            line = lines[i]
            heading = HEADING.match(line)
            if not line.strip() or ANCHOR_ONLY.match(line.strip()):
                flush()
            elif line.startswith('<pre class="schema-example">'):
                flush()
                guide.records.append(("example", "start"))
                i += 1
                while i < len(lines) and lines[i].strip() != "</pre>":
                    def anchor(match: re.Match) -> str:
                        guide.links.append((clean(match.group(2)), same_page(match.group(1), name)))
                        return match.group(2)
                    guide.records.append(("example line", example_line(HTML_LINK.sub(anchor, lines[i]))))
                    i += 1
                guide.records.append(("example", "end"))
            elif heading:
                flush()
                text = clean(inline(heading.group(2), name))
                guide.records.append(("heading", text))
                guide.headings.append((text, len(heading.group(1))))
                guide.heading_ids.append(github_slug(heading.group(2)))
            elif line.startswith("- "):
                flush()
                guide.records.append(("list item", clean(inline(line[2:], name))))
            elif line.startswith("|"):
                flush()
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    rows.append(lines[i].strip())
                    i += 1
                i -= 1
                if len(rows) < 2 or not DELIMITER_ROW.match(rows[1]):
                    guide.records.append(("malformed table", clean(" ".join(rows))))
                else:
                    for n, row in enumerate(r for k, r in enumerate(rows) if k != 1):
                        cells = [c.strip().replace("\\|", "|") for c in CELL_SPLIT.split(row.strip())[1:-1]]
                        if n == 0:
                            guide.records.append(("table column headings", " | ".join(clean(inline(c, name)) for c in cells)))
                            continue
                        shown = []
                        for k, cell in enumerate(cells):
                            bold = WHOLLY_BOLD.match(cell) if k == 0 else None
                            shown.append(clean(inline(bold.group(1) if bold else cell, name)) + (ROW_HEADING if bold else ""))
                        guide.records.append(("table row", " | ".join(shown)))
                    guide.records.append(("table", "end"))
            else:
                paragraph.append(line)
            i += 1
        flush()
    return guide


def github_slug(heading: str) -> str:
    """The ID GitHub gives a heading: lower case, punctuation removed, spaces as hyphens."""
    text = re.sub(r"<[^>]+>", "", heading)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return text.replace(" ", "-")


def same_page(target: str, source_file: str) -> str:
    """A link between this guide's section files, written as GOV.UK writes it: #fragment."""
    path, _, fragment = target.partition("#")
    if fragment and (path in SECTION_FILES or (path == "" and source_file in SECTION_FILES)):
        return f"#{fragment}"
    return target


# --- Comparison ------------------------------------------------------------


def relative_levels(headings: list[tuple[str, int]], starts: set[int]) -> list[tuple[str, int]]:
    """Each heading's level relative to the first heading of its file (or the matching GOV.UK heading)."""
    out, base = [], None
    for n, (text, level) in enumerate(headings):
        if n in starts or base is None:
            base = level
        out.append((text, level - base))
    return out


def compare(govuk: Guide, repo: Guide, file_starts: set[int]) -> list[str]:
    """Differences between GOV.UK and the repository, as lines to print."""
    problems: list[str] = []

    def diff(title: str, published: list[str], here: list[str]) -> None:
        matcher = difflib.SequenceMatcher(a=published, b=here, autojunk=False)
        for op, a0, a1, b0, b1 in matcher.get_opcodes():
            if op == "equal":
                continue
            problems.append(f"  {title}:")
            problems.extend(f"    GOV.UK:     {line}" for line in published[a0:a1] or ["(nothing)"])
            problems.extend(f"    repository: {line}" for line in here[b0:b1] or ["(nothing)"])

    diff("text", [f"{kind}: {value}" for kind, value in govuk.records],
         [f"{kind}: {value}" for kind, value in repo.records])
    diff("link", [f"[{text}] -> {href}" for text, href in govuk.links],
         [f"[{text}] -> {href}" for text, href in repo.links])
    if [t for t, _ in govuk.headings] == [t for t, _ in repo.headings]:
        diff("heading ID, used by links to the heading", govuk.heading_ids, repo.heading_ids)
        diff("heading level below the first heading of its file",
             [f"{text}: +{level}" for text, level in relative_levels(govuk.headings, file_starts)],
             [f"{text}: +{level}" for text, level in relative_levels(repo.headings, file_starts)])
    return problems


def fetch(path: str) -> str:
    request = urllib.request.Request(f"{CONTENT_API}{path}", headers={"User-Agent": "dvs-data-schema-compare"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["details"]["body"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare the schema text with the publication on GOV.UK.")
    parser.add_argument("--html-dir", type=Path, help="use gpg-45.html and gpg-44.html saved in this folder")
    parser.add_argument("--save-html", type=Path, metavar="DIR", help="save the fetched GOV.UK text in this folder")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, metavar="DIR",
                        help="read the section files from this copy of the repository, such as a checked-out tag")
    args = parser.parse_args(argv)

    failed = False
    for guide_name, path in GUIDES.items():
        try:
            if args.html_dir:
                html = (args.html_dir / f"{guide_name}.html").read_text(encoding="utf-8")
            else:
                html = fetch(path)
                if args.save_html:
                    args.save_html.mkdir(parents=True, exist_ok=True)
                    (args.save_html / f"{guide_name}.html").write_text(html, encoding="utf-8", newline="\n")
            files = [
                (name, (args.root / SCHEMA_DIR / guide_name / name).read_text(encoding="utf-8"))
                for name in SECTION_FILES
            ]
            govuk, repo = parse_govuk(html), parse_markdown(files)
        except (OSError, ValueError, KeyError, urllib.error.URLError) as err:
            print(f"ERROR: {guide_name}: {err}")
            return 2

        # Where each file starts in the list of headings, to compare heading levels file by file.
        starts, count = set(), 0
        for name, source in files:
            starts.add(count)
            count += len(parse_markdown([(name, source)]).headings)

        problems = compare(govuk, repo, starts)
        examples = sum(1 for r in govuk.records if r == ("example", "start"))
        tables = sum(1 for r in govuk.records if r == ("table", "end"))
        summary = (f"{guide_name}: {len(govuk.records)} published text items, including {examples} examples "
                   f"and {tables} tables, and {len(govuk.links)} links")
        if problems:
            failed = True
            print(f"{summary}: DIFFERENCES FOUND")
            print("\n".join(problems))
        else:
            print(f"{summary}: the repository matches GOV.UK.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())

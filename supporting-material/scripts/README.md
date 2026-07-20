> [!CAUTION]
> This repository is a workspace copy for navigation, drafting, version control and collaboration. It is not the official statement of the UK digital verification services trust framework and must not be relied on as such. For the official published DVS trust framework, see the GOV.UK publication.

# Scripts

Python scripts that regenerate derived artefacts under `supporting-material/`.
Each script states what it reads and what it writes; all are deterministic
(running them twice on unchanged input produces byte-identical output).

## Available scripts

- [`apply_cross_file_links.py`](apply_cross_file_links.py) — rewrites bare
  `#anchor` links inside `schema-1.0/gpg-45/` and `schema-1.0/gpg-44/`
  Markdown files to `target.md#anchor` form when the anchor's definition
  now lives in a different file. Idempotent: a second run is a no-op.
  Applied during the KI-4 cleanup.
- [`convert_schema_examples.py`](convert_schema_examples.py) — converts
  GOV.UK publishing `$E ... $E` fenced blocks inside the schema text to
  HTML `<pre class="schema-example">` elements. Inside each block,
  `&nbsp;` entities become regular spaces, Markdown links become HTML
  `<a>` elements, and blank-line export artefacts are collapsed.
  Idempotent: after the first run there are no `$E` markers left, so a
  second run finds nothing to convert. Applied during the KI-1 cleanup.
- [`regenerate_machine_readable.py`](regenerate_machine_readable.py) —
  regenerates the CSV, YAML, dot-path and nested-tree views under
  `machine-readable/gpg-45/` and `machine-readable/gpg-44/`. At launch this
  script contains the deterministic source-of-truth for the derived data —
  future versions will parse the published Markdown directly.
- [`validate_caution_block.py`](validate_caution_block.py) — the same check
  that CI runs, wrapped as a local script for quick pre-push verification.
- [`update_caution_block.py`](update_caution_block.py) - sets or refreshes the standard caution block at the top of every workspace Markdown file in one pass. Skips the same tooling paths as the CI check (`.github/`, `docs-site/README.md`, `docs-site/node_modules/`, `TEMPLATE-USAGE.md`). Edit `CAUTION_TEXT` in the script to change the wording repo-wide. Idempotent: a second run on unchanged input is a no-op. Where `validate_caution_block.py` reports drift, this script fixes it.

## Running

```bash
python3 supporting-material/scripts/apply_cross_file_links.py
python3 supporting-material/scripts/convert_schema_examples.py
python3 supporting-material/scripts/regenerate_machine_readable.py
python3 supporting-material/scripts/update_caution_block.py
python3 supporting-material/scripts/validate_caution_block.py
```

## Adding new scripts

- Prefer the Python standard library. If a third-party package is essential,
  add a `requirements.txt` in this folder and document the minimum Python
  version.
- Every script must print what it writes and must be safe to run from any
  working directory (use `Path(__file__).resolve()` rather than relative
  paths from `.`).
- Every script must be idempotent.

## Back

- [Supporting material](../README.md)
- [Repository home](../../README.md)

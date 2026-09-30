<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# Data files

Parts of the data schema as files you can open in a spreadsheet or read with software.

These files are not part of the published data schema. If a file differs from the [data schema](../../schema-1.0/README.md), the data schema is right.

- [Data files for GPG 45](gpg-45/README.md)
- [Data files for GPG 44](gpg-44/README.md)

## What each file is

Each guide has the same 6 files.

| File | What it holds | How it is kept up to date |
| --- | --- | --- |
| `predefined-values.csv` | The predefined values table, cell for cell | Written by a tool from the data schema |
| `predefined-lists.csv` | The predefined lists table, cell for cell | Written by a tool from the data schema |
| `data-dictionary.csv` | Every element in the data model, with its sub-elements, their types and a short description | Written by hand. A tool checks that the elements and types match the data model. The descriptions are summaries, not the published wording |
| `data-dictionary.yaml` | The same rows as `data-dictionary.csv`, grouped by element | Written by a tool from `data-dictionary.csv` |
| `dot-path-view.md` | Every element as a path, such as `verified_claims.claims.given_name` | Written by hand |
| `nested-tree-view.md` | Every element, indented to show which element contains which | Written by hand |

The CSV files use commas and UTF-8, and their first line holds the column headings. In the 2 files copied from the data schema, the column headings are the ones in the published tables.

## Keeping the files up to date

After a change to the data schema, run this from the repository folder:

```sh
python tools/machine_readable.py --write
```

This rewrites the 3 files the tool writes for each guide. It also reports any element in the data model that is missing from `data-dictionary.csv` or has a different type there. Fix those by hand, along with the path and tree views, which no tool checks.

The same check runs on every pull request. [How this repository works](../../ARCHITECTURE.md#data-files) has more detail.

## Back

- [Supporting material](../README.md)
- [Repository home](../../README.md)

<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# Data files for GPG 44

Parts of the [GPG 44 data schema](../../../schema-1.0/gpg-44/README.md) as files you can open in a spreadsheet or read with software. [Data files](../README.md) explains how each one is kept up to date.

These files are not part of the published data schema. If a file differs from the data schema, the data schema is right.

| File | What it holds |
| --- | --- |
| [`predefined-values.csv`](predefined-values.csv) | The table in [Predefined values](../../../schema-1.0/gpg-44/05-predefined-values.md), cell for cell |
| [`predefined-lists.csv`](predefined-lists.csv) | The table in [Predefined lists](../../../schema-1.0/gpg-44/06-predefined-lists.md), cell for cell |
| [`data-dictionary.csv`](data-dictionary.csv) | Every element in the [data model](../../../schema-1.0/gpg-44/03-data-model.md), with its sub-elements, their types and a short description. The descriptions are summaries, not the published wording |
| [`data-dictionary.yaml`](data-dictionary.yaml) | The same rows as `data-dictionary.csv`, grouped by element |
| [Dot-path view](dot-path-view.md) | Every element as a path from `authentication` |
| [Nested tree view](nested-tree-view.md) | Every element, indented to show which element contains which |

## Back

- [Data files](../README.md)
- [Supporting material](../../README.md)
- [Repository home](../../../README.md)

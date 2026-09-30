<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# Presentation experiments

An experiment in showing parts of the data model as tables, with each type cell coloured by the kind of type it is.

These pages are not part of the published data schema. They were written by hand and cover only some elements. If a page differs from the data model, the data model is right. The descriptions in the tables are summaries, not the published wording.

- [GPG 45: colour-coded data model](gpg-45-colour-coded-model.md)
- [GPG 44: colour-coded data model](gpg-44-colour-coded-model.md)

## The colours

| Colour | Kind of type |
| --- | --- |
| Light yellow | Primitive, such as `string`, `number`, `date` or `timestamp` |
| Light blue | Reference to another element of the data model |
| Light green | Array |
| Light grey | Fixed value, such as 'uk_dvstf' |
| Light orange | Limited to a predefined list |

Colour is never the only way the kind of type is shown. Each table has a "Kind of type" column that says it in words.

The colours show on the reading website. GitHub removes colours from Markdown pages, so on GitHub the tables are plain and the "Kind of type" column carries the information.

## Back

- [Supporting material](../README.md)
- [Repository home](../../README.md)

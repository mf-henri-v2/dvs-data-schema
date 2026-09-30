<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# Versions and published baselines

This repository holds OfDIA's working draft of the UK digital verification services trust framework data schema. Git tags record each version exactly as it was formally published, so you can always see what has changed since publication.

## How it works

- **The `main` branch is the working draft.** It holds the text OfDIA has accepted through review. It can include changes that have not been published yet.
- **A `published-X.Y` tag marks each formally published version.** A tag points at the version of the files that matched that publication, and never moves.
- **GOV.UK is authoritative for the published version.** A change accepted into the working draft takes effect only when OfDIA publishes a new version on GOV.UK.

The working draft is expected to differ from the latest published version once changes have been accepted. That difference is what the comparison below shows.

## Published versions

| Tag | Published on GOV.UK | Notes |
| --- | --- | --- |
| [`published-1.0`](https://github.com/mf-henri-v2/dvs-data-schema/tree/published-1.0) | 3 March 2026, last corrected 13 April 2026 | [Data schema 1.0](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0), published alongside the pre-release of trust framework 1.0. The tag matches the text as corrected on 13 April 2026. |

GOV.UK has corrected data schema 1.0 twice without changing its version number:

- 6 March 2026: links were fixed and added, and formatting problems were corrected.
- 13 April 2026: in the GPG 45 data model, one element of `attachment` that was shown as `content_type` was corrected to `content_format`.

## Compare the working draft with a published version

- On GitHub: [compare `published-1.0` with the working draft](https://github.com/mf-henri-v2/dvs-data-schema/compare/published-1.0...main). This shows every change since publication, file by file. It includes changes to the repository's own tools and documentation as well as changes to the data schema.
- To see only changes to the data schema, in a local copy of the repository:

  ```sh
  git fetch --tags
  git diff published-1.0 main -- schema-1.0/
  ```

## Where the text lives

The data schema is in [`schema-1.0/`](schema-1.0/README.md). Each of the 2 guides has its own folder, with one file per section. The folder name records the version the working draft started from. Whether to rename it is decided when a new version is published.

## When a new version is published

1. Through a reviewed pull request, make sure `main` holds exactly the text published on GOV.UK. [How this repository works](ARCHITECTURE.md#compare-the-text-with-govuk) explains how to check this.
2. A maintainer tags that commit `published-X.Y` with an annotated tag, and adds a row to the table above.
3. If the banner needs to point to the new publication, update [`tools/caution-banner.md`](tools/caution-banner.md) and apply it. [How this repository works](ARCHITECTURE.md#caution-banner) explains how.
4. Optionally, create a GitHub release from the tag so the published version is easy to find.

## How the text was first added

The text was added on 1 June 2026 from data schema 1.0 on GOV.UK, as corrected on 13 April 2026. GOV.UK publishes each guide as one page. Here each guide is split into 6 files, one per section.

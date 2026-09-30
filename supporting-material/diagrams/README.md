<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# Diagrams

3 diagrams of how the main data elements fit together. Each diagram is described in words below, so you do not need to see the diagram to use this page.

The diagrams are not part of the published data schema. They were drawn by hand from the data model and show only some of its elements. If a diagram differs from the data model, the data model is right.

Each diagram is a text file in [Mermaid](https://mermaid.js.org/) format. GitHub shows the file as a diagram when you open it.

## GPG 45: main elements

Diagram file: [`gpg-45-top-level-containment.mmd`](gpg-45-top-level-containment.mmd). Drawn from the [GPG 45 data model](../../schema-1.0/gpg-45/03-data-model.md).

The diagram shows which elements contain which:

- `verified_claims` contains:
  - `claims`
  - `verification`, which contains:
    - `trust_framework`, which is always 'uk_dvstf'
    - `dvs_registration`
    - `evidence`, which contains:
      - `document`
      - `electronic_record`
      - `vouch`
    - `assurance_level`
    - `assurance_process`, which contains:
      - `policy`, which is always 'gpg45'
      - `procedure`
      - `assurance_details`

## GPG 45: evidence

Diagram file: [`gpg-45-evidence-structure.mmd`](gpg-45-evidence-structure.mmd). Drawn from the [GPG 45 data model](../../schema-1.0/gpg-45/03-data-model.md).

The diagram shows the 3 kinds of evidence and what each contains:

- `evidence` contains:
  - `document`, which contains:
    - `document_details`, which contains `issuer`, an `authority`
    - `attachments`
    - `check_details`
  - `electronic_record`, which contains:
    - `record`, which contains `source`, an `authority`
    - `attachments`
    - `check_details`
  - `vouch`, which contains:
    - `attestation`, which contains `voucher`
    - `attachments`
    - `check_details`

## GPG 44: authentication

Diagram file: [`gpg-44-authentication-structure.mmd`](gpg-44-authentication-structure.mmd). Drawn from the [GPG 44 data model](../../schema-1.0/gpg-44/03-data-model.md).

The diagram shows which elements contain which:

- `authentication` contains:
  - `authenticator_protection`
  - `multifactor`
  - `monitoring`
  - `authenticators`, an array in which each `authenticator` contains:
    - `authenticator_type`
    - `authenticator_quality`

## Changing a diagram

Edit the `.mmd` file and the description on this page together, so that they say the same thing.

## Back

- [Supporting material](../README.md)
- [Repository home](../../README.md)

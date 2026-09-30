<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# Mappings

Draft notes that compare the GPG 45 data schema with other identity standards.

These files are a starting point for discussion. They are not part of the published data schema. They have not been checked line by line against the standards they refer to, and they do not claim that the data schema conforms to, or works with, any of those standards. Check each entry against the standard itself before you rely on it.

## Files

| File | What it compares | Status |
| --- | --- | --- |
| [`oid4ida-mapping.yaml`](oid4ida-mapping.yaml) | Elements of the GPG 45 data model with the [OpenID Identity Assurance Schema Definition 1.0](https://openid.net/specs/openid-ida-verified-claims-1_0-final.html) | Draft, 64 entries |
| [`oidc-core-mapping.yaml`](oidc-core-mapping.yaml) | The elements under `verified_claims.claims` with the standard claims in [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) | Draft, 14 entries |
| [`w3c-vc-notes.md`](w3c-vc-notes.md) | How a `verified_claims` object could be carried inside a [W3C Verifiable Credential](https://www.w3.org/TR/vc-data-model-2.0/) | Discussion notes, not an element-by-element comparison |

The YAML files record the date their author last looked at each standard, as `date_referenced`. The standards may have changed since.

## How the YAML files are laid out

Each file has:

- `standard`: the name and address of the standard it compares with
- `mappings`: a list of entries. Each entry gives an element of the data schema as a path (`dvs`), the matching element in the other standard (`target`), a `kind`, and notes

| Kind | Meaning |
| --- | --- |
| `exact` | Same name, structure and meaning |
| `renamed` | Different name, same meaning |
| `restructured` | Same meaning, arranged differently |
| `dvs_only` | In the data schema, with nothing matching in the other standard |
| `target_only` | In the other standard, with nothing matching in the data schema |

The entries were written by hand. When the data schema or a standard changes, they need updating by hand.

## Suggest a change to the data schema

A mapping can point out a difference. It cannot change the data schema. To suggest a change, [open a new issue](https://github.com/mf-henri-v2/dvs-data-schema/issues/new/choose) and choose "Schema feedback".

## Back

- [Supporting material](../README.md)
- [Repository home](../../README.md)

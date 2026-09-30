<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# GPG 44: dot-path view

Every element of the GPG 44 data model, written as a path from `authentication` with a dot between each level. `[]` marks an array.

You can use a path to say exactly which element you mean, for example when you [give feedback](../../../CONTRIBUTING.md).

This view was written by hand from the [GPG 44 data model](../../../schema-1.0/gpg-44/03-data-model.md). It is not part of the published data schema. If it differs from the data model, the data model is right.

```text
authentication
authentication.authenticator_protection
authentication.multifactor
authentication.monitoring
authentication.authenticators[]
authentication.authenticators[].authenticator_type
authentication.authenticators[].authenticator_quality
```

## Back

- [Data files for GPG 44](README.md)
- [Supporting material](../../README.md)
- [Repository home](../../../README.md)

<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

> Derived, non-authoritative, for implementation support only.  
> Authoritative definition: the publication text under `schema-1.0/`.

# GPG 44 — nested tree view

Same content as the [dot-path view](dot-path-view.md), rendered as an indented tree.

```text
authentication
    authenticator_protection
    multifactor
    monitoring
    authenticators[]
        authenticator_type
        authenticator_quality
```

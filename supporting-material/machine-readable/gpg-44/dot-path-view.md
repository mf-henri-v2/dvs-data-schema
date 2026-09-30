<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

> Derived, non-authoritative, for implementation support only.  
> Authoritative definition: the publication text under `schema-1.0/`.

# GPG 44 — dot-path view

Every field of the GPG 44 data model as a dot-separated path.

```text
authentication
authentication.authenticator_protection
authentication.multifactor
authentication.monitoring
authentication.authenticators[]
authentication.authenticators[].authenticator_type
authentication.authenticators[].authenticator_quality
```

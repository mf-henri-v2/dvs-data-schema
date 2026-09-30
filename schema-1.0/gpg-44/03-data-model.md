<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

## Data model

The data model provides a description of the data element name, the relevant sub-elements and the data type.

### Overview

This nested view shows the relationship between elements and their sub‑elements.

<pre class="schema-example">
authentication
    authenticator_protection: string
    multifactor: string
    monitoring: string
    authenticators: array (authenticator)
</pre>

An authenticator is defined as:

<pre class="schema-example">
authenticator
    authenticator_type: string
    authenticator_quality: string
</pre>

---

**Repository navigation**

[← Previous: 2. Data taxonomy](02-data-taxonomy.md) · [GPG 44 contents](README.md) · [Schema contents](../README.md) · [Repository home](../../README.md) · [Next: 4. Data dictionary →](04-data-dictionary.md)

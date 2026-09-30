<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# GPG 44: colour-coded data model (experiment)

This page is an experiment in presentation. It shows the 2 elements of the GPG 44 data model as tables, with each type cell coloured by the kind of type it is. The "Kind of type" column says the same thing in words.

It is not part of the published data schema, and it was written by hand. If it differs from the [GPG 44 data model](../../schema-1.0/gpg-44/03-data-model.md), the data model is right. The descriptions are summaries, not the published wording.

The colours show on the reading website. GitHub removes them, so on GitHub use the "Kind of type" column.

## Legend

<table>
  <thead>
    <tr><th>Colour</th><th>Kind of type</th><th>Example</th></tr>
  </thead>
  <tbody>
    <tr>
      <td style="background-color:#fff9e6">Light yellow</td>
      <td>Primitive</td>
      <td><code>string</code>, <code>number</code>, <code>date</code>, <code>timestamp</code></td>
    </tr>
    <tr>
      <td style="background-color:#e6f2ff">Light blue</td>
      <td>Reference to another object</td>
      <td>none in GPG 44</td>
    </tr>
    <tr>
      <td style="background-color:#e6ffe6">Light green</td>
      <td>Array</td>
      <td><code>array (authenticator)</code></td>
    </tr>
    <tr>
      <td style="background-color:#f0f0f0">Light grey</td>
      <td>Fixed literal value</td>
      <td>none in GPG 44</td>
    </tr>
    <tr>
      <td style="background-color:#ffeecc">Light orange</td>
      <td>Restricted to a predefined list</td>
      <td><code>authenticator_type</code>, <code>authenticator_quality</code>, <code>authenticator_protection</code></td>
    </tr>
  </tbody>
</table>

## `authentication`

The top-level object. One element limited to a predefined list, two strings and one array.

<table>
  <thead>
    <tr><th>Field</th><th>Type</th><th>Kind of type</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><code>authenticator_protection</code></td>
      <td style="background-color:#ffeecc"><code>string</code> (<a href="../../schema-1.0/gpg-44/06-predefined-lists.md">authenticator_protection</a>)</td>
      <td>Predefined list</td>
      <td>Level of protection achieved according to GPG 44.</td>
    </tr>
    <tr>
      <td><code>multifactor</code></td>
      <td style="background-color:#fff9e6"><code>string</code></td>
      <td>Primitive</td>
      <td>The number of factors used in the authentication.</td>
    </tr>
    <tr>
      <td><code>monitoring</code></td>
      <td style="background-color:#fff9e6"><code>string</code></td>
      <td>Primitive</td>
      <td>Whether monitoring is being performed.</td>
    </tr>
    <tr>
      <td><code>authenticators</code></td>
      <td style="background-color:#e6ffe6"><code>array</code> (<code>authenticator</code>)</td>
      <td>Array</td>
      <td>Array of authenticator objects.</td>
    </tr>
  </tbody>
</table>

## `authenticator`

Each item in the `authenticators` array. Both elements are limited to a predefined list.

<table>
  <thead>
    <tr><th>Field</th><th>Type</th><th>Kind of type</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><code>authenticator_type</code></td>
      <td style="background-color:#ffeecc"><code>string</code> (<a href="../../schema-1.0/gpg-44/06-predefined-lists.md">authenticator_type</a>)</td>
      <td>Predefined list</td>
      <td>The type of authenticator according to GPG 44.</td>
    </tr>
    <tr>
      <td><code>authenticator_quality</code></td>
      <td style="background-color:#ffeecc"><code>string</code> (<a href="../../schema-1.0/gpg-44/06-predefined-lists.md">authenticator_quality</a>)</td>
      <td>Predefined list</td>
      <td>The quality of the authenticator according to GPG 44.</td>
    </tr>
  </tbody>
</table>

## Back

- [Presentation experiments](README.md)
- [GPG 44 data model](../../schema-1.0/gpg-44/03-data-model.md)
- [Supporting material](../README.md)
- [Repository home](../../README.md)

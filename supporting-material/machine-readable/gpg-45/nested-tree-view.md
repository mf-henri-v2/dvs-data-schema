<!-- caution-banner:start (wording is kept in tools/caution-banner.md; edit it there) -->
> [!CAUTION]
> This is a working draft of the UK digital verification services trust framework data schema, maintained for collaboration and review. It is not the formally published version and may differ from it. For the published data schema, see [GOV.UK](https://www.gov.uk/government/publications/uk-digital-verification-services-trust-framework-data-schema-1-0).
<!-- caution-banner:end -->

# GPG 45: nested tree view

Every element of the GPG 45 data model, indented to show which element contains which. `[]` marks an array. The [dot-path view](dot-path-view.md) shows the same elements as paths.

This view was written by hand from the [GPG 45 data model](../../../schema-1.0/gpg-45/03-data-model.md). It is not part of the published data schema. If it differs from the data model, the data model is right.

Three elements are used in more than one place: `check_details`, `attachment` and `authority`. Their sub-elements are listed once, at the end.

```text
verified_claims
    claims
        given_name
        family_name
        transliteration_status
            original_language
            transliterated_language
            transliteration_type
        biometric_information[]
            biometric_modality
            attachments[]
        birthdate
        nationalities[]
        address
            street_address
            locality
            postal_code
            country
            transliteration_status
        age
        is_under
        is_over
    verification
        trust_framework
        dvs_registration
            registered_name
            registration_id
        evidence[]
            document
                type
                document_details
                    type
                    document_number
                    serial_number
                    personal_number
                    date_of_issuance
                    date_of_expiry
                    issuer
                    transliteration_status
                attachments[]
                check_details
            electronic_record
                type
                record
                    type
                    reference_number
                    created_at
                    date_of_expiry
                    source
                    transliteration_status
                attachments[]
                check_details
            vouch
                type
                attestation
                    type
                    reference_number
                    date_of_issuance
                    date_of_expiry
                    voucher
                        name
                        birthdate
                        address
                        country_code
                        occupation
                        organisation
                    transliteration_status
                attachments[]
                check_details
        assurance_level
        assurance_process
            policy
            procedure
            assurance_details[]
                assurance_type
                assurance_classification
                evidence_ref[]
                    check_id
                    evidence_ref
                        evidence_classification

# Shared sub-elements referenced from multiple places:
#   check_details.check_method
#   check_details.check_id
#   check_details.time
#   check_details.organisation
#   attachment.desc
#   attachment.content_type
#   attachment.content_format
#   attachment.content
#   authority.name
#   authority.address
#   authority.country_code
#   authority.jurisdiction
```

## Back

- [Data files for GPG 45](README.md)
- [Supporting material](../../README.md)
- [Repository home](../../../README.md)

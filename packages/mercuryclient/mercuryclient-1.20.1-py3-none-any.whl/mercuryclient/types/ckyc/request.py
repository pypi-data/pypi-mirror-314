from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import HttpUrl, conlist

from mercuryclient.types.ckyc.enums import (
    AccountType,
    AddressType,
    CountryCode,
    Gender,
    IndvAddressKyc,
    IndvIdentitiesType,
    IndvImageDocumentTypes,
    IndvRelationPersonType,
    KycTypes,
    LegalAddressKyc,
    LegalConstitutionType,
    LegalIdentitiesType,
    LegalImageDocumentTypes,
    PhotographImageEnum,
    RelationIdentityType,
    RelationshipType,
    StateMaster,
)
from mercuryclient.types.common import NormalizedString


class ImageDetails(BaseModel):
    """
    Image Details
    """

    image_url: HttpUrl


class PhotographImage(ImageDetails):
    """
    Image Details
    """

    image_type: PhotographImageEnum


class IndvImageDetails(ImageDetails):
    """
    Image Details
    """

    image_type: IndvImageDocumentTypes


class LegalImageDetails(ImageDetails):
    """
    Image Details
    """

    image_type: LegalImageDocumentTypes


class NameDetails(BaseModel):
    """
    Name
    """

    name_prefix: NormalizedString = Field(max_length=5)
    first_name: NormalizedString = Field(max_length=50)
    middle_name: Optional[NormalizedString] = Field(max_length=50)
    last_name: Optional[NormalizedString] = Field(max_length=50)


class IndvPersonalDetails(BaseModel):
    """
    personal details
    """

    applicant_name: NameDetails
    applicant_maiden_name: Optional[NameDetails]
    relationship_type: Optional[RelationshipType]
    relationship_person_name: Optional[NameDetails]
    applicant_mother_name: Optional[NameDetails]
    gender: Gender
    date_of_birth: date
    pan_or_form_60: NormalizedString
    applicant_image: PhotographImage


class AddressDetails(BaseModel):

    """
    Address
    """

    address_type: AddressType
    address_line_1: NormalizedString = Field(max_length=55)
    address_line_2: Optional[NormalizedString] = Field(max_length=55)
    address_line_3: Optional[NormalizedString] = Field(max_length=55)
    city: NormalizedString = Field(max_length=50)
    district: NormalizedString = Field(max_length=50)
    state: StateMaster
    country: CountryCode
    pincode: Optional[NormalizedString] = Field(max_length=10)
    id_proof_and_address_proof_same: bool


class IndvAddress(AddressDetails):
    """
    IndvAddress
    """

    address_proof: IndvAddressKyc
    address_proof_other_details: Optional[NormalizedString] = Field(max_length=75)
    address_proof_images: Optional[IndvImageDetails]


class LegalAddress(AddressDetails):
    """
    LegalAddress
    """

    address_proof: LegalAddressKyc
    address_proof_other_details: Optional[NormalizedString] = Field(
        max_length=75,
    )
    address_proof_images: Optional[LegalImageDetails]


class ContactDetails(BaseModel):
    """ContactDetails"""

    office_telephone_code: Optional[NormalizedString] = Field(max_length=4)
    office_telephone_no: Optional[NormalizedString] = Field(max_length=10)
    mobile_code: Optional[NormalizedString] = Field(max_length=3)
    mobile_no: Optional[NormalizedString] = Field(min_length=10, max_length=20)
    email_id: Optional[NormalizedString]


class IndvContactDetails(ContactDetails):

    """
    Contact
    """

    residence_telephone_code: Optional[NormalizedString] = Field(max_length=4)
    residence_telephone_no: Optional[NormalizedString] = Field(max_length=10)


class LegalContactDetails(ContactDetails):

    """
    Contact
    """

    fax_code: Optional[NormalizedString] = Field(max_length=4)
    fax_no: Optional[NormalizedString] = Field(max_length=10)
    alternate_email_id: Optional[NormalizedString]
    alternate_mobile_number_code: Optional[NormalizedString] = Field(max_length=3)
    alternate_mobile_number: Optional[NormalizedString] = Field(
        min_length=10, max_length=20
    )


class KycDetails(BaseModel):
    """
    Kyc
    """

    date_of_declaration: date
    place_of_declaration: NormalizedString = Field(max_length=50)
    kyc_verification_date: date
    type_of_document_submitted: KycTypes
    kyc_verification_name: NormalizedString = Field(max_length=150)
    kyc_verification_designation: NormalizedString = Field(max_length=50)
    kyc_verification_branch: NormalizedString = Field(max_length=50)
    kyc_verification_emp_code: NormalizedString = Field(max_length=50)
    organisation_name: NormalizedString = Field(max_length=150)
    organisation_code: NormalizedString = Field(max_length=7)


class IdentityDetails(BaseModel):
    """
    Identity Details
    """

    identity_number: NormalizedString = Field(max_length=20)
    other_identity_description: Optional[NormalizedString]


class IndvIdentity(IdentityDetails):
    """IndvIdentity"""

    identity_type: IndvIdentitiesType
    identity_image: IndvImageDetails


class LegalIdentity(IdentityDetails):
    """LegalIdentity"""

    identity_type: LegalIdentitiesType
    identity_image: LegalImageDetails


class RelatedIdentity(IdentityDetails):
    """
    Related Identity Details
    """

    identity_type: RelationIdentityType
    identity_image: LegalImageDetails


class RelationPersonDetails(BaseModel):
    """
    Relation Person Details
    """

    related_person_type_others_description: NormalizedString = Field(
        max_length=150, required=False
    )

    ckyc_number: NormalizedString = Field(max_length=14, required=False)
    name: NameDetails
    maiden_name: Optional[NameDetails]
    relationship_type: Optional[RelationshipType]
    relationship_person_name: Optional[NameDetails]
    mother_name: Optional[NameDetails]
    date_of_birth: date
    gender: Gender
    nationality: CountryCode
    pan_or_form_60: NormalizedString = Field(max_length=10)
    related_person_image: PhotographImage
    contact_details: Optional[ContactDetails]
    kyc_verification_details: KycDetails
    remarks: Optional[NormalizedString] = Field(default="", max_length=300)
    identity_details: RelatedIdentity


class IndvRelationPerson(RelationPersonDetails):
    """IndvRelationPerson"""

    address_details: conlist(IndvAddress, max_items=2)  # type: ignore
    type_of_relationship: IndvRelationPersonType


class LegalRelationPerson(RelationPersonDetails):
    """LegalRelationPerson"""

    address_details: conlist(LegalAddress, max_items=2)  # type: ignore
    type_of_relationship: IndvRelationPersonType
    director_identification_number: Optional[NormalizedString] = Field(max_length=8)


class IndividualEntityRequest(BaseModel):

    fi_reference_no: NormalizedString = Field(max_length=20)
    account_type: AccountType
    personal_details: IndvPersonalDetails
    address_details: conlist(IndvAddress, max_items=2)  # type: ignore
    contact_details: Optional[IndvContactDetails]
    remarks: Optional[NormalizedString] = Field(default="", max_length=300)
    kyc_verification_details: KycDetails
    identity_details: conlist(IndvIdentity, min_items=1)  # type: ignore
    relation_person_details: Optional[List[IndvRelationPerson]]


class LegalEntityDetails(BaseModel):
    """
    personal details
    """

    name_of_the_entity: Optional[NormalizedString] = Field(
        max_length=150,
    )

    date_of_incorporation: date
    place_of_incorporation: Optional[NormalizedString] = Field(
        max_length=50,
    )

    date_of_commencement_of_business: Optional[date]
    country_of_incorporation: Optional[CountryCode]

    tin_or_gst_registration_number: Optional[NormalizedString] = Field(
        max_length=20,
    )
    tin_issuing_country: CountryCode
    pan_or_form_60: NormalizedString = Field(max_length=10)


class LegalEntityRequest(BaseModel):
    """LegalEntityRequest"""

    fi_reference_no: NormalizedString = Field(max_length=20)
    constitution_type: LegalConstitutionType
    constitution_type_others: NormalizedString = Field(default="", max_length=20)
    legal_entity_details: LegalEntityDetails
    address_details: conlist(LegalAddress, max_items=2)  # type: ignore
    contact_details: Optional[LegalContactDetails]
    remarks: NormalizedString = Field(default="", required=False, max_length=300)
    kyc_verification_details: KycDetails
    identity_details: conlist(LegalIdentity, min_items=1)  # type: ignore
    relation_person_details: Optional[List[LegalRelationPerson]]

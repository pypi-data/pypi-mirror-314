from datetime import date
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from .enums import (
    AdditionalNameType,
    IDTypes,
    ProductCode,
    InquiryPurpose,
    State,
    AddressType,
    PhoneNumberType,
)

from ..common import Pincode


class Address(BaseModel):
    address_line_1: str = Field(max_length=200)
    address_type: List[AddressType]
    locality: Optional[str] = Field(max_length=40)
    city: Optional[str] = Field(max_length=50)
    state: State
    postal: Pincode


class PhoneNumber(BaseModel):

    number: str = Field(min_length=5, max_length=15)
    number_type: List[PhoneNumberType]


class Identity(BaseModel):
    id_value: str = Field(max_length=20)
    id_type: IDTypes
    source: Optional[str]


class FamilyDetails(BaseModel):
    additional_name_type: AdditionalNameType
    additional_name: str = Field(max_length=200)


class MIFDetails(BaseModel):
    family_details: List[FamilyDetails]


class EquifaxRequest(BaseModel):
    product_code: Optional[List[ProductCode]] = Field(min_items=1, max_items=3)
    inquiry_purpose: Optional[InquiryPurpose]
    first_name: str = Field(max_length=40)
    middle_name: Optional[str] = Field(max_length=40)
    last_name: str = Field(max_length=40)
    dob: Optional[date]
    inquiry_address: Optional[List[Address]] = Field(min_items=1, max_items=3)
    inquiry_phones: List[PhoneNumber] = Field(min_items=1, max_items=3)
    id_details: Optional[List[Identity]] = Field(min_items=1, max_items=10)
    mif_details: Optional[MIFDetails]

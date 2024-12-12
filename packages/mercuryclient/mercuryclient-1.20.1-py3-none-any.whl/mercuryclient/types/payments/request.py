from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


from mercuryclient.types.common import NormalizedString
from mercuryclient.types.payments.enums import PlanType, SubscriptionActionType


class CustomerDetails(BaseModel):

    """
    Customer Details
    """

    name: NormalizedString = Field(max_length=100)
    email: NormalizedString = Field(max_length=100)
    contact: NormalizedString = Field(max_length=15)


class NotesField(BaseModel):
    """
    Notes Field Details
    """

    purpose: Optional[NormalizedString] = Field(max_length=250)


class BankDetails(BaseModel):
    """
    Bank Details
    """

    account_holder_name: NormalizedString
    account_number: NormalizedString
    account_type: NormalizedString
    account_bank_code: NormalizedString


class ItemField(BaseModel):
    """
    Item Field Details
    """

    name: NormalizedString = Field(max_length=80)
    amount: float = Field()
    currency: NormalizedString = Field(max_length=8)
    description: NormalizedString = Field(max_length=250)


class QRCodeDetails(BaseModel):
    """
    QR Code details
    """

    type: NormalizedString = Field(max_length=20)
    name: NormalizedString = Field(max_length=80)
    usage: NormalizedString = Field(max_length=25)
    fixed_amount: bool = Field()
    payment_amount: float = Field()
    description: NormalizedString = Field(max_length=250)
    notes: Optional[NotesField]


class PlanDetails(BaseModel):
    plan_name: Optional[NormalizedString] = Field(max_length=20)
    plan_type: Optional[PlanType]
    plan_currency: Optional[NormalizedString] = Field(max_length=20, default="INR")
    max_amount: Optional[float]
    plan_note: Optional[NormalizedString] = Field(max_length=20)
    plan_recurring_amount: Optional[float]


class CreatePlan(PlanDetails):
    """
    Payment Plan Details
    """

    period: NormalizedString = Field(max_length=20)
    interval: int = Field()
    item: Optional[ItemField]

    plan_id: Optional[NormalizedString] = Field(max_length=20)


class SubscriptionCreation(BaseModel):

    """
    Subscription Creation Details
    """

    plan_id: Optional[NormalizedString] = Field(max_length=100)
    subscription_id: Optional[NormalizedString] = Field(max_length=100)

    total_count: Optional[int] = Field()
    quantity: Optional[int] = Field()
    customer_notify: Optional[bool] = Field(default=False)
    customer_details: Optional[CustomerDetails]
    expiry_time: Optional[datetime] = Field()
    first_charge_time: Optional[datetime] = Field()
    note: Optional[NormalizedString] = Field(max_length=100)
    bank_details: Optional[BankDetails]
    plan_details: Optional[PlanDetails]


class SubscriptionFetch(BaseModel):

    """
    Serializer for subscription fetch
    """

    subscription_id: NormalizedString = Field(max_length=100)


class Notify(BaseModel):

    """
    Notify Details
    """

    sms: bool = Field()
    email: bool = Field()


class PaymentGateway(BaseModel):
    """
    Payment Gateway Link Details
    """

    amount: float = Field()
    currency: NormalizedString = Field(max_length=10)
    accept_partial: bool = Field()
    description: NormalizedString = Field(max_length=250)
    notes: Optional[NotesField]
    customer: CustomerDetails
    notify: Optional[Notify]
    reminder_enable: bool = Field()


class SubscriptionCharge(BaseModel):

    """
    Serializer for subscription Charge
    """

    subscription_id: NormalizedString = Field(max_length=100)
    payment_id: NormalizedString = Field(max_length=100)
    payment_amount: float
    payment_schedule_date: datetime


class SubscriptionManage(BaseModel):

    """
    Serializer for subscription manage
    """

    subscription_id: NormalizedString = Field(max_length=40)
    action: SubscriptionActionType
    next_scheduled_time: Optional[NormalizedString]
    plan_id: Optional[NormalizedString]

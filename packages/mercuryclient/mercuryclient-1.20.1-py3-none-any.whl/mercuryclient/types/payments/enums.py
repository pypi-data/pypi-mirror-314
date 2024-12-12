from enum import Enum


class Endpoints:
    api_endpoints = {
        "generate_qr_code": "generate/qr/code",
        "plan_creation": "plan/create",
        "subscription_creation": "subscription/create",
        "subscription_fetch": "subscription/fetch",
        "payment_link_creation": "payment/link/create",
        "charge_subscription": "subscription/charge",
        "manage_subscription": "subscription/manage",
    }


class PlanType(Enum):
    PERIODIC = "PERIODIC"
    ON_DEMAND = "ON_DEMAND"


class SubscriptionActionType(Enum):
    CANCEL = "CANCEL"
    PAUSE = "PAUSE"
    ACTIVATE = "ACTIVATE"
    CHNAGE_PLAN = "CHANGE_PLAN"

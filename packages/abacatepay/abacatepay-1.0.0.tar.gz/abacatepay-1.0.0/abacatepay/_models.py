from typing import List, Union
from ._constants import BILLING_STATUS, BILLING_METHODS, BILLING_KINDS
from pydantic import BaseModel


class Product(BaseModel):
    externalId: str
    name: str
    quantity: int
    price: int
    description: str


class Customer(BaseModel):
    taxId: str
    name: str
    email: str
    cellphone: str


class CostumerResponse:
    def __init__(self, data: dict):
        self.data = data
        self._format_json(data)

    def _format_json(self, data: dict):
        self.id = data.get("id")
        self.taxId: str = data.get("metadata", {}).get("taxId")
        self.name: str = data.get("metadata", {}).get("name")
        self.email: str = data.get("metadata", {}).get("email")
        self.cellphone: str = data.get("metadata", {}).get("cellphone")


class BillingResponse:
    def __init__(self, data: dict):
        self.data = data
        self._format_json(data)

    def _format_json(self, data: dict):
        billing_data = data

        self.id: str = billing_data["id"]
        self.url: str = billing_data["url"]
        self.amount: int = billing_data["amount"]
        self.status: BILLING_STATUS = billing_data["status"]
        self.dev_mode: bool = billing_data["devMode"]
        self.methods: List[BILLING_METHODS] = billing_data["methods"]
        self.products: List[dict] = billing_data["products"]
        self.frequency: BILLING_KINDS = billing_data["frequency"]
        self.next_billing: Union[str, None] = billing_data.get(
            "nextBilling"
        )  # Optional field
        self.customer: Union[CostumerResponse, None] = (
            CostumerResponse(data=billing_data.get("customer"))
            if "customer" in billing_data
            else None
        )  # Optional field
        self.account_id: str = billing_data.get("accountId")
        self.store_id: str = billing_data.get("storeId")
        self.created_at: str = billing_data.get("createdAt")
        self.updated_at: str = billing_data.get("updatedAt")

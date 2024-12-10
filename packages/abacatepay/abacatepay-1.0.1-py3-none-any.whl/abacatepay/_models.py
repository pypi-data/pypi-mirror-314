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
    """
    Customer model

    Attributes:
        id: str | None
        taxId: str | None
        name: str | None
        email: str
        cellphone: str | None
    Note: never pass `id` as an argument, it is supposed to be returned by the API!
    """
    id: str | None = None
    taxId: str | None = None
    name: str | None = None
    email: str
    cellphone: str | None = None

    @classmethod
    def from_dict(cls, data: dict):
        metadata = data.get("metadata", {})
        return cls(
            id = data.get("id"),
            taxId=metadata.get("taxId"),
            name=metadata.get("name"),
            email=metadata.get("email"),
            cellphone=metadata.get("cellphone"),
        )





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
        self.customer: Union[Customer, None] = (
            Customer.from_dict(data=billing_data.get("customer"))
            if "customer" in billing_data
            else None
        )  # Optional field
        self.account_id: str = billing_data.get("accountId")
        self.store_id: str = billing_data.get("storeId")
        self.created_at: str = billing_data.get("createdAt")
        self.updated_at: str = billing_data.get("updatedAt")

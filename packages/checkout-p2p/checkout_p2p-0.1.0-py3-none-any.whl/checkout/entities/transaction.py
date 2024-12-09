from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from checkout.entities.amount_conversion import AmountConversion
from checkout.entities.discount import Discount
from checkout.entities.name_value_pair import NameValuePair
from checkout.entities.status import Status
from checkout.enums.status_enum import StatusEnum


class Transaction(BaseModel):
    reference: str = Field(..., description="Commerce-provided reference")
    internal_reference: Union[str, int] = Field(
        default="", alias="internalReference", description="PlacetoPay reference"
    )
    payment_method: str = Field(default="", alias="paymentMethod", description="Payment method identifier")
    payment_method_name: str = Field(default="", alias="paymentMethodName", description="Payment method name")
    issuer_name: str = Field(default="", alias="issuerName", description="Name of the issuer")
    amount: Optional[AmountConversion] = Field(default=None, description="Amount conversion details")
    authorization: str = Field(default="", description="Authorization code")
    receipt: str = Field(default="", description="Receipt number")
    franchise: str = Field(default="", description="Franchise identifier")
    refunded: bool = Field(default=False, description="Refund status of the transaction")
    processor_fields: List[NameValuePair] = Field(
        default_factory=list, alias="processorFields", description="Processor fields"
    )
    discount: Optional[Discount] = Field(default=None, description="Discount information")
    status: Optional[Status] = Field(default=None, description="Transaction status")
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    def is_successful(self) -> bool:
        """
        Determines if the transaction is valid (query successful, not necessarily approved).
        """
        return bool(self.status and self.status.status != StatusEnum.ERROR)

    def is_approved(self) -> bool:
        """
        Determines if the transaction has been approved.
        """
        return bool(self.status and self.status.status == StatusEnum.APPROVED)

    def set_processor_fields(self, data: List[dict]) -> None:
        """
        Set the processor fields from a list of dictionaries.
        """
        if isinstance(data, dict) and "item" in data:
            data = data["item"]

        self.processor_fields = [NameValuePair(**nvp) for nvp in data]

    def processor_fields_to_array(self) -> List[dict]:
        """
        Convert processor fields to a list of dictionaries.
        """
        return [field.to_dict() for field in self.processor_fields]

    def additional_data(self) -> Dict[str, str]:
        """
        Parse processor fields as a key-value dictionary.
        """
        return {field.keyword: field.value for field in self.processor_fields}

    def to_dict(self) -> dict:
        """
        Convert the Transaction object to a dictionary.
        """
        return {
            "status": self.status.to_dict() if self.status else None,
            "internalReference": self.internal_reference,
            "paymentMethod": self.payment_method,
            "paymentMethodName": self.payment_method_name,
            "issuerName": self.issuer_name,
            "amount": self.amount.to_dict() if self.amount else None,
            "authorization": self.authorization,
            "reference": self.reference,
            "receipt": self.receipt,
            "franchise": self.franchise,
            "refunded": self.refunded,
            "discount": self.discount.to_dict() if self.discount else None,
            "processorFields": self.processor_fields_to_array(),
        }

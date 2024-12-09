from typing import Optional

from pydantic import BaseModel, Field

from checkout.entities.status import Status
from checkout.entities.transaction import Transaction


class ReverseResponse(BaseModel):
    status: Optional[Status] = Field(default=None, description="Status of the reversal response")
    payment: Optional[Transaction] = Field(default=None, description="Transaction details associated with the reversal")

    def to_dict(self) -> dict:
        """
        Convert the ReverseResponse object to a dictionary.
        """
        return {
            "status": self.status.to_dict() if self.status else None,
            "payment": self.payment.to_dict() if self.payment else None,
        }

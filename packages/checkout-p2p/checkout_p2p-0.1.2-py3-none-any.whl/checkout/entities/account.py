from typing import Optional

from pydantic import BaseModel, Field

from checkout.entities.status import Status


class Account(BaseModel):
    bankCode: str = Field(..., description="Code of the bank")
    bankName: str = Field(..., description="Name of the bank")
    accountType: str = Field(default="", description="Type of the account")
    accountNumber: str = Field(default="", description="Number of the account")
    status: Optional[Status] = Field(default=None, description="Status of the account")

    def to_dict(self) -> dict:
        """
        Convert the Account object to a dictionary.
        """
        return {
            "status": self.status.to_dict() if self.status else None,
            "bankCode": self.bankCode,
            "bankName": self.bankName,
            "accountType": self.accountType,
            "accountNumber": self.accountNumber,
        }

    def get_type(self) -> str:
        """
        Returns the type of the entity (always 'account').
        """
        return "account"

    def last_digits(self) -> str:
        """
        Returns the last 4 digits of the account number.
        """
        return self.accountNumber[-4:] if self.accountNumber else ""

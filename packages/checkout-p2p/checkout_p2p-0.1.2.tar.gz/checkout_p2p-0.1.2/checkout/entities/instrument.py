from typing import Optional

from pydantic import BaseModel, Field

from checkout.entities.account import Account
from checkout.entities.credit import Credit
from checkout.entities.token import Token


class Instrument(BaseModel):
    bank: Optional[Account] = Field(default=None, description="Associated bank account")
    token: Optional[Token] = Field(default=None, description="Associated token")
    credit: Optional[Credit] = Field(default=None, description="Associated credit information")
    pin: str = Field(default="", description="PIN for the instrument")
    password: str = Field(default="", description="Password for the instrument")

    def to_dict(self) -> dict:
        """
        Convert the Instrument object to a dictionary.
        """
        return {
            "bank": self.bank.to_dict() if self.bank else None,
            "token": self.token.to_dict() if self.token else None,
            "credit": self.credit.to_dict() if self.credit else None,
            "pin": self.pin,
            "password": self.password,
        }

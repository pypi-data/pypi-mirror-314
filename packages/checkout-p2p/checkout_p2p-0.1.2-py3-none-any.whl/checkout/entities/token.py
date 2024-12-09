from datetime import datetime

from pydantic import BaseModel, Field


class Token(BaseModel):
    token: str = Field(default="", description="Unique token identifier")
    subtoken: str = Field(default="", description="Secondary token identifier")
    franchise: str = Field(default="", description="Franchise associated with the token")
    franchiseName: str = Field(default="", description="Name of the franchise")
    issuerName: str = Field(default="", description="Name of the issuer")
    lastDigits: str = Field(default="", description="Last digits of the card/token")
    validUntil: str = Field(default="", description="Expiration date in ISO format")
    cvv: str = Field(default="", description="CVV associated with the token")
    installments: int = Field(default=0, description="Number of installments")

    def expiration(self) -> str:
        """
        Convert valid_until to 'mm/yy' format for expiration date.
        """
        try:
            expiration_date = datetime.strptime(self.validUntil, "%Y-%m-%d")
            return expiration_date.strftime("%m/%y")
        except ValueError:
            return "Invalid date"

    def to_dict(self) -> dict:
        """
        Convert the Token object to a dictionary using the Pydantic model_dump method.
        """
        return self.model_dump()

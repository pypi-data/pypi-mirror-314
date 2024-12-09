from pydantic import BaseModel, Field


class Address(BaseModel):
    street: str = Field(default="", description="Street address")
    city: str = Field(default="", description="City")
    state: str = Field(default="", description="State or province")
    postalCode: str = Field(default="", description="Postal code")
    country: str = Field(default="", description="Country")
    phone: str = Field(default="", description="Phone number associated with the address")

    def to_dict(self) -> dict:
        """
        Convert the address object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()

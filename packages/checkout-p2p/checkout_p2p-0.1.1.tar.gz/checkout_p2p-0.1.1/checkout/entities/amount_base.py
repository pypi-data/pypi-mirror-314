from pydantic import BaseModel, Field


class AmountBase(BaseModel):
    currency: str = Field(default="COP", description="Currency code")
    total: float = Field(..., description="Total amount")

    def to_dict(self) -> dict:
        """
        Convert the AmountBase object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()

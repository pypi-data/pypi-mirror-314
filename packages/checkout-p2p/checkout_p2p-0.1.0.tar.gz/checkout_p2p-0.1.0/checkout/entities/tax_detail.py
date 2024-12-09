from typing import Optional

from pydantic import BaseModel, Field


class TaxDetail(BaseModel):
    kind: str = Field(..., description="The type of tax")
    amount: float = Field(..., description="The tax amount")
    base: Optional[float] = Field(default=None, description="The base amount for the tax calculation")

    def to_dict(self) -> dict:
        """
        Convert the TaxDetail object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()

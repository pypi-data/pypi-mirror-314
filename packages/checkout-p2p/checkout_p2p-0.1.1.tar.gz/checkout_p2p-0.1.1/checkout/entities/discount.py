from typing import Optional

from pydantic import BaseModel, Field


class Discount(BaseModel):
    code: str = Field(..., description="The discount code")
    type: str = Field(..., description="The type of discount")
    amount: float = Field(..., description="The amount of the discount")
    base: float = Field(..., description="The base amount for the discount calculation")
    percent: Optional[float] = Field(default=None, description="The percentage of the discount, if applicable")

    def to_dict(self) -> dict:
        """
        Convert the Discount object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()

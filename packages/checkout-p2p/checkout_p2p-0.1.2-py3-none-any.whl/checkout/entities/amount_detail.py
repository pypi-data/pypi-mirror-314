from pydantic import BaseModel, Field


class AmountDetail(BaseModel):
    kind: str = Field(..., description="The type of amount")
    amount: float = Field(..., description="The amount value")

    def to_dict(self) -> dict:
        """
        Convert the AmountDetail object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()

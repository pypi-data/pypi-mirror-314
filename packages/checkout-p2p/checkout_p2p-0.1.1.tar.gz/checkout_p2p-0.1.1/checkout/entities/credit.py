from pydantic import BaseModel, Field


class Credit(BaseModel):
    code: str = Field(..., description="Credit code")
    type: str = Field(..., description="Type of credit")
    groupCode: str = Field(..., description="Group code of the credit")
    installment: int = Field(..., description="Number of installments when first created")

    def to_dict(self) -> dict:
        """
        Convert the Credit object to a dictionary using the Pydantic model_dump method.
        """
        return self.model_dump()

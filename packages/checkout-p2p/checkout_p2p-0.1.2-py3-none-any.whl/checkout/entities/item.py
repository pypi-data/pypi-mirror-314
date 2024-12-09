from pydantic import BaseModel, Field


class Item(BaseModel):
    sku: str = Field(default="", description="Stock Keeping Unit (SKU) of the item")
    name: str = Field(default="", description="Name of the item")
    category: str = Field(default="", description="Category of the item")
    qty: str = Field(default="", description="Quantity of the item")
    price: str = Field(default="", description="Price of the item")
    tax: str = Field(default="", description="Tax applied to the item")

    def to_dict(self) -> dict:
        """
        Convert the Item object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()

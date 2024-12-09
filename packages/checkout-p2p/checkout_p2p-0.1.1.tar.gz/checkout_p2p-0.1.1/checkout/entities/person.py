from typing import Optional

from pydantic import BaseModel, Field

from checkout.entities.address import Address


class Person(BaseModel):
    document: str = Field(default="", description="Document number of the person")
    documentType: str = Field(default="", description="Type of document (e.g., ID, Passport)")
    name: str = Field(default="", description="First name of the person")
    surname: str = Field(default="", description="Last name of the person")
    company: str = Field(default="", description="Company name if applicable")
    email: Optional[str] = Field(default="", description="Email address of the person")
    mobile: str = Field(default="", description="Mobile number of the person")
    address: Optional[Address] = Field(default=None, description="Address information")

    def is_business(self) -> bool:
        """
        Check if the person is representing a business based on their document type.
        """
        return bool(self.documentType and self._business_document(self.documentType))

    @staticmethod
    def _business_document(document_type: str) -> bool:
        """
        Placeholder for business document validation.
        Replace this with actual logic similar to DocumentHelper::businessDocument.
        """
        business_document_types = {"TIN", "VAT", "EIN"}
        return document_type in business_document_types

    def to_dict(self) -> dict:
        """
        Convert the person object to a dictionary using the new `model_dump` method.
        """
        return self.model_dump(exclude_none=True)

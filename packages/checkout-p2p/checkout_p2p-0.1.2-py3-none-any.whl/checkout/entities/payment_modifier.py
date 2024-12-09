from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PaymentModifier(BaseModel):
    TYPE_FEDERAL_GOVERNMENT: str = "FEDERAL_GOVERNMENT"

    type: Optional[str] = Field(default=None, description="Type of payment modifier")
    code: Optional[str] = Field(default=None, description="Code associated with the payment modifier")
    additional: Dict[str, Any] = Field(default_factory=dict, description="Additional data for the payment modifier")

    def set_type(self, type: Optional[str]) -> "PaymentModifier":
        """
        Set the type of the payment modifier.
        """
        self.type = type
        return self

    def set_code(self, code: Optional[str]) -> "PaymentModifier":
        """
        Set the code of the payment modifier.
        """
        self.code = code
        return self

    def get_additional(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get additional data by key. If key is not provided, return the entire additional data dictionary.
        """
        if key:
            return self.additional.get(key, default)
        return self.additional

    def set_additional(self, additional: Dict[str, Any]) -> "PaymentModifier":
        """
        Set the additional data for the payment modifier.
        """
        self.additional = additional
        return self

    def merge_additional(self, data: Dict[str, Any]) -> "PaymentModifier":
        """
        Merge the current additional data with new data.
        """
        self.additional.update(data)
        return self

    def to_dict(self) -> dict:
        """
        Convert the PaymentModifier object to a dictionary.
        """
        return {
            "type": self.type,
            "code": self.code,
            "additional": self.additional,
        }

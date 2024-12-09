from typing import List, Optional

from pydantic import BaseModel, Field

from checkout.entities.name_value_pair import NameValuePair
from checkout.mixins.fields_mixin import FieldsMixin


class Subscription(BaseModel, FieldsMixin):
    reference: str = Field(default="", description="Reference for the subscription")
    description: str = Field(default="", description="Description of the subscription")
    customFields: Optional[List[NameValuePair]] = Field(
        default_factory=lambda: [], description="Additional fields for the subscription"
    )

    def to_dict(self) -> dict:
        """
        Convert the subscription object to a dictionary including fields.
        """
        data = self.model_dump()
        data["fields"] = self.fields_to_array()
        return data

from typing import Optional

from pydantic import ConfigDict, Field

from checkout.decorators.convert_to_boolean import convert_booleans_to_strings
from checkout.entities.instrument import Instrument
from checkout.messages.requests.redirect import RedirectRequest


class CollectRequest(RedirectRequest):

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    instrument: Optional[Instrument] = Field(..., description="Instrument details")
    return_url: str = Field(default="", alias="returnUrl", description="URL to return to after processing")
    ip_address: str = Field(default="", alias="ipAddress", description="IP address of the user")
    user_agent: str = Field(default="", alias="userAgent", description="User agent of the user's browser")

    @convert_booleans_to_strings
    def to_dict(self) -> dict:
        """
        Convert the CollectRequest object to a dictionary.
        """
        parent_dict = super().to_dict()

        return {
            **parent_dict,
            "instrument": self.instrument.to_dict() if self.instrument else "",
        }

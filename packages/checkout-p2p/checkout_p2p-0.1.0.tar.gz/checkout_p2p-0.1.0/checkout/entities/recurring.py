from typing import Optional

from pydantic import BaseModel, Field


class Recurring(BaseModel):
    periodicity: str = Field(
        ...,
        description="Frequency of the transaction (Y = annual, M = monthly, D = daily)",
    )
    interval: int = Field(..., description="Interval between payments")
    nextPayment: str = Field(default="", description="Next payment date")
    maxPeriods: Optional[int] = Field(
        default=None,
        description="Maximum times the recurrence will happen, -1 if unlimited",
    )
    dueDate: str = Field(default="", description="Due date for the recurring charge")
    notificationUrl: str = Field(default="", description="URL for sending notifications")

    def to_dict(self) -> dict:
        """
        Convert the Recurring object to a dictionary using the Pydantic `model_dump` method.
        """
        return self.model_dump()

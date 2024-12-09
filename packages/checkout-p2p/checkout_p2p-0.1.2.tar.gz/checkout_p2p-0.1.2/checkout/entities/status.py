from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from checkout.enums.status_enum import StatusEnum


class Status(BaseModel):
    status: StatusEnum
    reason: str
    message: str = Field(default="", description="Status message")
    date: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())

    def is_successful(self) -> bool:
        return self.status == StatusEnum.OK

    def is_approved(self) -> bool:
        return self.status == StatusEnum.APPROVED

    def is_rejected(self) -> bool:
        return self.status == StatusEnum.REJECTED

    def is_error(self) -> bool:
        return self.status == StatusEnum.ERROR

    @classmethod
    def quick(
        cls,
        status: StatusEnum,
        reason: str,
        message: str = "",
        date: Optional[str] = None,
    ) -> "Status":
        return cls(status=status, reason=reason, message=message, date=date)

    def to_dict(self) -> dict:
        """
        Convert the Status object to a dictionary.
        """
        return {
            "status": self.status.value,
            "reason": self.reason,
            "message": self.message,
            "date": self.date,
        }

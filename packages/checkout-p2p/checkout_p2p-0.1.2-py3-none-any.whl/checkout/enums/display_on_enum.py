from enum import Enum


class DisplayOnEnum(str, Enum):
    NONE = "none"
    """Not displayed in any view of the payment process. Ideal for keeping the data hidden."""

    PAYMENT = "payment"
    """Displayed only in the payment information entry view. Useful for showing data during input."""

    RECEIPT = "receipt"
    """Displayed only in the payment result view. Perfect for showing information in the final step."""

    BOTH = "both"
    """Displayed in both the payment and result views. Ensures visibility in all payment steps."""

    APPROVED = "approved"
    """Displayed in the result view only if the payment is successful."""

from dataclasses import dataclass


@dataclass
class PaymentView:
    payment_id: str
    status: str
    amount_due: float
    last_updated_at: str

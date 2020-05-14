from datetime import datetime
from src.domain.models.domain_event import DomainEvent


class PaymentCreated(DomainEvent):
    def __init__(self, payment_id: str, amount_due: float, created_at: str = datetime.utcnow().isoformat()):
        super().__init__(payment_id, created_at)
        self._amount_due = amount_due

    @property
    def amount_due(self) -> float:
        return self._amount_due

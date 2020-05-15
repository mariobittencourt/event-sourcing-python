from datetime import datetime
from src.domain.models.domain_event import DomainEvent


class PaymentCreated(DomainEvent):
    def __init__(self, aggregate_id: str, amount_due: float, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(aggregate_id, occurred_at)
        self.amount_due = amount_due

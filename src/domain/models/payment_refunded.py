from datetime import datetime
from src.domain.models.domain_event import DomainEvent


class PaymentRefunded(DomainEvent):
    def __init__(self, aggregate_id: str, amount_refunded: float, refund_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(aggregate_id, occurred_at)
        self.amount_refunded = amount_refunded
        self.refund_id = refund_id

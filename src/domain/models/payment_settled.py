from datetime import datetime
from src.domain.models.domain_event import DomainEvent


class PaymentSettled(DomainEvent):
    def __init__(self, aggregate_id: str, amount_settled: float, settlement_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(aggregate_id, occurred_at)
        self.amount_settled = amount_settled
        self.settlement_id = settlement_id

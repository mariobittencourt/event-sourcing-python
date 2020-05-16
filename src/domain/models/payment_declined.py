from datetime import datetime
from src.domain.models.domain_event import DomainEvent


class PaymentDeclined(DomainEvent):
    def __init__(self, aggregate_id: str, bank_name: str, decline_code: int, decline_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(aggregate_id, occurred_at)
        self.decline_code = decline_code
        self.decline_id = decline_id
        self.bank_name = bank_name


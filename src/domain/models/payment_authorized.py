from datetime import datetime
from src.domain.models.domain_event import DomainEvent


class PaymentAuthorized(DomainEvent):
    def __init__(self, aggregate_id: str, bank_name: str, authorization_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(aggregate_id, occurred_at)
        self.bank_name = bank_name
        self.authorization_id = authorization_id

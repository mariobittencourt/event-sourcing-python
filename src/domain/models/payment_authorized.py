from datetime import datetime
from src.domain.models.domain_event import DomainEvent


class PaymentAuthorized(DomainEvent):
    def __init__(self, payment_id: str, bank_name: str, authorization_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(payment_id, occurred_at)
        self._bank_name = bank_name
        self._authorization_id = authorization_id

    @property
    def bank_name(self) -> str:
        return self._bank_name

    @property
    def authorization_id(self) -> str:
        return self._authorization_id

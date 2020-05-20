from datetime import datetime

from src.domain.models.transaction import Transaction


class Refund(Transaction):
    def __init__(self, amount_refunded: float, refund_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(occurred_at)
        self._amount_refunded = amount_refunded
        self._refund_id = refund_id

    @property
    def amount_refunded(self) -> float:
        return self._amount_refunded

    @property
    def refund_id(self) -> str:
        return self._refund_id

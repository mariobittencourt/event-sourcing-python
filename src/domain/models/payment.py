from __future__ import annotations

from src.domain.models.aggregate import Aggregate, method_dispatch
from src.domain.models.domain_event import DomainEvent
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_id import PaymentId
from src.domain.models.payment_status import PaymentStatus


class Payment(Aggregate):
    def __init__(self, payment_id: PaymentId):
        super().__init__()
        self._payment_id = payment_id

    @classmethod
    def create(cls, payment_id: PaymentId, amount_due: float) -> Payment:
        payment = cls(payment_id)
        created = PaymentCreated(payment_id.value, amount_due)
        payment.apply(created)
        payment.events.append(created)
        return payment

    @method_dispatch
    def apply(self, event: DomainEvent):
        raise ValueError('Unknown event!')

    @apply.register(PaymentCreated)
    def _(self, event: PaymentCreated):
        self._status = PaymentStatus.PENDING_PROCESSING
        self._amount_due = event.amount_due

    @property
    def status(self) -> PaymentStatus:
        return self._status

    @property
    def payment_id(self) -> PaymentId:
        return self._payment_id

    @property
    def amount_due(self) -> float:
        return self._amount_due

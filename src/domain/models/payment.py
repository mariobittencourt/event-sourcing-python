from __future__ import annotations

from src.domain.models.aggregate import Aggregate, method_dispatch
from src.domain.models.authorization import Authorization
from src.domain.models.domain_event import DomainEvent
from src.domain.models.payment_authorized import PaymentAuthorized
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_id import PaymentId
from src.domain.models.payment_status import PaymentStatus


class Payment(Aggregate):
    def __init__(self, payment_id: PaymentId):
        super().__init__()
        self._payment_id = payment_id

    @property
    def status(self) -> PaymentStatus:
        return self._status

    @property
    def payment_id(self) -> PaymentId:
        return self._payment_id

    @property
    def amount_due(self) -> float:
        return self._amount_due

    @property
    def transactions(self):
        return self._transactions

    @classmethod
    def create(cls, payment_id: PaymentId, amount_due: float) -> Payment:
        payment = cls(payment_id)
        payment.apply(PaymentCreated(payment_id.value, amount_due))
        return payment

    @method_dispatch
    def apply(self, event: DomainEvent):
        raise ValueError('Unknown event!')

    @apply.register(PaymentCreated)
    def _(self, event: PaymentCreated):
        self._status = PaymentStatus.PENDING_PROCESSING
        self._amount_due = event.amount_due
        self._transactions = []
        self.events.append(event)

    def authorize(self, bank_name: str, authorization_id: str):
        if self.status == PaymentStatus.PENDING_PROCESSING:
            self.apply(PaymentAuthorized(self.payment_id.value, bank_name, authorization_id))
        else:
            raise Exception('Only pending payments can be authorized')

    @apply.register(PaymentAuthorized)
    def _(self, event: PaymentAuthorized):
        self._status = PaymentStatus.AUTHORIZED
        transaction = Authorization(event.bank_name, event.authorization_id, event.occurred_at)
        self.transactions.append(transaction)
        self.events.append(event)

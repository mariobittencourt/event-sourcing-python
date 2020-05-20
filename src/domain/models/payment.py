from __future__ import annotations

from src.domain.models.aggregate import Aggregate, method_dispatch
from src.domain.models.authorization import Authorization
from src.domain.models.decline import Decline
from src.domain.models.domain_event import DomainEvent
from src.domain.models.payment_authorized import PaymentAuthorized
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_declined import PaymentDeclined
from src.domain.models.payment_id import PaymentId
from src.domain.models.payment_settled import PaymentSettled
from src.domain.models.payment_status import PaymentStatus
from src.domain.models.settlement import Settlement


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

    def settle(self, bank_name: str, amount_settled: float, settlement_id: str):
        # Some business rule. For example if the amount is less than the amount due etc.
        self.apply(PaymentSettled(self.payment_id.value, bank_name, amount_settled, settlement_id))

    @apply.register(PaymentSettled)
    def _(self, event: PaymentSettled):
        # In real scenario, validate if amount is equal before setting the status to something specific
        self._status = PaymentStatus.SETTLED
        self._amount_due -= event.amount_settled
        transaction = Settlement(bank_name=event.bank_name, amount_settled=event.amount_settled, settlement_id=event.settlement_id)
        self.transactions.append(transaction)
        self.events.append(event)

    def decline(self, bank_name: str, decline_code: int, decline_id: str):
        # again some business rules
        self.apply(PaymentDeclined(self.payment_id.value, bank_name, decline_code, decline_id))

    @apply.register(PaymentDeclined)
    def _(self, event: PaymentDeclined):
        self._status = PaymentStatus.DECLINED.value
        transaction = Decline(decline_code=event.decline_code, decline_id=event.decline_id)
        self.transactions.append(transaction)
        self.events.append(event)

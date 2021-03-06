from __future__ import annotations

from src.domain.models.aggregate import Aggregate, method_dispatch
from src.domain.models.authorization import Authorization
from src.domain.models.decline import Decline
from src.domain.models.domain_event import DomainEvent
from src.domain.models.invalid_state_error import InvalidStateError
from src.domain.models.payment_authorized import PaymentAuthorized
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_declined import PaymentDeclined
from src.domain.models.payment_id import PaymentId
from src.domain.models.payment_refunded import PaymentRefunded
from src.domain.models.payment_settled import PaymentSettled
from src.domain.models.payment_status import PaymentStatus
from src.domain.models.refund import Refund
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
        payment.record_that(PaymentCreated(payment_id.value, amount_due))
        return payment

    @method_dispatch
    def apply(self, event: DomainEvent):
        raise ValueError('Unknown event!')

    @apply.register(PaymentCreated)
    def _(self, event: PaymentCreated):
        self._status = PaymentStatus.PENDING_PROCESSING
        self._amount_due = event.amount_due
        self._transactions = []

    def authorize(self, bank_name: str, authorization_id: str) -> None:
        if self.status == PaymentStatus.PENDING_PROCESSING:
            self.record_that(PaymentAuthorized(self.payment_id.value, bank_name, authorization_id))
        else:
            raise Exception('Only pending payments can be authorized')

    @apply.register(PaymentAuthorized)
    def _(self, event: PaymentAuthorized):
        self._status = PaymentStatus.AUTHORIZED
        transaction = Authorization(
            bank_name=event.bank_name, authorization_id=event.authorization_id, occurred_at=event.occurred_at
        )
        self.transactions.append(transaction)

    def settle(self, bank_name: str, amount_settled: float, settlement_id: str) -> None:
        # Some business rules. For example if the amount is less than the amount due etc.
        if self.status != PaymentStatus.PENDING_PROCESSING and self.status != PaymentStatus.AUTHORIZED:
            raise InvalidStateError('only pending or authorized payments can be settled')

        if self.amount_due != amount_settled:
            raise InvalidStateError('The settled amount is different than the amount due')

        self.record_that(PaymentSettled(self.payment_id.value, bank_name, amount_settled, settlement_id))

    @apply.register(PaymentSettled)
    def _(self, event: PaymentSettled):
        self._status = PaymentStatus.SETTLED
        self._amount_due -= event.amount_settled
        transaction = Settlement(
            bank_name=event.bank_name, amount_settled=event.amount_settled, settlement_id=event.settlement_id
        )
        self.transactions.append(transaction)

    def decline(self, bank_name: str, decline_code: int, decline_id: str) -> None:
        # again some business rules
        if self.status != PaymentStatus.PENDING_PROCESSING:
            raise InvalidStateError('Only pending payments can be declined')
        self.record_that(PaymentDeclined(self.payment_id.value, bank_name, decline_code, decline_id))

    @apply.register(PaymentDeclined)
    def _(self, event: PaymentDeclined):
        self._status = PaymentStatus.DECLINED
        transaction = Decline(
            decline_code=event.decline_code, decline_id=event.decline_id, occurred_at=event.occurred_at
        )
        self.transactions.append(transaction)

    def refund(self, amount_refunded: float, refund_id: str) -> None:
        # business rules
        if self.status != PaymentStatus.SETTLED:
            raise InvalidStateError('Only settled payments can be refunded')
        self.record_that(PaymentRefunded(
            aggregate_id=self.payment_id.value, amount_refunded=amount_refunded, refund_id=refund_id)
        )

    @apply.register(PaymentRefunded)
    def _(self, event: PaymentRefunded):
        self._status = PaymentStatus.REFUNDED
        transaction = Refund(
            refund_id=event.refund_id, amount_refunded=event.amount_refunded, occurred_at=event.occurred_at
        )
        self.transactions.append(transaction)
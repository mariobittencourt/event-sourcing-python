from src.domain.views.projector import method_dispatch
from src.domain.models.domain_event import DomainEvent
from src.domain.models.payment_authorized import PaymentAuthorized
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_declined import PaymentDeclined
from src.domain.models.payment_refunded import PaymentRefunded
from src.domain.models.payment_settled import PaymentSettled
from src.domain.models.payment_status import PaymentStatus
from src.domain.views.customer.payment_projection import PaymentProjection


class PaymentProjector:
    def __init__(self, projection: PaymentProjection):
        self.projection = projection

    @method_dispatch
    def apply(self, event: DomainEvent):
        raise ValueError('Unknown event!')

    @apply.register(PaymentCreated)
    def _(self, event: PaymentCreated):
        self.projection.create_payment(
            payment_id=event.aggregate_id,
            status=PaymentStatus.PENDING_PROCESSING.value,
            amount_due=event.amount_due,
            last_updated_at=event.occurred_at
        )

    @apply.register(PaymentAuthorized)
    def _(self, event: PaymentAuthorized):
        self.projection.make_payment_authorized(
            payment_id=event.aggregate_id,
            status=PaymentStatus.AUTHORIZED.value,
            last_updated_at=event.occurred_at
        )

    @apply.register(PaymentSettled)
    def _(self, event: PaymentSettled):
        self.projection.make_payment_settled(
            payment_id=event.aggregate_id,
            status=PaymentStatus.SETTLED.value,
            amount_settled=event.amount_settled,
            last_updated_at=event.occurred_at
        )

    @apply.register(PaymentDeclined)
    def _(self, event: PaymentDeclined):
        self.projection.make_payment_declined(
            payment_id=event.aggregate_id,
            status=PaymentStatus.DECLINED.value,
            last_updated_at=event.occurred_at
        )

    @apply.register(PaymentRefunded)
    def _(self, event: PaymentRefunded):
        self.projection.make_payment_refunded(
            payment_id=event.aggregate_id,
            status=PaymentStatus.REFUNDED.value,
            amount_refunded=event.amount_refunded,
            last_updated_at=event.occurred_at
        )
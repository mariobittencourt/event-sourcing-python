import functools

from src.domain.models.domain_event import DomainEvent
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_status import PaymentStatus
from src.domain.views.payment_projection import PaymentProjection


def method_dispatch(func):
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


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

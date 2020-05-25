import functools

from src.domain.models.domain_event import DomainEvent
from src.domain.models.payment_declined import PaymentDeclined
from src.domain.views.finance.decline_projection import DeclineProjection


def method_dispatch(func):
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


class DeclineProjector:
    def __init__(self, projection: DeclineProjection):
        self.projection = projection

    @method_dispatch
    def apply(self, event: DomainEvent):
        pass

    @apply.register(PaymentDeclined)
    def _(self, event: PaymentDeclined):
        self.projection.update_decline_code_count(decline_code=event.decline_code, bank_name=event.bank_name, date=event.occurred_at[0:10])

import abc

from src.domain.models.payment import Payment
from src.domain.models.payment_id import PaymentId


class PaymentRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'save') and
            callable(subclass.save) and
            hasattr(subclass, 'find_by_id') and
            callable(subclass.find_by_id)
            or NotImplemented
        )

    def save(self, payment: Payment) -> bool:
        raise NotImplementedError

    def find_by_id(self, payment_id: PaymentId) -> Payment:
        raise NotImplementedError
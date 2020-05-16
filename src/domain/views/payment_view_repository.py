import abc

from src.domain.views.payment_view import PaymentView


class PaymentViewRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'insert') and
            callable(subclass.insert) and
            hasattr(subclass, 'update') and
            callable(subclass.update) and
            hasattr(subclass, 'find_by_id') and
            callable(subclass.find_by_id)
            or NotImplemented
        )

    def insert(self, payment: PaymentView) -> bool:
        raise NotImplementedError

    def update(self, payment: PaymentView) -> bool:
        raise NotImplementedError

    def find_by_id(self, payment_id: str) -> PaymentView:
        raise NotImplementedError

import abc

from src.domain.models.payment import Payment


class PaymentRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'save') and
            callable(subclass.save) or
            NotImplemented
        )

    def save(self, payment: Payment) -> bool:
        raise NotImplementedError

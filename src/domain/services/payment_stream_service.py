import abc


class PaymentStreamService(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'subscribe') and
            callable(subclass.subscribe)
            or NotImplemented
        )

    def subscribe(self, stream: str, start_from: int, projectionist):
        raise NotImplementedError

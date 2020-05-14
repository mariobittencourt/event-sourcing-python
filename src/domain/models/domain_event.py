from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime


class DomainEvent(ABC, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, aggregate_id: str, occurred_at: datetime):
        self._type = self.__class__.__name__
        self._aggregate_id = aggregate_id
        self._occurred_at = occurred_at

    @property
    def type(self) -> str:
        return self._type

    @property
    def aggregate_id(self) -> str:
        return self._aggregate_id

    @property
    def occurred_at(self) -> datetime:
        return self._occurred_at

from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime
import json


class DomainEventEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class DomainEvent(ABC, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, aggregate_id: str, occurred_at: str):
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
    def occurred_at(self) -> str:
        return self._occurred_at

    def encode(self):
        return DomainEventEncoder().encode(self)

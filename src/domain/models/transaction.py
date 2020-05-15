from abc import ABC, ABCMeta, abstractmethod


class Transaction(ABC, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, occurred_at: str):
        self._occurred_at = occurred_at

    @property
    def occurred_at(self) -> str:
        return self._occurred_at

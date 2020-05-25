import abc
from typing import Optional, List

from src.domain.views.finance.decline_view import DeclineView


class DeclineViewRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'increment_occurrence') and
            callable(subclass.increment_occurrence) and
            hasattr(subclass, 'initialize') and
            callable(subclass.initialize) and
            hasattr(subclass, 'reset') and
            callable(subclass.reset) and
            hasattr(subclass, 'find_by_decline_code') and
            callable(subclass.find_by_decline_code)
            or NotImplemented
        )

    def initialize(self) -> bool:
        raise NotImplementedError

    def reset(self) -> bool:
        raise NotImplementedError

    def increment_occurrence(self, decline_code: int, bank_name: str, date: str) -> bool:
        raise NotImplementedError

    def find_by_decline_code(self, decline_code: int) -> List[DeclineView]:
        raise NotImplementedError


from typing import Optional
import abc

from src.domain.views.ledger import Ledger


class LedgerRepository(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'find_by_id') and
            callable(subclass.find_by_id) and
            hasattr(subclass, 'initialize') and
            callable(subclass.initialize) and
            hasattr(subclass, 'reset') and
            callable(subclass.reset) and
            hasattr(subclass, 'find_by_projection_name') and
            callable(subclass.find_by_projection_name)
            or NotImplemented
        )

    def find_by_id(self, ledger_id: int) -> Optional[Ledger]:
        raise NotImplementedError

    def find_by_projection_name(self, projection_name: str) -> Optional[Ledger]:
        raise NotImplementedError

    def initialize(self) -> bool:
        raise NotImplementedError

    def reset(self) -> bool:
        raise NotImplementedError

    def insert(self, ledger: Ledger) -> bool:
        raise NotImplementedError

    def update(self, ledger: Ledger) -> bool:
        raise NotImplementedError

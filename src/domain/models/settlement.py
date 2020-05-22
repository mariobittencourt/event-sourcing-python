from datetime import datetime

from src.domain.models.transaction import Transaction


class Settlement(Transaction):
    def __init__(self, bank_name: str, amount_settled: float, settlement_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(occurred_at)
        self._amount_settled = amount_settled
        self._settlement_id = settlement_id
        self._bank_name = bank_name

    @property
    def amount_settled(self) -> float:
        return self._amount_settled

    @property
    def settlement_id(self) -> str:
        return self._settlement_id

    @property
    def bank_name(self) -> str:
        return self._bank_name

    def __str__(self):
        return f'\tBank name: {self.bank_name}\n\tAmount settled: {self.amount_settled}\n\tSettlement ID: {self.settlement_id}\n\t{Transaction.__str__(self)}'

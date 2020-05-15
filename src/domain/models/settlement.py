from src.domain.models.transaction import Transaction


class Settlement(Transaction):
    def __init__(self, amount_settled: float, settlement_id: str, occurred_at: str):
        super().__init__(occurred_at)
        self._amount_settled = amount_settled
        self._settlement_id = settlement_id

    @property
    def amount_settled(self) -> float:
        return self._amount_settled

    @property
    def settlement_id(self) -> str:
        return self._settlement_id

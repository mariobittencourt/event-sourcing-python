from datetime import datetime

from src.domain.models.transaction import Transaction


class Decline(Transaction):
    def __init__(self, decline_code: int, decline_id: str, occurred_at: str = datetime.utcnow().isoformat()):
        super().__init__(occurred_at)
        self._decline_code = decline_code
        self._decline_id = decline_id

    @property
    def decline_code(self) -> str:
        return self._decline_code

    @property
    def decline_id(self) -> int:
        return self._decline_id

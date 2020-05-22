from src.domain.models.transaction import Transaction


class Authorization(Transaction):
    def __init__(self, bank_name: str, authorization_id: str, occurred_at: str):
        super().__init__(occurred_at)
        self._bank_name = bank_name
        self._authorization_id = authorization_id

    @property
    def bank_name(self) -> str:
        return self._bank_name

    @property
    def authorization_id(self) -> str:
        return self._authorization_id

    def __str__(self):
        return f'\tBank name: {self.bank_name}\n\tAuthorization ID: {self.authorization_id}\n\t{Transaction.__str__(self)}'

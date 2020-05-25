from src.domain.views.finance.decline_view_repository import DeclineViewRepository


class DeclineProjection:
    def __init__(self, repository: DeclineViewRepository):
        self.repository = repository

    def boot(self) -> bool:
        return self.repository.initialize()

    def update_decline_code_count(self, decline_code: int, bank_name: str, date: str) -> bool:
        self.repository.increment_occurrence(decline_code, bank_name, date)
        return True

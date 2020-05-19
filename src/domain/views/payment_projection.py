from src.domain.views.payment_view import PaymentView
from src.domain.views.payment_view_repository import PaymentViewRepository


class PaymentProjection:
    def __init__(self, repository: PaymentViewRepository):
        self.repository = repository

    def create_payment(self, payment_id: str, status: str, amount_due: float, last_updated_at: str):
        payment_view = PaymentView(
            payment_id=payment_id,
            status=status,
            amount_due=amount_due,
            last_updated_at=last_updated_at
        )
        self.repository.insert(payment_view)
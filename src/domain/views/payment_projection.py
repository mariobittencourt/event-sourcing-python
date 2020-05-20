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

    def make_payment_authorized(self, payment_id: str, status: str, last_updated_at: str):
        payment_view = self.repository.find_by_id(payment_id)
        if payment_view is not None:
            payment_view.status = status
            payment_view.last_updated_at = last_updated_at
            self.repository.update(payment_view)

    def make_payment_settled(self, payment_id: str, status: str, amount_settled: float, last_updated_at: str):
        payment_view = self.repository.find_by_id(payment_id)
        if payment_view is not None:
            payment_view.status = status
            payment_view.amount_due -= amount_settled
            payment_view.last_updated_at = last_updated_at
            self.repository.update(payment_view)

class PaymentView:
    def __init__(self, payment_id: str, status: str, amount_due: float, last_updated_at: str):
        self.payment_id = payment_id
        self.status = status
        self.amount_due = amount_due
        self.last_updated_at = last_updated_at

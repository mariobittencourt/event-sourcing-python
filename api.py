from src.domain.models.payment import Payment
from src.domain.models.payment_id import PaymentId

payment = Payment.create(PaymentId, 10.00)
print(payment)
print(payment.events)
import asyncio

from src.domain.models.payment import Payment
from src.domain.models.payment_id import PaymentId
from src.infrastructure.domain.models.event_store_payment_repository import EventStorePaymentRepository


async def save(payment: Payment):
    repository = EventStorePaymentRepository(username='admin', password='changeit')
    await repository.save(payment)

if __name__ == "__main__":
    payment = Payment.create(PaymentId(), 10.00)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save(payment))

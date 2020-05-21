import asyncio

from src.domain.models.payment import Payment
from src.domain.models.payment_id import PaymentId
from src.infrastructure.domain.models.event_store_payment_repository import EventStorePaymentRepository


async def save(my_payment: Payment):
    repository = EventStorePaymentRepository(username='admin', password='changeit')
    await repository.save(my_payment)


async def find(my_payment: Payment):
    repository = EventStorePaymentRepository(username='admin', password='changeit')
    await repository.find_by_id(my_payment.payment_id)


if __name__ == "__main__":
    payment = Payment.create(PaymentId(), 10.00)
    payment.authorize('BMO', 'xxx-uuu-id')
    payment.settle('BMO', amount_settled=9.00, settlement_id='xxx-zzz-id')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save(payment))

    payment = Payment.create(PaymentId(), 100.00)
    payment.decline(bank_name='BMO', decline_code=999, decline_id='zzz-uuu-id')
    loop.run_until_complete(save(payment))

    payment = Payment.create(PaymentId(), 1000.00)
    payment.settle(bank_name='BMO', settlement_id='zzz-uuu-zzz', amount_settled=999)
    payment.refund(amount_refunded=998, refund_id='888-refund')
    loop.run_until_complete(save(payment))

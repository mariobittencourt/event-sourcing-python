import asyncio
import sqlite3

from src.domain.models.payment import Payment
from src.domain.models.payment_id import PaymentId
from src.domain.views.payment_view import PaymentView
from src.infrastructure.domain.models.event_store_payment_repository import EventStorePaymentRepository
from src.infrastructure.domain.views.sqlite_payment_view_repository import SqlitePaymentViewRepository


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
    loop.run_until_complete(find(payment))

    payment_view_repository = SqlitePaymentViewRepository('./payment_view.sqlite')
    try:
        payment_view_repository.create()
    except sqlite3.OperationalError:
        pass

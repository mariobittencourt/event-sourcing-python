import asyncio
import photonpump
from photonpump.conversations import VolatileSubscription

from src.domain.models.payment_authorized import PaymentAuthorized
from src.domain.models.payment_created import PaymentCreated
from src.domain.models.payment_status import PaymentStatus
from src.domain.views.payment_view import PaymentView
from src.infrastructure.domain.models.event_store_payment_repository import EventStorePaymentRepository
from src.infrastructure.domain.views.sqlite_payment_view_repository import SqlitePaymentViewRepository


async def import_stream():
    repository = SqlitePaymentViewRepository(database_name='payment_view.sqlite')
    client = photonpump.connect(username='admin', password='changeit')
    await client.connect()
    event: photonpump.Event
    subscription: VolatileSubscription = await client.subscribe_to(stream='$ce-payments', start_from=0)
    async for event in subscription.events:
        event_payload = await EventStorePaymentRepository.convert_to_domain_event(event)
        if event.type == PaymentCreated.__name__:
            event_payload: PaymentCreated
            payment_view = PaymentView(
                payment_id=event_payload.aggregate_id,
                status=PaymentStatus.PENDING_PROCESSING.value,
                amount_due=event_payload.amount_due,
                last_updated_at=event_payload.occurred_at
            )
            repository.insert(payment_view)
        elif event.type == PaymentAuthorized.__name__:
            event_payload: PaymentAuthorized
            payment_view = repository.find_by_id(event_payload.aggregate_id)
            if payment_view is not None:
                payment_view.status = PaymentStatus.AUTHORIZED.value
                payment_view.last_updated_at = event_payload.occurred_at
                repository.update(payment_view)

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(import_stream())
    except KeyboardInterrupt:
        print('Bye')
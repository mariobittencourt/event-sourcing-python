import asyncio
import photonpump

from src.domain.views.payment_projection import PaymentProjection
from src.domain.views.payment_projector import PaymentProjector
from src.infrastructure.domain.services.event_store_stream_service import PaymentProjectionist, EventStoreStreamService
from src.infrastructure.domain.views.sqlite_payment_view_repository import SqlitePaymentViewRepository


async def import_stream():
    # Use DI and config files (.env) to initialize in real life
    repository = SqlitePaymentViewRepository(database_name='../../../../payment_view.sqlite')
    projection = PaymentProjection(repository)

    projector = PaymentProjector(projection)

    stream_service = EventStoreStreamService(photonpump.connect(username='admin', password='changeit'))
    projectionist = PaymentProjectionist(projector, stream_service)
    await projectionist.start()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(import_stream())
    except KeyboardInterrupt:
        print('Bye')

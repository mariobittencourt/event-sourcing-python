import asyncio
import photonpump

from src.config.settings import DATABASE_NAME, EVENT_STORE_PASSWORD, EVENT_STORE_USERNAME
from src.domain.views.payment_projection import PaymentProjection
from src.domain.views.payment_projector import PaymentProjector
from src.infrastructure.domain.services.event_store_stream_service import PaymentProjectionist, EventStoreStreamService
from src.infrastructure.domain.views.sqlite_ledger_repository import SqliteLedgerRepository
from src.infrastructure.domain.views.sqlite_payment_view_repository import SqlitePaymentViewRepository


async def import_stream():
    # Use DI to initialize in real life
    database_name = f"../../../../{DATABASE_NAME}"
    ledger_repository = SqliteLedgerRepository(database_name=database_name)

    repository = SqlitePaymentViewRepository(database_name=database_name)
    projection = PaymentProjection(repository)

    projector = PaymentProjector(projection)

    stream_service = EventStoreStreamService(
        photonpump.connect(username=EVENT_STORE_USERNAME, password=EVENT_STORE_PASSWORD)
    )
    projectionist = PaymentProjectionist(projector, stream_service, ledger_repository=ledger_repository)
    await projectionist.start()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(import_stream())
    except KeyboardInterrupt:
        print('Bye')

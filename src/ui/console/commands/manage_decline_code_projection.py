import asyncio
import photonpump

from src.config.settings import DATABASE_NAME, EVENT_STORE_PASSWORD, EVENT_STORE_USERNAME, DECLINE_PROJECTION
from src.domain.views.finance.decline_projection import DeclineProjection
from src.domain.views.finance.decline_projectionist import DeclineProjectionist
from src.domain.views.finance.decline_projector import DeclineProjector
from src.infrastructure.domain.services.event_store_stream_service import PaymentProjectionist, EventStoreStreamService
from src.infrastructure.domain.views.finance.sqlite_decline_view_repository import SqliteDeclineViewRepository
from src.infrastructure.domain.views.sqlite_ledger_repository import SqliteLedgerRepository


async def import_stream():
    # Use DI to initialize in real life
    database_name = f"../../../../{DATABASE_NAME}"
    ledger_repository = SqliteLedgerRepository(database_name=database_name)

    repository = SqliteDeclineViewRepository(database_name=database_name)
    projection = DeclineProjection(repository)

    projector = DeclineProjector(projection)

    stream_service = EventStoreStreamService(
        photonpump.connect(username=EVENT_STORE_USERNAME, password=EVENT_STORE_PASSWORD)
    )
    projectionist = DeclineProjectionist(
        projector=projector, stream_service=stream_service, ledger_repository=ledger_repository, ledger_name=DECLINE_PROJECTION
    )
    await projectionist.start()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(import_stream())
    except KeyboardInterrupt:
        print('Bye')
